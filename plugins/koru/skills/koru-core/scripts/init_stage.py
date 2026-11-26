#!/usr/bin/env python3
"""Start a stage in an existing engagement (once per phase).

Usage:
  python init_stage.py --engagement <project-folder> --stage-dir <path to the phase skill>

Reads <stage-dir>/stage.json. Creates stages/<stage>/ with drafts/<each draft folder>/ (and sources/ if
source_folder is true) and templates/, creates the stage's final folders at the engagement root,
copies the phase templates (project, date, size filled in), appends the step tracker to the read-me,
marks the stage active in the stage table, and merges the stage's types and required roles into .koru/.
Refuses to run twice for the same stage.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fill, load_json  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--stage-dir", required=True)
    a = ap.parse_args()

    eng = Path(a.engagement).expanduser()
    sd = Path(a.stage_dir).expanduser()
    if not (eng / "00-read-me-first.md").is_file() or not (eng / ".koru" / "project.json").is_file():
        sys.exit(f"ERROR: {eng} is not a koru engagement (run init_engagement.py first)")
    cfg = load_json(sd / "stage.json")
    if not cfg:
        sys.exit(f"ERROR: {sd}/stage.json not found")
    stage = cfg["stage"]
    proj = load_json(eng / ".koru" / "project.json")
    stages = load_json(eng / ".koru" / "stages.json", {"stages": {}})
    if stage in stages["stages"]:
        sys.exit(f"ERROR: stage '{stage}' is already initialised in {eng}")
    if cfg.get("core_version", 1) != proj.get("core_version", 1):
        print(f"WARNING: stage expects core v{cfg.get('core_version')}, engagement is core v{proj.get('core_version')}")

    root = eng / "stages" / stage
    for d in cfg.get("draft_folders", []):
        (root / "drafts" / d).mkdir(parents=True, exist_ok=True)
    if cfg.get("source_folder"):
        (root / "sources").mkdir(parents=True, exist_ok=True)
    (root / "templates").mkdir(parents=True, exist_ok=True)
    for f in cfg.get("final_folders", []):
        (eng / f).mkdir(exist_ok=True)

    vals = {"project": proj["project"], "date": proj["date"], "size": proj["size"], "client_alias": proj["client_alias"]}
    tdir = sd / cfg.get("templates_dir", "assets/templates")
    if tdir.is_dir():
        for t in sorted([*tdir.glob("*.md"), *tdir.glob("*.html")]):
            (root / "templates" / t.name).write_text(fill(t.read_text(encoding="utf-8"), vals), encoding="utf-8")

    rm = eng / "00-read-me-first.md"
    text = rm.read_text(encoding="utf-8")
    tracker = sd / cfg.get("step_tracker", "assets/stage/step-tracker.md")
    if tracker.is_file():
        text = text.rstrip("\n") + "\n\n" + fill(tracker.read_text(encoding="utf-8"), vals).rstrip("\n") + "\n"
    # stage table row
    row = f"| {cfg['title']} | {cfg.get('skill','')} | active | | |"
    pat = re.compile(rf"^\|\s*{re.escape(cfg['title'])}\s*\|.*$", re.M)
    if pat.search(text):
        text = pat.sub(row, text, count=1)
    else:
        print(f"WARNING: no '{cfg['title']}' row in the read-me stage table; add it by hand")
    rm.write_text(text, encoding="utf-8")

    stages["stages"][stage] = {"title": cfg["title"], "skill": cfg.get("skill"), "number": cfg.get("number"),
                               "required_roles": cfg.get("required_roles", []), "final_folders": cfg.get("final_folders", [])}
    (eng / ".koru" / "stages.json").write_text(json.dumps(stages, indent=2), encoding="utf-8")
    types = load_json(eng / ".koru" / "types.json", {})
    types[stage] = cfg.get("types", [])
    (eng / ".koru" / "types.json").write_text(json.dumps(types, indent=2), encoding="utf-8")
    print(f"Stage '{stage}' started in {eng}")
    print("Next: make sure every required role is named, run check_roles.py, then begin the first step.")


if __name__ == "__main__":
    main()
