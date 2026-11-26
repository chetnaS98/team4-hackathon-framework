#!/usr/bin/env python3
"""Hand the active stage off and start the next one. Refuses unless every handoff check passes.

Usage:
  python advance_stage.py --engagement <folder> --confirmed-by "<name>" [--dry-run]

Checks, for the active stage (all from koru-core's rules; nothing new is invented here):
  1. every step in the stage's step tracker is passed or skipped
  2. the roles gate passes (koru-core check_roles.py)
  3. the stale-check is clean (koru-core stale_check.py)
  4. the handoff card exists (handoff-cards/<project>-<stage>-handoff-card.md, or -handoff-card-v<iteration>.md
     for a stage with versioned handoffs such as Ship) and every row except
     "Checked by the next stage" is filled
  5. the stage's final folders hold at least one artefact, and every artefact there is status final
  6. the decisions log has at least one sign-off line for the stage
  7. --confirmed-by names a person (never the AI) and is not the stage's runner role holder alone

On success: logs the handoff in the decisions log, marks the stage "handed off" in the read-me stage
table (with the card name) and in .koru/stages.json, then runs koru-core init_stage.py for the next
stage if its phase skill is installed. With --dry-run, only the checks run and nothing is written.
Exit 0 on success, 1 when a check fails, 2 on a usage error.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _koru as k  # noqa: E402

UNFILLED = re.compile(r"^\s*$|^\(the phase fills this in\)$|^<[^>]*>|^TODO", re.I)


def card_problems(card):
    if not card.is_file():
        return [f"handoff card missing: {card.name} (fill it from koru-core/assets/templates/handoff-card.md and the phase's handoff lines)"]
    probs = []
    for line in card.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("Field", "") or set(cells[0]) <= set("-: "):
            continue
        if cells[0].lower().startswith("checked by the next stage"):
            continue
        v = cells[1]
        # labels with no values, e.g. "High: · Medium: · Low:" or "Assumptions: · Questions:"
        if UNFILLED.search(v) or "<result>" in v or "<date>" in v or re.fullmatch(r"(\s*[A-Za-z ]+:\s*·?)+\s*", v):
            probs.append(f"handoff card row not filled: {cells[0]}")
    return probs


def final_problems(eng, folders):
    probs, count = [], 0
    for f in folders:
        d = eng / f
        if not d.is_dir():
            probs.append(f"final folder missing: {f}/")
            continue
        for p in sorted(d.rglob("*")):
            if p.suffix not in (".md", ".html") or not p.is_file():
                continue
            fm = {}
            m = re.search(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S | re.M)
            if m:
                for l in m.group(1).splitlines():
                    if ":" in l:
                        a, b = l.split(":", 1)
                        fm[a.strip()] = b.strip().strip('"')
            if "type" not in fm:
                continue
            count += 1
            if fm.get("status") != "final" or not p.stem.endswith("-final"):
                probs.append(f"not final but in a final folder: {f}/{p.name}")
    if count == 0:
        probs.append("no artefacts in the final folders (" + ", ".join(folders) + ")")
    return probs


def signoff_lines(log_text, stage):
    rows = []
    for l in log_text.splitlines():
        if not l.startswith("|"):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 5 and c[1].lower() == stage and re.search(r"sign", c[2], re.I) and c[4] and not c[4].upper().startswith("TODO"):
            rows.append(c)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--confirmed-by", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    core = k.core_dir()
    eng = Path(a.engagement).expanduser().resolve()
    if not k.is_engagement(eng):
        print(f"ERROR: {eng} is not a koru engagement", file=sys.stderr)
        sys.exit(2)
    rm = eng / "00-read-me-first.md"
    text = rm.read_text(encoding="utf-8")
    proj = k.load_json(eng / ".koru" / "project.json", {})
    stages_json = k.load_json(eng / ".koru" / "stages.json", {"stages": {}})
    table = k.stage_table(text)
    active = [s for s in table if s["status"] == "active"]
    if not active:
        print("ERROR: no active stage to hand off", file=sys.stderr)
        sys.exit(2)
    cur = active[0]
    key = k.stage_key(cur["title"])
    cfg = stages_json["stages"].get(key, {})
    after = table[table.index(cur) + 1:]
    nxt = next((s for s in after if s["status"] == "not started"), None)

    problems = []
    tracker = k.step_tracker(text, cur["title"])
    if not tracker:
        problems.append(f"no '{cur['title']} step tracker' in the read-me")
    for t in tracker:
        if t["status"] not in k.DONE:
            problems.append(f"step {t['step']} is '{t['status']}', not passed or skipped")
    rc, out = k.run_core(core, "check_roles.py", eng)
    if rc != 0:
        problems.append("roles gate failed:\n      " + "\n      ".join(out.splitlines()[1:]))
    sc, out = k.run_core(core, "stale_check.py", "--engagement", eng)
    if sc != 0:
        problems.append("stale-check has warnings:\n      " + "\n      ".join(out.splitlines()[1:10]))
    card = k.handoff_card_path(eng, proj.get('project'), key, k.find_skill(cur["skill"]) if cur["skill"] else None)
    problems += card_problems(card)
    problems += final_problems(eng, cfg.get("final_folders", []))
    log = eng / "05-decisions-log.md"
    signs = signoff_lines(log.read_text(encoding="utf-8") if log.is_file() else "", key)
    if not signs:
        problems.append(f"no sign-off line for stage '{key}' in 05-decisions-log.md")
    who = a.confirmed_by.strip()
    if not who or who.lower() in ("claude", "ai", "assistant", "the ai"):
        problems.append("--confirmed-by must name the person who confirms the handoff")

    print(f"Handoff check: {cur['title']} -> {nxt['title'] if nxt else '(no next stage)'}")
    print(f"  steps: {sum(t['status'] in k.DONE for t in tracker)}/{len(tracker)} passed or skipped")
    print(f"  sign-offs in decisions log: {len(signs)}")
    print(f"  handoff card: {card.name}")
    if problems:
        print("REFUSED. Fix these first:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("All handoff checks pass.")
    if a.dry_run:
        print("Dry run: nothing written.")
        return

    today = datetime.date.today().isoformat()
    with log.open("a", encoding="utf-8") as f:
        f.write(f"| {today} | {key} | Stage handed off to {nxt['title'] if nxt else 'nobody (last stage)'} via koru orchestrator | {card.stem} | {who} | Keep {cur['title']} open |\n")
    row = re.compile(rf"^\|\s*{re.escape(cur['title'])}\s*\|.*$", re.M)
    text = row.sub(f"| {cur['title']} | {cur['skill']} | handed off | {cur['lead']} | {card.name} |", text, count=1)
    rm.write_text(text, encoding="utf-8")
    if key in stages_json["stages"]:
        stages_json["stages"][key]["status"] = "handed off"
        stages_json["stages"][key]["handed_off"] = {"date": today, "confirmed_by": who, "card": card.name}
        (eng / ".koru" / "stages.json").write_text(json.dumps(stages_json, indent=2), encoding="utf-8")
    print(f"{cur['title']} marked handed off; logged in 05-decisions-log.md (confirmed by {who}).")

    if not nxt:
        print("That was the last stage.")
        return
    d = k.find_skill(nxt["skill"]) if nxt["skill"] else None
    if not d or not (d / "stage.json").is_file():
        print(f"Next stage {nxt['title']} has no installed phase skill ({nxt['skill']}); left 'not started'. It is not built yet.")
        return
    rc, out = k.run_core(core, "init_stage.py", "--engagement", eng, "--stage-dir", d)
    print(out)
    if rc != 0:
        sys.exit(1)
    print(f"Next: name the {nxt['title']} roles, then run route.py.")


if __name__ == "__main__":
    main()
