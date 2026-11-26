#!/usr/bin/env python3
"""Create a Koru engagement folder (once per project).

Usage:
  python init_engagement.py --project deskly --out <parent-folder> [--size small|large]
                            [--client-alias "the client"] [--date 2026-11-25]

Creates <out>/<project>/ with: 00-read-me-first.md (roles table, stage table), 05-decisions-log.md,
ai-quality-log.md, assumptions-register.md, open-questions-register.md, artefact-registry.md,
handoff-cards/, stages/, and .koru/ (project.json, stages.json, types.json).
Numbers 03 and 04 are reserved for Harden and are not created. Refuses to overwrite.
Then run init_stage.py for the phase you are starting.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import CORE, fill, load_json  # noqa: E402

TEMPLATES = CORE / "assets" / "templates"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True, help="code name, lowercase letters and digits only (never the client's real name)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", choices=["small", "large"], default="small")
    ap.add_argument("--client-alias", default="the client")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9]*", a.project):
        sys.exit("ERROR: --project must be lowercase letters and digits only (no hyphens or spaces), e.g. deskly")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.date):
        sys.exit("ERROR: --date must be YYYY-MM-DD")
    root = Path(a.out).expanduser() / a.project
    if root.exists():
        sys.exit(f"ERROR: {root} already exists; not overwriting. Resume it instead.")

    roles = load_json(CORE / "registry" / "roles.json")
    role_rows = "\n".join(f"| {r['name']} | |" for r in roles["roles"])
    vals = {"project": a.project, "date": a.date, "size": a.size, "client_alias": a.client_alias, "role_rows": role_rows}

    for d in ["handoff-cards", "stages", ".koru"]:
        (root / d).mkdir(parents=True)
    files = {
        "read-me-first.md": "00-read-me-first.md",
        "decisions-log.md": "05-decisions-log.md",
        "ai-quality-log.md": "ai-quality-log.md",
        "assumptions-register.md": "assumptions-register.md",
        "open-questions-register.md": "open-questions-register.md",
        "artefact-registry.md": "artefact-registry.md",
        "break-log.md": "break-log.md",
        "playbook-changes.md": "playbook-changes.md",
    }
    for src, dst in files.items():
        (root / dst).write_text(fill((TEMPLATES / src).read_text(encoding="utf-8"), vals), encoding="utf-8")
    (root / "handoff-cards" / "README.md").write_text(
        "One handoff card per stage handoff, from koru-core/assets/templates/handoff-card.md. "
        "Name: <project>-<stage>-handoff-card.md.\n", encoding="utf-8")
    (root / ".koru" / "project.json").write_text(json.dumps(
        {"project": a.project, "date": a.date, "size": a.size, "client_alias": a.client_alias, "core_version": 1}, indent=2), encoding="utf-8")
    (root / ".koru" / "stages.json").write_text(json.dumps({"stages": {}}, indent=2), encoding="utf-8")
    (root / ".koru" / "types.json").write_text(json.dumps({}, indent=2), encoding="utf-8")

    print(f"Created {root}")
    print("Next: run init_stage.py for the phase you are starting, fill the roles table in 00-read-me-first.md,")
    print("then run check_roles.py. No step may start until the roles gate passes.")


if __name__ == "__main__":
    main()
