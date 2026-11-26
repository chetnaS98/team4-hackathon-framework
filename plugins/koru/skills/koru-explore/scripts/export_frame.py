#!/usr/bin/env python3
"""Build Explore's input (the "frame.md" of the source skill) from Frame's FINAL artefacts.

Usage:
  python export_frame.py --engagement <project-folder> [--dry-run]

Reads every `final` Markdown artefact in 01-framed-brief/ and 02-research/ (newest final version of each),
and writes stages/explore/sources/<project>-frame-export-v<n>.md with front matter whose `derives_from`
lists each final it used. The export is generated, never hand-edited, and never overwritten:
  - if the newest export already lists exactly the same finals, nothing is written;
  - otherwise the next version is written, and the stale-check flags every Explore artefact built on the old one.
Refuses (exit 1) when there is no final brief in 01-framed-brief/: Explore never starts from a draft.
Prints the read-me's "Design system" line so the skill can confirm the path.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

FINAL_RE = re.compile(r"^(?P<project>[a-z][a-z0-9]*)-frame-(?P<artefact>[a-z0-9]+(?:-[a-z0-9]+)*)-v(?P<ver>\d+)-final$")
EXPORT_RE = re.compile(r"-frame-export-v(\d+)$")
FOLDERS = ("01-framed-brief", "02-research")
ORDER = ["brief", "research-pack", "persona", "jtbd", "workflow", "competitive-scan", "insight", "opportunity"]


def front(text):
    """(front matter dict, body). Same reading as koru-core's _common.front, Markdown only."""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            v = re.sub(r"\s+#.*$", "", v).strip().strip('"')
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            fm[k.strip()] = v
    return fm, text[m.end():]


def collect(eng):
    """Newest final version of each Frame artefact family in the final folders."""
    best = {}
    for folder in FOLDERS:
        d = eng / folder
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            if "superseded" in p.parts:
                continue
            m = FINAL_RE.match(p.stem)
            if not m:
                continue
            fm, body = front(p.read_text(encoding="utf-8"))
            if fm.get("status") != "final":
                print(f"warn  {p.name}: name says final but front matter status is '{fm.get('status')}'; skipped")
                continue
            fam = f"{m.group('project')}-frame-{m.group('artefact')}"
            ver = int(m.group("ver"))
            if fam not in best or ver > best[fam]["ver"]:
                best[fam] = {"ver": ver, "path": p, "folder": folder, "fm": fm, "body": body.strip(),
                             "type": fm.get("type", ""), "name": f"{fam}-v{ver}"}
    return sorted(best.values(), key=lambda x: (ORDER.index(x["type"]) if x["type"] in ORDER else len(ORDER), x["name"]))


def design_system_line(eng):
    text = (eng / "00-read-me-first.md").read_text(encoding="utf-8")
    m = re.search(r"^\*\*Design system:\*\*\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--dry-run", action="store_true", help="say what would be written, write nothing")
    a = ap.parse_args()

    eng = Path(a.engagement).expanduser()
    pj = eng / ".koru" / "project.json"
    if not (eng / "00-read-me-first.md").is_file() or not pj.is_file():
        print(f"ERROR: {eng} is not a koru engagement (no 00-read-me-first.md and .koru/project.json)")
        sys.exit(1)
    project = json.loads(pj.read_text(encoding="utf-8"))["project"]

    finals = [f for f in collect(eng) if f["name"].startswith(project + "-")]
    if not any(f["type"] == "brief" and f["folder"] == "01-framed-brief" for f in finals):
        print("REFUSED: there is no final framed brief in 01-framed-brief/.")
        print("Explore starts only from Frame's final brief and research pack. Finish Frame's sign-off first,")
        print("or, with no engagement, share frame.md by hand as the Explore skill describes.")
        sys.exit(1)
    if not any(f["type"] == "research-pack" for f in finals):
        print("warn  no final research pack in 02-research/; the export holds the brief only. Say so to the designer.")

    out_dir = eng / "stages" / "explore" / "sources"
    used = [f["name"] for f in finals]
    versions = []
    for p in out_dir.glob(f"{project}-frame-export-v*.md") if out_dir.is_dir() else []:
        m = EXPORT_RE.search(p.stem)
        if m:
            versions.append((int(m.group(1)), p))
    if versions:
        last_v, last_p = max(versions)
        last_fm, _ = front(last_p.read_text(encoding="utf-8"))
        prev = last_fm.get("derives_from", [])
        prev = [prev] if isinstance(prev, str) else prev
        if sorted(prev) == sorted(used):
            print(f"Up to date: {last_p.name} already uses the same finals. Nothing written.")
            ds = design_system_line(eng)
            print(f"Design system (read-me): {ds if ds else 'line not found'}")
            sys.exit(0)
        version = last_v + 1
    else:
        version = 1

    name = f"{project}-frame-export-v{version}"
    today = datetime.date.today().isoformat()
    lines = [
        "---",
        f'title: "{project} | Frame | Export for Explore | v{version}"',
        f'description: "Generated by koru-explore/scripts/export_frame.py from the final Frame artefacts listed in derives_from. Explore reads this in place of frame.md. Never edit it by hand; re-run the script."',
        "type: source",
        "stage: frame",
        "status: final",
        f"version: {version}",
        f"last_checked: {today}",
        "owner: export_frame.py",
        f"derives_from: [{', '.join(used)}]",
        "---",
        "",
        f"# {project} | Frame export for Explore | v{version}",
        "",
        "Generated, not written. Do not edit: re-run `export_frame.py` after any Frame final changes.",
        "",
        "## Contents",
        "",
        "| Artefact | Type | Folder |",
        "| --- | --- | --- |",
    ]
    lines += [f"| {f['name']} | {f['type']} | {f['folder']} |" for f in finals]
    for f in finals:
        lines += ["", "---", "", f"## From {f['name']}", "", f["body"]]
    text = "\n".join(lines).rstrip("\n") + "\n"

    if a.dry_run:
        print(f"Would write {out_dir / (name + '.md')} from {len(finals)} finals: {', '.join(used)}")
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / f"{name}.md"
        if target.exists():
            print(f"ERROR: {target} exists; not overwriting.")
            sys.exit(1)
        target.write_text(text, encoding="utf-8")
        print(f"Wrote {target} from {len(finals)} finals: {', '.join(used)}")
        if version > 1:
            print("A new export version: run the stale-check; Explore artefacts built on the old export are now flagged.")
    ds = design_system_line(eng)
    print(f"Design system (read-me): {ds if ds else 'line not found'}")


if __name__ == "__main__":
    main()
