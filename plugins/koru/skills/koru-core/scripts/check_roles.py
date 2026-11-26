#!/usr/bin/env python3
"""Roles gate: fail unless every owner the active stages require is named in 00-read-me-first.md.

Usage: python check_roles.py <engagement-folder>

Required roles = union of `required_roles` of the stages in .koru/stages.json (or Frame's set if the
engagement has no .koru, i.e. an older Frame-only engagement), plus the client lines "Decision makers"
and "Review rhythm". A blank cell, TODO or placeholder counts as missing.
Exit 0 = all named, 1 = something missing. Run it at the start of every session and before every step.
Also warns when the same person is both runner (Researcher) and checker, or shares a name with another owner.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import CORE, load_json, table_rows  # noqa: E402

FRAME_DEFAULT = ["Researcher", "Research owner", "Senior", "Developer", "Second-person checker pool"]


def empty(v):
    v = v.strip().strip("*").strip()
    return v == "" or v.upper().startswith("TODO") or v in ("-", "n/a", "tbc", "TBC") or bool(re.fullmatch(r"<[^>]*>", v))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    eng = Path(sys.argv[1]).expanduser()
    f = eng / "00-read-me-first.md"
    if not f.is_file():
        sys.exit(f"ERROR: {f} not found")
    reg = load_json(CORE / "registry" / "roles.json")
    aliases = reg.get("aliases", {})
    stages = load_json(eng / ".koru" / "stages.json", None)
    required = []
    if stages and stages.get("stages"):
        for s in stages["stages"].values():
            for r in s.get("required_roles", []):
                r = aliases.get(r, r)
                if r not in required:
                    required.append(r)
    else:
        required = list(FRAME_DEFAULT)
    text = f.read_text(encoding="utf-8")
    roles = {}
    for cells in table_rows(text, r"^## Roles"):
        if len(cells) >= 2 and cells[0] not in ("Role", ""):
            roles[cells[0]] = cells[1]
    missing = []
    for r in required:
        if r not in roles or empty(roles[r]):
            missing.append(f"role: {r}")
    for c in reg.get("client_lines", []):
        mm = re.search(rf"^-[ \t]*{re.escape(c)}:[ \t]*(.*)$", text, re.M | re.I)
        if not mm or empty(mm.group(1)):
            missing.append(f"client: {c}")
    if missing:
        print("ROLES GATE: not all owners are named. Do not start or continue any step until these are filled in 00-read-me-first.md:")
        for x in missing:
            print("  -", x)
        sys.exit(1)
    print("Roles gate passed: all owners are named.")
    for r in required:
        print(f"  {r}: {roles[r]}")
    names = lambda v: {x.strip().lower() for x in re.split(r"[,/&]| and ", v) if x.strip()}
    if "Researcher" in roles and "Research owner" in roles:
        same = names(roles["Researcher"]) & names(roles["Research owner"])
        if same:
            print(f"WARNING: researcher and research owner include the same name ({', '.join(sorted(same))}). If this is one person, the research owner's checks of steps the researcher ran must go to the second-person checker. If they are two people who share a name, record a distinguishing surname or initial.")
    if "Researcher" in roles and "Second-person checker pool" in roles:
        clash = names(roles["Researcher"]) & names(roles["Second-person checker pool"])
        if clash:
            print(f"WARNING: the researcher is also in the checker pool ({', '.join(sorted(clash))}). The checker can never be the person who ran the step.")


if __name__ == "__main__":
    main()
