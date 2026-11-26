#!/usr/bin/env python3
"""Set up a new koru engagement from the intake answers, in one go.

Usage:
  python intake.py --answers <answers.json> [--dry-run]

The /koru:next command asks the intake questions, writes the answers to a JSON file and runs this.
It then: creates the engagement (koru-core init_engagement), starts Frame (init_stage), fills the
read-me (what the project is, size, knowledge base, design system path, roles, client decision
makers and review rhythm, the request material list), copies the client material into
stages/frame/sources/ unchanged, logs the kickoff decisions, and runs the roles gate.

answers.json keys (only project, out and made_by are required; anything missing stays TODO and the
roles gate will say so):
  project          code name, lowercase letters and digits (never the client's real name)
  out              parent folder for the engagement
  made_by          the person answering (logged as who made the kickoff decisions)
  team             team name (used in the break log)
  what             one line: what the project is
  client_alias     how derived artefacts name the client (default "the client")
  size             small or large
  design_system    {"path": "with" | "partial" | "without", "where": "<link or folder>"}
  research_exists  true (validated research on this exact problem: roadmap path) or false (discovery)
  knowledge_base   where final files will live (for example "Claude project: Meridian")
  sources          list of files or folders holding the client material
  request          list of file names that are "the request" (brief, PRD, kickoff transcripts)
  roles            {"Team lead": "Name", "Researcher": "Name", ...}
  decision_makers  text
  review_rhythm    text
Exit 0 when set up (even if the roles gate still fails: that is reported), 1 on an error.
"""
import argparse
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _koru as k  # noqa: E402

DS_TEXT = {
    "with": "with DS: {w} (use only its components and tokens)",
    "partial": "with DS, partial: {w} (use what exists, list every gap; Explore and Harden run the with-DS path and record what must be built)",
    "without": "without DS: {w} (plain wireframes first; tokens and components captured as you go)",
}


def sub_line(text, label, value):
    pat = re.compile(rf"^\*\*{re.escape(label)}:\*\*.*$", re.M)
    return pat.sub(f"**{label}:** {value}", text, count=1) if pat.search(text) else text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ans = json.loads(Path(a.answers).read_text(encoding="utf-8"))
    for key in ("project", "out", "made_by"):
        if not str(ans.get(key, "")).strip():
            sys.exit(f"ERROR: answers.json needs '{key}'")
    project, who = ans["project"].strip(), ans["made_by"].strip()
    if not re.fullmatch(r"[a-z][a-z0-9]*", project):
        sys.exit("ERROR: project must be lowercase letters and digits only, e.g. meridian")
    out = Path(ans["out"]).expanduser().resolve()
    eng = out / project
    if eng.exists():
        sys.exit(f"ERROR: {eng} already exists. Run /koru:next to resume it.")
    sources = [Path(s).expanduser() for s in ans.get("sources", [])]
    missing = [str(s) for s in sources if not s.exists()]
    if missing:
        sys.exit("ERROR: these source paths don't exist: " + ", ".join(missing))
    size = ans.get("size", "small")
    if size not in ("small", "large"):
        sys.exit("ERROR: size must be small or large")
    ds = ans.get("design_system") or {}
    if ds and ds.get("path") not in DS_TEXT:
        sys.exit("ERROR: design_system.path must be with, partial or without")
    frame = k.find_skill("koru-frame")
    if not frame:
        sys.exit("ERROR: koru-frame is not installed")

    plan = [f"create {eng}", "start Frame", f"copy {len(sources)} source path(s) into stages/frame/sources/",
            "fill the read-me", "log the kickoff decisions", "run the roles gate"]
    if a.dry_run:
        print("Dry run. Would:\n  - " + "\n  - ".join(plan))
        return

    core = k.core_dir()
    today = datetime.date.today().isoformat()
    rc, o = k.run_core(core, "init_engagement.py", "--project", project, "--out", out, "--size", size,
                       "--client-alias", ans.get("client_alias", "the client"), "--date", today)
    if rc:
        sys.exit(o)
    rc, o = k.run_core(core, "init_stage.py", "--engagement", eng, "--stage-dir", frame)
    if rc:
        sys.exit(o)

    # team name for the break log
    pj = eng / ".koru" / "project.json"
    meta = json.loads(pj.read_text(encoding="utf-8"))
    meta["team"] = ans.get("team", "")
    pj.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # copy client material unchanged
    dest = eng / "stages" / "frame" / "sources"
    copied = []
    for s in sources:
        if s.is_dir():
            for f in sorted(s.rglob("*")):
                if f.is_file() and not any(p.startswith(".") for p in f.relative_to(s).parts):
                    t = dest / f.relative_to(s)
                    t.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, t)
                    copied.append(str(f.relative_to(s)))
        else:
            shutil.copy2(s, dest / s.name)
            copied.append(s.name)

    # read-me
    rm = eng / "00-read-me-first.md"
    t = rm.read_text(encoding="utf-8")
    if ans.get("what"):
        t = sub_line(t, "What the project is", ans["what"])
    if ans.get("knowledge_base"):
        t = sub_line(t, "Knowledge base", ans["knowledge_base"])
    if ds:
        t = sub_line(t, "Design system", DS_TEXT[ds["path"]].format(w=ds.get("where", "link TODO")))
    for role, name in (ans.get("roles") or {}).items():
        if str(name).strip():
            t = re.sub(rf"^\|\s*{re.escape(role)}\s*\|[^|\n]*\|$", f"| {role} | {name.strip()} |", t, count=1, flags=re.M)
    if ans.get("decision_makers"):
        t = re.sub(r"^- Decision makers:.*$", f"- Decision makers: {ans['decision_makers']}", t, count=1, flags=re.M)
    if ans.get("review_rhythm"):
        t = re.sub(r"^- Review rhythm:.*$", f"- Review rhythm: {ans['review_rhythm']}", t, count=1, flags=re.M)
    req = ans.get("request") or []
    block = "\n## Request material\n" + ("".join(f"- {r}\n" for r in req) if req else "- To confirm at Frame step 1\n") + \
            f"\nEverything else in `stages/frame/sources/` ({len(copied)} files) is related material for steps 3 and 5.\n"
    t = t.replace("\n## Where everything lives", block + "\n## Where everything lives", 1)
    rm.write_text(t, encoding="utf-8")

    # decisions log
    log = eng / "05-decisions-log.md"
    lt = log.read_text(encoding="utf-8").replace("| TODO |", f"| {who} |")
    lines = []
    if ds:
        lines.append(f"| {today} | core | Design system path: {ds['path']} ({ds.get('where', '')}) | 00-read-me-first | {who} | The other paths |")
    if "research_exists" in ans:
        path = "roadmap (validated research exists on this exact problem)" if ans["research_exists"] else "discovery (no validated research on this exact problem)"
        lines.append(f"| {today} | frame | Provisional path: {path}; confirmed at step 4 | - | {who} | The other path |")
    if req:
        lines.append(f"| {today} | frame | Request material: {', '.join(req)} | 00-read-me-first | {who} | Treat more files as the request |")
    log.write_text(lt.rstrip("\n") + "\n" + "".join(l + "\n" for l in lines), encoding="utf-8")

    rc, gate = k.run_core(core, "check_roles.py", eng)
    print(f"Engagement ready: {eng}")
    print(f"  Frame started · {len(copied)} source files copied · design system: {ds.get('path', 'not decided')}")
    print("  " + gate.replace("\n", "\n  "))
    print("Next: /koru:next" if rc == 0 else "Next: name the missing owners, then /koru:next")


if __name__ == "__main__":
    main()
