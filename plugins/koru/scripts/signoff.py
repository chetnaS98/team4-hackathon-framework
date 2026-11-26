#!/usr/bin/env python3
"""Record a named sign-off and promote a draft (or review) artefact to final, in one checked step.

Usage:
  python signoff.py --engagement <folder> --file <path to the draft> --by "<name>" [--role "<role>"] [--dry-run]

Checks, then acts:
  1. the signer is named in the Roles table
  2. the stale-check reports nothing for this artefact's family (an artefact with open warnings can't be final)
  3. koru-core lint_core.py passes on the file
Then: logs "<name> signed off" in 05-decisions-log.md, writes a copy named ...-final with status: final into the
stage's final folder (the draft stays where it is, untouched), rebuilds the artefact registry, and prints what the
context keeper should now upload. Exit 1 if refused.

A code artefact (Ship's React starter) is a folder whose manifest shares its name:
<project>-ship-react-starter-v1-draft/<project>-ship-react-starter-v1-draft.md. Sign off by passing the manifest
as --file: the checks run on the manifest (plus no TODO left in the code), and the whole folder is copied to
<final folder>/<...-final>/, without node_modules/ and dist/, with the manifest renamed and set to final.
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

# which final folder each type goes to when a stage has more than one (a stage.json "final_homes" map overrides)
DEFAULT_HOMES = {
    "frame": {"brief": "01-framed-brief"},
    "harden": {"tokens": "04-design-library", "rulebook-chapter": "03-rulebook"},
}


def front(text):
    m = re.match(r"^(\s*<!--\s*\n)?---\n(.*?)\n---\s*\n(-->\s*\n?)?", text, re.S)
    fm = {}
    if m:
        for line in m.group(2).splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                a, b = line.split(":", 1)
                fm[a.strip()] = b.strip().strip('"')
    return fm


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--by", required=True)
    ap.add_argument("--role", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    core = k.core_dir()
    eng = Path(a.engagement).expanduser().resolve()
    src = Path(a.file).expanduser().resolve()
    if not k.is_engagement(eng) or not src.is_file():
        sys.exit("ERROR: need an engagement folder and an existing file")
    text = src.read_text(encoding="utf-8")
    fm = front(text)
    stage, typ = fm.get("stage"), fm.get("type")
    if not stage or not typ:
        sys.exit("ERROR: the file has no front matter with type and stage")
    m = re.match(r"^(?P<fam>.+)-v(?P<v>\d+)-(?P<st>draft|review|final)$", src.stem)
    if not m:
        sys.exit("ERROR: the file name doesn't follow [project]-[stage]-[artefact]-v[n]-[status]")
    if m.group("st") == "final":
        sys.exit("ERROR: this file is already final")
    fam, ver = m.group("fam"), m.group("v")
    final_stem = f"{fam}-v{ver}-final"

    problems = []
    readme = (eng / "00-read-me-first.md").read_text(encoding="utf-8")
    people = {n.strip().lower() for r in k.section_table(readme, "Roles") if len(r) > 1 for n in re.split(r"[,/&]| and ", r[1]) if n.strip()}
    if a.by.strip().lower() not in people:
        problems.append(f"'{a.by}' is not named in the Roles table")
    sc, stale = k.run_core(core, "stale_check.py", "--engagement", eng)
    if sc != 0 and re.search(rf"\b{re.escape(fam)}-v{ver}", stale):
        problems.append("the stale-check has open warnings on this artefact:\n      " + "\n      ".join(l for l in stale.splitlines() if fam in l)[:800])
    lc, lint = k.run_core(core, "lint_core.py", src, "--engagement", eng)
    if lc != 0:
        problems.append("lint_core.py failed:\n      " + "\n      ".join(lint.splitlines()[:8]))

    body = re.sub(r"^(\s*<!--\s*\n)?---\n.*?\n---\s*\n(-->\s*\n?)?", "", text, count=1, flags=re.S)
    left = re.findall(r"\bTODO\b|\bTBD\b", body) + ([] if src.suffix == ".html" else re.findall(r"<[a-z][^>\n]{1,60}>", body))
    code_dir = src.parent if src.parent.name == src.stem else None
    if code_dir:
        for p in code_dir.rglob("*"):
            if p.is_file() and not ({"node_modules", "dist"} & set(p.relative_to(code_dir).parts)) and p != src \
                    and p.suffix in (".ts", ".tsx", ".js", ".jsx", ".css", ".html", ".json", ".md"):
                if re.search(r"\bTODO\b", p.read_text(encoding="utf-8", errors="replace")):
                    left.append(f"TODO in {p.relative_to(code_dir)}")
    if re.search(r"^owner:\s*(TODO|$)", text, re.M):
        left.append("owner: TODO")
    if left:
        problems.append(f"the file still has {len(left)} placeholder(s) (e.g. {', '.join(sorted(set(left))[:3])}); a final carries none")
    stages = (k.load_json(eng / ".koru" / "stages.json", {}) or {}).get("stages", {})
    finals = (stages.get(stage) or {}).get("final_folders", [])
    if not finals:
        problems.append(f"stage '{stage}' has no final folders in .koru/stages.json")
    homes = dict(DEFAULT_HOMES.get(stage, {}))
    skill = k.find_skill((stages.get(stage) or {}).get("skill") or "")
    if skill:
        homes.update((k.load_json(skill / "stage.json", {}) or {}).get("final_homes", {}))
    home = homes.get(typ) or (finals[-1] if stage in ("frame", "harden") and len(finals) > 1 else (finals[0] if finals else ""))
    dest = eng / home / final_stem / (final_stem + src.suffix) if code_dir else eng / home / (final_stem + src.suffix)
    if code_dir and dest.parent.exists():
        problems.append(f"{dest.parent.relative_to(eng)} already exists (finals are never overwritten; make the next version)")
    if dest.exists():
        problems.append(f"{dest.relative_to(eng)} already exists (finals are never overwritten; make the next version)")

    print(f"Sign-off: {src.name} -> {dest.relative_to(eng) if home else '?'} by {a.by}")
    if problems:
        print("REFUSED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    if a.dry_run:
        print("All checks pass. Dry run: nothing written.")
        return

    today = datetime.date.today().isoformat()
    out = re.sub(r"^status:\s*\w+", "status: final", text, count=1, flags=re.M)
    out = re.sub(r"^last_checked:.*$", f"last_checked: {today}", out, count=1, flags=re.M)
    with (eng / "05-decisions-log.md").open("a", encoding="utf-8") as f:
        f.write(f"| {today} | {stage} | {final_stem} signed off{' as ' + a.role if a.role else ''} | {final_stem} | {a.by} | Another review round |\n")
    if code_dir:
        shutil.copytree(code_dir, dest.parent, ignore=shutil.ignore_patterns("node_modules", "dist", src.name))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    k.run_core(core, "build_registry.py", "--engagement", eng)
    print(f"Signed off and saved: {dest.relative_to(eng)}")
    print(f"Context keeper: upload {dest.name} to project knowledge. The draft stays in {src.parent.relative_to(eng)}.")


if __name__ == "__main__":
    main()
