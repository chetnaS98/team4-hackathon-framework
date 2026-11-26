#!/usr/bin/env python3
"""Update one row of a stage's step tracker in 00-read-me-first.md. Use this instead of editing the table.

Usage:
  python step.py --engagement <folder> --step <id> --status <status> [--checker "<name>"] [--stage <title>] [--reason "<text>"]

  --step     the step id as the tracker shows it: 2, 14a, A9, H5, S4 ... (matches the start of the Step cell)
  --status   not started | drafted | in check | passed | skipped
  --checker  required for passed; must be a person named in the Roles table
  --stage    defaults to the active stage
  --reason   required for skipped (written into the Checker cell, and logged in the decisions log)

Prints the router's next action afterwards. Exit 1 on a refused update.
"""
import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _koru as k  # noqa: E402

STATUSES = ("not started", "drafted", "in check", "passed", "skipped")


def named_people(text):
    names = set()
    for row in k.section_table(text, "Roles"):
        if len(row) >= 2:
            for n in re.split(r"[,/&]| and ", row[1]):
                n = n.strip()
                if n:
                    names.add(n.lower())
    return names


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--step", required=True)
    ap.add_argument("--status", required=True, choices=STATUSES)
    ap.add_argument("--checker", default="")
    ap.add_argument("--stage")
    ap.add_argument("--reason", default="")
    a = ap.parse_args()

    eng = Path(a.engagement).expanduser().resolve()
    if not k.is_engagement(eng):
        sys.exit(f"ERROR: {eng} is not a koru engagement")
    rm = eng / "00-read-me-first.md"
    text = rm.read_text(encoding="utf-8")
    title = a.stage
    if not title:
        active = [s for s in k.stage_table(text) if s["status"] == "active"]
        if not active:
            sys.exit("ERROR: no active stage; pass --stage")
        title = active[0]["title"]
    title = title.strip().title()

    if a.status == "passed":
        if not a.checker.strip():
            sys.exit("REFUSED: a step is passed only by a named checker (--checker)")
        if a.checker.strip().lower() not in named_people(text):
            sys.exit(f"REFUSED: '{a.checker}' is not named in the Roles table. Add them first (a checker must be a named person).")
    if a.status == "skipped" and not a.reason.strip():
        sys.exit("REFUSED: a skipped step needs --reason")

    lines = text.splitlines()
    try:
        h = next(i for i, l in enumerate(lines) if re.match(rf"^##\s+{re.escape(title)} step tracker\s*$", l, re.I))
    except StopIteration:
        sys.exit(f"ERROR: no '## {title} step tracker' in the read-me")
    head_i = next((i for i in range(h + 1, len(lines)) if lines[i].strip().startswith("|")), None)
    if head_i is None:
        sys.exit("ERROR: the step tracker has no table")
    head = [c.strip().lower() for c in lines[head_i].strip().strip("|").split("|")]
    col = {n: head.index(n) for n in ("step", "status", "checker", "date") if n in head}
    if "step" not in col or "status" not in col:
        sys.exit("ERROR: the tracker table needs Step and Status columns")
    sid = a.step.strip().lower()
    hit = None
    for i in range(head_i + 2, len(lines)):
        l = lines[i]
        if not l.strip().startswith("|"):
            break
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        first = cells[col["step"]].lower()
        if first == sid or re.match(rf"^{re.escape(sid)}(\s|\(|$|:)", first):
            hit = (i, cells)
            break
    if not hit:
        sys.exit(f"ERROR: step '{a.step}' not found in the {title} tracker")
    i, cells = hit
    cells[col["status"]] = a.status
    today = datetime.date.today().isoformat()
    if "checker" in col:
        if a.status == "passed":
            cells[col["checker"]] = a.checker.strip()
        elif a.status == "skipped":
            cells[col["checker"]] = f"skipped: {a.reason.strip()}"
    if "date" in col and a.status in ("passed", "skipped", "drafted", "in check"):
        cells[col["date"]] = today
    lines[i] = "| " + " | ".join(cells) + " |"
    rm.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    print(f"{title} step {a.step}: {a.status}" + (f" (checker {a.checker})" if a.status == "passed" else ""))

    if a.status == "skipped":
        log = eng / "05-decisions-log.md"
        with log.open("a", encoding="utf-8") as f:
            f.write(f"| {today} | {title.lower()} | Step {a.step} skipped: {a.reason.strip()} | - | {a.checker or 'TODO'} | Run the step |\n")

    r = subprocess.run([sys.executable, "-I", str(Path(__file__).with_name("route.py")), "--engagement", str(eng)],
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip())


if __name__ == "__main__":
    main()
