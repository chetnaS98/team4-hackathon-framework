#!/usr/bin/env python3
"""Deliver Ship tickets without Jira access: a Jira CSV import file, one combined Markdown file, and
optionally GitHub Issues.

Usage:
  python export_tickets.py --engagement <project> [--status final|review|draft|any] [--out <dir>]
                           [--format wiki|plain] [--issue-type Story] [--link-base <url>]
                           [--github owner/repo [--yes]]

Reads every ticket artefact (type: ticket, stage: ship) in the engagement, skipping templates/ and
superseded/, and takes the latest version of each ticket that has the chosen status (default final).
Writes into --out (default <project>/07-ship/export/ for final, <project>/stages/ship/export-preview/
otherwise):
  tickets.csv   Jira CSV import format: Summary, Issue Type, Priority, Description, Labels, Labels.
                Description is the full ticket body (every field after the title), in Jira wiki markup
                (--format plain keeps Markdown). Final tickets carry the labels koru and koru-final;
                others carry koru only. Jira reads each Labels column as one label.
  tickets.md    every ticket in one file, for pasting into any tool.
--link-base <url>: rewrite links to the deliverable (<name>.html#anchor) as <url>#anchor, so they work
  outside the engagement folder.
--github owner/repo: create one GitHub issue per ticket with `gh issue create`, labels koru and
  koru-final. Without --yes this is a DRY RUN: it prints each command and writes the bodies to
  <out>/github/. With --yes it creates the issues (final tickets only). It publishes outside the
  team: ask the user before passing --yes. If `gh auth status` fails, it says how to log in and the
  CSV stays the delivery.
Exit 0 on success, 1 when nothing was exported or a GitHub step failed.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _core_scripts():
    for c in (os.environ.get("KORU_CORE"), str(Path(__file__).resolve().parent.parent.parent / "koru-core")):
        if c and (Path(c) / "scripts" / "_common.py").is_file():
            return Path(c) / "scripts"
    sys.exit("ERROR: koru-core not found. Install it next to koru-ship or set KORU_CORE to its folder.")


sys.path.insert(0, str(_core_scripts()))
from _common import front, parse_name  # noqa: E402

PRIORITIES = {"highest": "Highest", "high": "High", "medium": "Medium", "low": "Low", "lowest": "Lowest"}


def find_tickets(eng, status):
    fams = {}
    for p in sorted(eng.rglob("*.md")):
        if {"templates", "superseded", "export", "export-preview"} & set(p.parts):
            continue
        fm, body, _ = front(p.read_text(encoding="utf-8"))
        if fm.get("type") != "ticket" or fm.get("stage", "ship") != "ship":
            continue
        fam, ver, _ = parse_name(p.stem)
        fams.setdefault(fam, []).append((int(fm.get("version") or ver), fm.get("status"), p, fm, body))
    chosen, notes = [], []
    for fam, vs in sorted(fams.items()):
        vs.sort(key=lambda x: x[0])
        pick = [v for v in vs if status == "any" or v[1] == status]
        if not pick:
            notes.append(f"skipped {fam}: no {status} version (latest is v{vs[-1][0]} {vs[-1][1]})")
            continue
        chosen.append(pick[-1])
        if pick[-1][0] < vs[-1][0]:
            notes.append(f"note {fam}: exporting v{pick[-1][0]} {pick[-1][1]}; a newer v{vs[-1][0]} {vs[-1][1]} exists")
    return chosen, notes


def split_ticket(body):
    """(summary, priority, description markdown) from the ticket body."""
    lines = body.splitlines()
    summary, priority, desc, in_title, started = "", "", [], False, False
    for l in lines:
        if l.startswith("# ") and not started:
            continue
        if l.startswith("## "):
            in_title = l[3:].strip().lower() == "title"
            started = True
            if in_title:
                continue
        if in_title:
            m = re.match(r"^\s*Priority:\s*(.*)$", l, re.I)
            if m:
                priority = PRIORITIES.get(m.group(1).strip().lower(), "")
            elif l.strip() and not summary:
                summary = l.strip()
            continue
        if started:
            desc.append(l)
    return summary, priority, "\n".join(desc).strip() + "\n"


def relink(text, base):
    if not base:
        return text
    return re.sub(r"\b[a-z][a-z0-9]*-ship-deliverable-v\d+(?:-(?:draft|review|final))?\.html(?=#|\b)", base, text)


def md_to_wiki(md):
    out, header_done = [], False
    for l in md.splitlines():
        if re.match(r"^\s*\|", l):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            sep = "|" if header_done else "||"
            out.append(sep + sep.join(cells) + sep)
            header_done = True
            continue
        header_done = False
        l = re.sub(r"\*\*(.+?)\*\*", r"*\1*", l)
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m:
            l = f"h{len(m.group(1))}. {m.group(2)}"
        m = re.match(r"^(\s*)[-*]\s+(.*)$", l)
        if m and not re.match(r"^\*[^*\s]", l):
            l = "*" * (len(m.group(1)) // 2 + 1) + " " + m.group(2)
        l = re.sub(r"`([^`]+)`", r"{{\1}}", l)
        l = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[\1|\2]", l)
        out.append(l)
    return "\n".join(out)


def gh_ok():
    if not shutil.which("gh"):
        return False, "The GitHub CLI (gh) is not installed. Install it (https://cli.github.com), run `gh auth login`, then run this again."
    r = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if r.returncode != 0:
        return False, ("The GitHub CLI is not logged in. Run `gh auth login` yourself (GitHub.com, HTTPS, log in with a "
                       "browser), check with `gh auth status`, then run this again.")
    return True, ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--status", default="final", choices=["final", "review", "draft", "any"])
    ap.add_argument("--out")
    ap.add_argument("--format", default="wiki", choices=["wiki", "plain"])
    ap.add_argument("--issue-type", default="Story")
    ap.add_argument("--link-base")
    ap.add_argument("--github", metavar="OWNER/REPO")
    ap.add_argument("--yes", action="store_true", help="really create GitHub issues (ask the user first)")
    a = ap.parse_args()

    eng = Path(a.engagement).expanduser().resolve()
    if not (eng / "00-read-me-first.md").is_file():
        sys.exit(f"ERROR: {eng} is not a koru engagement")
    tickets, notes = find_tickets(eng, a.status)
    for n in notes:
        print(n)
    if not tickets:
        print(f"No {a.status} tickets found. Nothing exported."
              + (" Tickets become final at S7, after the engineer's sign-off; use --status draft for a preview." if a.status == "final" else ""))
        sys.exit(1)
    try:
        it = int(json.loads((eng / ".koru" / "progress.json").read_text()).get("_iterations", {}).get("ship", 1))
    except (OSError, ValueError):
        it = 1
    out = Path(a.out) if a.out else (eng / "07-ship" / "export" / f"iteration-{it}" if a.status == "final"
                                     else eng / "stages" / "ship" / "export-preview" / f"iteration-{it}")
    out.mkdir(parents=True, exist_ok=True)

    rows, md_parts, gh_items = [], [], []
    for ver, st, path, fm, body in tickets:
        summary, priority, desc_md = split_ticket(body)
        desc_md = relink(desc_md, a.link_base)
        final = st == "final"
        stem = re.sub(r"-(draft|review|final)$", "", path.stem)
        note = f"Koru ticket: {stem} ({st}). The Markdown ticket is the source of truth.\n"
        footer = "\n***\n" + note  # never a bare '---' line: it would look like front matter to other tools
        desc = (md_to_wiki(desc_md) + "\n----\n" + note) if a.format == "wiki" else desc_md + footer
        rows.append([summary, a.issue_type, priority, desc, "koru", "koru-final" if final else ""])
        md_parts.append(f"## {summary}\n\n_{stem} · {st} · labels: koru{', koru-final' if final else ''}_\n\n{desc_md}")
        gh_items.append((summary, desc_md + footer, final, stem))

    with (out / "tickets.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Summary", "Issue Type", "Priority", "Description", "Labels", "Labels"])
        w.writerows(rows)
    head = (f"# Tickets ({a.status}), {len(rows)} in total\n\n"
            "Generated by koru-ship/scripts/export_tickets.py from the Markdown ticket artefacts. Do not edit; "
            "change the ticket (a new version) and export again.\n\n")
    (out / "tickets.md").write_text(head + "\n\n***\n\n".join(md_parts), encoding="utf-8")
    print(f"Exported {len(rows)} tickets ({a.status}):")
    for r in rows:
        print(f"  - {r[0]}  [labels: {r[4]}{', ' + r[5] if r[5] else ''}]")
    print(f"Wrote {out / 'tickets.csv'} (Jira CSV import) and {out / 'tickets.md'}")
    if a.status != "final":
        print("These are not final: they carry no koru-final label and are for preview only.")

    if not a.github:
        return
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", a.github):
        sys.exit(f"ERROR: --github needs owner/repo, got '{a.github}'")
    ok, msg = gh_ok()
    gdir = out / "github"
    gdir.mkdir(exist_ok=True)
    if not a.yes:
        print(f"\nDRY RUN: would create {len(gh_items)} GitHub issues in {a.github} (nothing is sent):")
        for i, (title, body, final, stem) in enumerate(gh_items, 1):
            bf = gdir / f"{stem}.md"
            bf.write_text(body, encoding="utf-8")
            labels = "--label koru" + (" --label koru-final" if final else "")
            print(f"  gh issue create --repo {a.github} --title {title!r} {labels} --body-file {bf}")
        if not ok:
            print("\n" + msg + "\nMeanwhile, deliver the CSV above.")
        print("\nTo create them, the user must say yes in chat; then run again with --yes.")
        return
    if a.status != "final" or not all(f for _, _, f, _ in gh_items):
        sys.exit("ERROR: --yes creates issues only from final tickets (the upload rule). Export with --status final.")
    if not ok:
        print(msg + "\nNothing was created. Deliver the CSV meanwhile.")
        sys.exit(1)
    for name, colour, d in (("koru", "5319e7", "Koru engagement"), ("koru-final", "0e8a16", "Koru: final, source of truth")):
        subprocess.run(["gh", "label", "create", name, "--repo", a.github, "--color", colour, "--description", d],
                       capture_output=True, text=True)  # already exists is fine
    failed = 0
    for title, body, final, stem in gh_items:
        bf = gdir / f"{stem}.md"
        bf.write_text(body, encoding="utf-8")
        r = subprocess.run(["gh", "issue", "create", "--repo", a.github, "--title", title, "--body-file", str(bf),
                            "--label", "koru", "--label", "koru-final"], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  created {stem}: {r.stdout.strip()}  (add a registry row with its github: pointer)")
        else:
            failed += 1
            print(f"  FAILED {stem}: {r.stderr.strip()}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
