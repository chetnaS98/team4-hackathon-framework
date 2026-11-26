#!/usr/bin/env python3
"""Add a line to the break log or the playbook changes log.

Usage:
  python log.py break  --engagement <folder> --what "<what broke>" --instead "<what we did>" --severity blocked|slowed|minor [--stage <stage>]
  python log.py change --engagement <folder> --what "<what changed>" --why "<why>" --by "<who made the call>" [--stage <stage>]

--stage defaults to the active stage. Lines are appended; nothing is ever rewritten.
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _koru as k  # noqa: E402


def cell(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["break", "change"])
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--stage")
    ap.add_argument("--what", required=True)
    ap.add_argument("--instead", default="")
    ap.add_argument("--severity", choices=["blocked", "slowed", "minor"])
    ap.add_argument("--why", default="")
    ap.add_argument("--by", default="")
    a = ap.parse_args()

    eng = Path(a.engagement).expanduser().resolve()
    if not k.is_engagement(eng):
        sys.exit(f"ERROR: {eng} is not a koru engagement")
    stage = a.stage
    if not stage:
        active = [s for s in k.stage_table((eng / "00-read-me-first.md").read_text(encoding="utf-8")) if s["status"] == "active"]
        stage = active[0]["title"] if active else "core"
    now = datetime.datetime.now()

    if a.kind == "break":
        if not a.severity or not a.instead.strip():
            sys.exit("ERROR: a break needs --instead and --severity")
        team = (k.load_json(eng / ".koru" / "project.json", {}) or {}).get("team", "")
        f = eng / "break-log.md"
        row = f"| {now:%Y-%m-%d %H:%M} | {cell(team)} | {cell(stage)} | {cell(a.what)} | {cell(a.instead)} | {a.severity} |"
    else:
        if not a.why.strip() or not a.by.strip():
            sys.exit("ERROR: a playbook change needs --why and --by")
        f = eng / "playbook-changes.md"
        row = f"| {now:%Y-%m-%d} | {cell(a.what)} | {cell(stage)} | {cell(a.why)} | {cell(a.by)} |"
    if not f.is_file():
        sys.exit(f"ERROR: {f.name} is missing (engagement made before these logs existed); create it from koru-core/assets/templates/")
    with f.open("a", encoding="utf-8") as h:
        h.write(row + "\n")
    print(f"Logged in {f.name}: {row}")


if __name__ == "__main__":
    main()
