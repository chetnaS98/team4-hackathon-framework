#!/usr/bin/env python3
"""Update a stage's step tracker in 00-read-me-first.md and the step's progress record. Use this instead of
editing the table.

Usage:
  python step.py --engagement <folder> --step <id> --status <status> [options]
  python step.py --engagement <folder> --skip-optional --by "<name>" [--stage <title>]

  --step         the step id as the tracker shows it: 2, 14a, A9, H5, S4 ... (matches the start of the Step cell)
  --status       not started | drafted | in check | passed | skipped
  --checker      required for passed; a person named in the Roles table, never the person who ran the step
  --waiting-on   for "in check": the named checker the step is waiting on (shown by route.py)
  --note         where the step is, in one line ("audit back, findings folded in, lint clean"). Kept in
                 .koru/progress.json and shown by route.py, so a new turn or session knows what is done.
                 Use it at every pause inside a step (an agent launched, an agent back, waiting on a person).
  --by           required for skipped: the named person who decided the skip (logged)
  --reason       why it was skipped. Optional steps (stage.json "optional_steps") have a default reason;
                 any other step needs --reason and --override, and is logged as an override.
  --override     allow skipping a step the stage does not mark optional
  --skip-optional  skip every optional step of the stage that has not started, with its default reason
  --keep         with --skip-optional: optional steps to keep (comma-separated, e.g. 14b when a current platform exists)
  --stage        defaults to the active stage

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


def require_named(text, who, what):
    if not who.strip():
        sys.exit(f"REFUSED: {what} needs a named person")
    if who.strip().lower() not in named_people(text):
        sys.exit(f"REFUSED: '{who}' is not named in the Roles table. Add them first ({what} must be a named person).")


def tracker_rows(lines, title):
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
    rows = []
    for i in range(head_i + 2, len(lines)):
        if not lines[i].strip().startswith("|"):
            break
        rows.append((i, [c.strip() for c in lines[i].strip().strip("|").split("|")]))
    return col, rows


def find_row(col, rows, step):
    sid = step.strip().lower()
    for i, cells in rows:
        first = cells[col["step"]].lower()
        if first == sid or re.match(rf"^{re.escape(sid)}(\s|\(|$|:)", first):
            return i, cells
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--step")
    ap.add_argument("--status", choices=STATUSES)
    ap.add_argument("--checker", default="")
    ap.add_argument("--waiting-on", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--by", default="")
    ap.add_argument("--stage")
    ap.add_argument("--reason", default="")
    ap.add_argument("--override", action="store_true")
    ap.add_argument("--skip-optional", action="store_true")
    ap.add_argument("--keep", default="")
    a = ap.parse_args()
    if not a.skip_optional and not (a.step and a.status):
        ap.error("--step and --status are required (or use --skip-optional)")

    eng = Path(a.engagement).expanduser().resolve()
    if not k.is_engagement(eng):
        sys.exit(f"ERROR: {eng} is not a koru engagement")
    rm = eng / "00-read-me-first.md"
    text = rm.read_text(encoding="utf-8")
    stages = k.stage_table(text)
    title = a.stage
    if not title:
        active = [s for s in stages if s["status"] == "active"]
        if not active:
            sys.exit("ERROR: no active stage; pass --stage")
        title = active[0]["title"]
    title = title.strip().title()
    skill = next((s["skill"] for s in stages if s["title"].lower() == title.lower()), None)
    optional = k.optional_steps(k.find_skill(skill) if skill else None)

    lines = text.splitlines()
    col, rows = tracker_rows(lines, title)
    today = datetime.date.today().isoformat()
    progress = k.load_progress(eng)
    sp = progress.setdefault(title.lower(), {})
    log_lines, done_msgs = [], []

    def set_row(i, cells, status, checker_cell=None):
        cells[col["status"]] = status
        if "checker" in col and checker_cell is not None:
            cells[col["checker"]] = checker_cell
        if "date" in col and status != "not started":
            cells[col["date"]] = today
        lines[i] = "| " + " | ".join(cells) + " |"

    if a.skip_optional:
        require_named(text, a.by, "a skip")
        keep = {s.strip().lower() for s in a.keep.split(",") if s.strip()}
        for i, cells in rows:
            key = k.step_key(cells[col["step"]])
            if key in optional and key not in keep and cells[col["status"]].lower() == "not started":
                reason = optional[key]["skip_reason"]
                set_row(i, cells, "skipped", f"skipped: {reason}")
                sp.pop(key, None)
                log_lines.append(f"| {today} | {title.lower()} | Step {cells[col['step']].split(' ')[0]} skipped (optional): {reason} | - | {a.by.strip()} | Run it: {optional[key].get('run_when', 'run the step')} |")
                done_msgs.append(f"{title} step {cells[col['step']].split(' ')[0]}: skipped ({reason})")
        if not done_msgs:
            print(f"No optional {title} step is waiting to start; nothing skipped.")
    else:
        hit = find_row(col, rows, a.step)
        if not hit:
            sys.exit(f"ERROR: step '{a.step}' not found in the {title} tracker")
        i, cells = hit
        key = k.step_key(cells[col["step"]])
        checker_cell = None
        if a.status == "passed":
            require_named(text, a.checker, "a pass")
            checker_cell = a.checker.strip()
        elif a.status == "skipped":
            require_named(text, a.by, "a skip")
            reason = a.reason.strip() or (optional.get(key, {}).get("skip_reason", "") if key in optional else "")
            if key not in optional:
                if not (a.override and a.reason.strip()):
                    sys.exit(f"REFUSED: {title} step {a.step} is not optional. Skipping it needs --reason and --override, "
                             f"and is logged as an override decided by {a.by}. Optional steps: {', '.join(optional) or 'none'}.")
            checker_cell = f"skipped: {reason}"
            kind = "optional" if key in optional else "OVERRIDE, not an optional step"
            log_lines.append(f"| {today} | {title.lower()} | Step {a.step} skipped ({kind}): {reason} | - | {a.by.strip()} | Run the step |")
        elif a.status == "in check":
            if a.waiting_on:
                require_named(text, a.waiting_on, "the checker")
            checker_cell = f"waiting: {a.waiting_on.strip()}" if a.waiting_on else None
        elif a.status == "not started":
            checker_cell = ""
        set_row(i, cells, a.status, checker_cell)

        if a.status in ("passed", "skipped", "not started"):
            sp.pop(key, None)
        else:
            rec = sp.setdefault(key, {})
            rec["status"] = a.status
            rec["updated"] = datetime.datetime.now().isoformat(timespec="minutes")
            if a.note:
                rec["note"] = a.note.strip()
            if a.waiting_on:
                rec["waiting_on"] = a.waiting_on.strip()
        done_msgs.append(f"{title} step {a.step}: {a.status}"
                         + (f" (checker {a.checker})" if a.status == "passed" else "")
                         + (f" (waiting on {a.waiting_on})" if a.waiting_on else "")
                         + (f" — {a.note}" if a.note else ""))

    rm.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    k.save_progress(eng, progress)
    if log_lines:
        with (eng / "05-decisions-log.md").open("a", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n")
    print("\n".join(done_msgs))

    r = subprocess.run([sys.executable, "-I", str(Path(__file__).with_name("route.py")), "--engagement", str(eng)],
                       capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    print("\n".join(l for l in out if l.startswith(("Next step", "ACTION", "Progress", "Waiting"))) if out else r.stderr.strip())


if __name__ == "__main__":
    main()
