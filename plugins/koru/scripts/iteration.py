#!/usr/bin/env python3
"""Start the next iteration of a stage with versioned handoffs (Ship): v1 is the first handoff to the build team,
v2 the next round after their feedback, and so on. Nothing from an earlier iteration is overwritten.

Usage:
  python iteration.py --engagement <folder> --by "<name>" --reason "<why another round>" [--stage Ship] [--from S3] [--dry-run]

Refuses unless the current iteration was handed over (its card handoff-cards/<project>-ship-handoff-card-v<n>.md exists).
Then it:
  - records iteration n+1 in .koru/progress.json (route.py and the Ship skill read it),
  - sets the tracker rows from --from (default: stage.json "iteration_restart_step", S3 for Ship) to the end back to
    "not started"; the earlier rows keep their status,
  - reopens the stage if it was handed off (stage table and .koru/stages.json back to "active"),
  - logs the decision with the person's name and reason.
Every artefact made in iteration n+1 is a new version; the new handoff card is -v<n+1>, and the handoff note
says what changed since iteration n.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _koru as k  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--by", required=True)
    ap.add_argument("--reason", required=True)
    ap.add_argument("--stage", default="Ship")
    ap.add_argument("--from", dest="from_step")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    eng = Path(a.engagement).expanduser().resolve()
    if not k.is_engagement(eng):
        sys.exit(f"ERROR: {eng} is not a koru engagement")
    rm = eng / "00-read-me-first.md"
    text = rm.read_text(encoding="utf-8")
    proj = k.load_json(eng / ".koru" / "project.json", {}).get("project")
    stages = k.stage_table(text)
    st = next((s for s in stages if s["title"].lower() == a.stage.lower()), None)
    if not st:
        sys.exit(f"ERROR: no stage '{a.stage}' in the stage table")
    key = k.stage_key(st["title"])
    d = k.find_skill(st["skill"]) if st["skill"] else None
    meta = k.stage_meta(d)
    if not meta.get("versioned_handoff"):
        sys.exit(f"REFUSED: {st['title']} does not use iterations (no \"versioned_handoff\" in its stage.json). "
                 "Changes there are new versions plus a send-back.")
    if st["status"] not in ("active", "handed off"):
        sys.exit(f"REFUSED: {st['title']} is '{st['status']}'; it has not run yet.")
    from step import named_people  # noqa: E402
    if a.by.strip().lower() not in named_people(text):
        sys.exit(f"REFUSED: '{a.by}' is not named in the Roles table.")

    n = k.iteration(eng, key)
    card = k.handoff_card_path(eng, proj, key, d)
    if not card.is_file():
        sys.exit(f"REFUSED: iteration {n} has not been handed over yet ({card.name} does not exist). "
                 f"Rework inside iteration {n} is new versions of the drafts; start iteration {n + 1} after the handoff.")

    start = (a.from_step or meta.get("iteration_restart_step") or "").strip().lower()
    lines = text.splitlines()
    h = next(i for i, l in enumerate(lines) if re.match(rf"^##\s+{re.escape(st['title'])} step tracker\s*$", l, re.I))
    head_i = next(i for i in range(h + 1, len(lines)) if lines[i].strip().startswith("|"))
    head = [c.strip().lower() for c in lines[head_i].strip().strip("|").split("|")]
    col = {c: head.index(c) for c in ("step", "status", "checker", "date") if c in head}
    reset, on = [], not start
    for i in range(head_i + 2, len(lines)):
        if not lines[i].strip().startswith("|"):
            break
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if k.step_key(cells[col["step"]]) == start:
            on = True
        if on:
            cells[col["status"]] = "not started"
            for c in ("checker", "date"):
                if c in col:
                    cells[col[c]] = ""
            lines[i] = "| " + " | ".join(cells) + " |"
            reset.append(cells[col["step"]].split(" ")[0])
    if start and not reset:
        sys.exit(f"ERROR: step '{a.from_step}' not found in the {st['title']} tracker")

    print(f"{st['title']}: iteration {n} was handed over ({card.name}). Starting iteration {n + 1}.")
    print(f"  steps back to not started: {', '.join(reset)}")
    print(f"  new handoff card at the end: {k.handoff_card_path(eng, proj, key, d).name.replace(f'-v{n}.md', f'-v{n + 1}.md')}")
    if a.dry_run:
        print("Dry run: nothing written.")
        return

    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if st["status"] == "handed off":
        text = re.sub(rf"^\|\s*{re.escape(st['title'])}\s*\|.*$",
                      f"| {st['title']} | {st['skill']} | active | {st['lead']} | {st['card']} |", text, count=1, flags=re.M)
        sj = k.load_json(eng / ".koru" / "stages.json", {})
        if key in sj.get("stages", {}):
            sj["stages"][key]["status"] = "active"
            (eng / ".koru" / "stages.json").write_text(json.dumps(sj, indent=2), encoding="utf-8")
    rm.write_text(text, encoding="utf-8")

    prog = k.load_progress(eng)
    prog.setdefault("_iterations", {})[key] = n + 1
    prog[key] = {}
    k.save_progress(eng, prog)
    today = datetime.date.today().isoformat()
    with (eng / "05-decisions-log.md").open("a", encoding="utf-8") as f:
        f.write(f"| {today} | {key} | Iteration {n + 1} started after handoff {card.stem}: {a.reason.strip()}. "
                f"Steps {reset[0]}-{reset[-1]} rerun; every artefact is a new version | {card.stem} | {a.by.strip()} | Fix inside iteration {n} |\n")
    print(f"Logged. Iteration {n + 1} is active; run /koru:next.")


if __name__ == "__main__":
    main()
