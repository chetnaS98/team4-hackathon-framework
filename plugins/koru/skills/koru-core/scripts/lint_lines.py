#!/usr/bin/env python3
"""Traceable-line lint for any phase (core's file protocol, "Traceable lines and pointers").

Core's other checks (front matter, naming, status, client names, leftover TODOs) are in lint_core.py;
run that first. A phase may add its own stricter checks after this one (for example Frame's lint_claims.py).

Usage:
  python lint_lines.py <file-or-folder> [...] [--count] [--must-cite NAME ...]

A traceable line is any line that carries a confidence tag (a table row counts as one line):
  - <assertion>. [high|medium|low] [(observed)|(data)] [(inferred)] src: <pointer>[; <pointer>]
  - <assertion>. [low] (inferred) src: none

Errors (exit 1):
  - more than one assertion on one line (one assertion per line)
  - a confidence that is not high, medium or low (for example [certain] before src:)
  - no `src:`, or an empty one
  - `(inferred)` on anything but [low]
  - [high] with fewer than two distinct sources and no (observed) or (data) tag; [high] with src: none
  - `src: none` under a heading that says "know" ("What we know", "Known pain points"), unless it says
    the thing is not known ("Unknowns", "Not yet known", "What we don't know")
Warnings: a file pointer with no `§section` (figma:, jira:, github: and url: pointers need none).

Folders are searched for .md files, skipping templates/ and superseded/, files starting 00- or 05-,
and the decisions log, AI quality log and handoff card. A file named on the command line is always
checked. Fenced code blocks are ignored.

--count       print the totals of high, medium and low lines across all files (for handoff cards).
--must-cite   fail if no `src:` pointer in the files checked cites NAME (repeatable; use it for every
              request source, so no source is skipped).

This is a drop-in for koru-frame's lint_claims.py (same checks, flags, output and exit codes), with one
extra error (a confidence word that is not high, medium or low) and one fix (`src: none` under an
"Unknowns" or "not yet known" heading is not an error).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import front  # noqa: E402

LEVELS = ("high", "medium", "low")
CONF = re.compile(r"\[(high|medium|low)\]", re.I)
LINE = re.compile(r"^\s*(?:[-*]\s+)?(?P<text>.*?)\s*\[(?P<conf>high|medium|low)\](?P<tags>(?:\s*\((?:inferred|observed|data)\))*)\s*(?P<rest>.*)$", re.I)
BAD_CONF = re.compile(r"\[(?P<word>[A-Za-z][A-Za-z ]{1,20})\]\s*(?:\((?:inferred|observed|data)\)\s*)*src:", re.I)
SRC = re.compile(r"\bsrc:\s*(?P<src>.*)$")
NON_FILE = re.compile(r"^(figma|jira|github|url):", re.I)
NOT_KNOWN = re.compile(r"unknown|not (yet )?known|don't know|do not know")
SKIP_DIRS = {"templates", "superseded"}
SKIP_NAMES = ("ai-quality-log.md", "decisions-log.md", "handoff-card.md")
SKIP_PREFIXES = ("00-", "05-")


def check_unit(u, heading):
    """Return (errors, warnings, level or None) for one line or cell."""
    errs, warns = [], []
    bad = BAD_CONF.search(u)
    if bad and bad.group("word").lower() not in LEVELS:
        errs.append(f"confidence '[{bad.group('word')}]' must be [high], [medium] or [low]")
        return errs, warns, None
    if not CONF.search(u):
        return errs, warns, None
    if len(CONF.findall(u)) > 1:
        errs.append("more than one assertion on a line; one assertion per line")
        return errs, warns, None
    m = LINE.match(u)
    if not m:
        return errs, warns, None
    conf = m.group("conf").lower()
    tags = m.group("tags").lower()
    s = SRC.search(m.group("rest"))
    if not s or not s.group("src").strip():
        errs.append("assertion has no 'src:' (use 'src: none' and add it to the assumptions register)")
        return errs, warns, conf
    srcs = [x.strip() for x in s.group("src").strip().split(";") if x.strip()]
    is_none = len(srcs) == 1 and srcs[0].lower() == "none"
    if "(inferred)" in tags and conf != "low":
        errs.append(f"(inferred) is only allowed on [low], found [{conf}]")
    if conf == "high":
        if is_none:
            errs.append("[high] with src: none")
        else:
            names = {re.split(r"\s*§", x)[0].strip() for x in srcs}
            if len(names) < 2 and "(observed)" not in tags and "(data)" not in tags:
                errs.append("[high] needs two distinct sources, or an (observed) or (data) tag")
    if is_none and "know" in heading and not NOT_KNOWN.search(heading):
        errs.append(f"'src: none' under '{heading}'; an assumption is not something known (move it to the assumptions section or register)")
    if not is_none:
        for x in srcs:
            if "§" not in x and not NON_FILE.match(x):
                warns.append(f"source '{x}' has no §section")
    return errs, warns, conf


def lint(path):
    text = Path(path).read_text(encoding="utf-8")
    _, body, offset = front(text)
    errors, warns, counts = [], [], {k: 0 for k in LEVELS}
    heading, in_code = "", False
    for i, line in enumerate(body.splitlines(), 1 + offset):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("#"):
            heading = line.lstrip("#").strip().lower()
        e, w, conf = check_unit(line, heading)
        if conf:
            counts[conf] += 1
        errors += [f"{path}:{i}: {x}" for x in e]
        warns += [f"{path}:{i}: {x}" for x in w]
    return errors, warns, counts


def collect(paths):
    out = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            out += sorted(x for x in p.rglob("*.md")
                          if not x.name.startswith(SKIP_PREFIXES) and x.name not in SKIP_NAMES
                          and not (SKIP_DIRS & set(x.parts)))
        elif p.is_file():
            out.append(p)
        else:
            print(f"WARN: {p} not found", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--count", action="store_true", help="print high, medium and low totals across all files")
    ap.add_argument("--must-cite", action="append", default=[], help="source name that at least one src: pointer must cite; repeatable")
    a = ap.parse_args()

    files = collect(a.paths)
    total = {k: 0 for k in LEVELS}
    bad = 0
    for f in files:
        e, w, c = lint(f)
        for k in total:
            total[k] += c[k]
        for x in e:
            print("ERROR", x)
        for x in w:
            print("warn ", x)
        bad += len(e)
        print(f"[{'FAIL' if e else 'ok'}] {f}  (high {c['high']}, medium {c['medium']}, low {c['low']})")
    if a.must_cite:
        alltext = "\n".join(Path(f).read_text(encoding="utf-8") for f in files)
        for n in a.must_cite:
            if not re.search(r"\bsrc:[^\n]*" + re.escape(n), alltext):
                print(f"ERROR source never cited: {n} (read it and use it, or say why it adds nothing)")
                bad += 1
    if a.count:
        print(f"TOTAL claims: high {total['high']}, medium {total['medium']}, low {total['low']}")
    print(f"Checked {len(files)} files; {bad} errors.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
