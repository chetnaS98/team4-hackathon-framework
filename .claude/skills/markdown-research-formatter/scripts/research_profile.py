#!/usr/bin/env python3
"""Find, load and check the per-project research profile (research-profile.json).

Usage:
  python research_profile.py find  <start-dir>         # print the path of the nearest profile walking up, exit 1 if none
  python research_profile.py check <profile.json>      # validate a profile, print it as JSON
  python research_profile.py show  <start-dir>         # find + check + print

See references/profile.md for the fields. Other scripts import load_profile()/find_profile().
"""
import json
import re
import sys
from pathlib import Path

NAME = "research-profile.json"
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def find_profile(start):
    p = Path(start).expanduser().resolve()
    if p.is_file():
        p = p.parent
    for d in [p, *p.parents]:
        cand = d / NAME
        if cand.is_file():
            return cand
    return None


def check_profile(prof):
    """Return a list of error strings (empty = valid)."""
    errs = []
    if not isinstance(prof, dict):
        return ["profile must be a JSON object"]
    if prof.get("profile_version") != 1:
        errs.append("profile_version must be 1")
    if not isinstance(prof.get("project"), str) or not KEBAB.match(prof.get("project", "")):
        errs.append("project must be a kebab-case string")
    for key, required in (("products", True), ("lifecycle", False)):
        v = prof.get(key)
        if v is None:
            if required:
                errs.append(f"{key} is required (object of value -> description)")
            continue
        if not isinstance(v, dict) or not v:
            errs.append(f"{key} must be a non-empty object of value -> description")
            continue
        for k in v:
            if not KEBAB.match(k):
                errs.append(f"{key} value '{k}' must be lowercase kebab-case")
    for key in ("personas", "workflows", "search_keywords"):
        v = prof.get(key)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) for x in v)):
            errs.append(f"{key} must be a list of strings")
    for key in ("personas", "workflows"):
        for x in prof.get(key) or []:
            if isinstance(x, str) and not KEBAB.match(x):
                errs.append(f"{key} value '{x}' must be lowercase kebab-case")
    g = prof.get("glossary")
    if g is not None and (not isinstance(g, dict)
                          or not all(isinstance(v, list) for v in g.values())):
        errs.append("glossary must be an object of canonical name -> list of variants")
    return errs


def load_profile(path=None, start=None):
    """Load a profile from an explicit path, or by walking up from start. Returns (profile, path) or (None, None).
    Raises ValueError if the file exists but is invalid."""
    p = Path(path).expanduser() if path else (find_profile(start) if start else None)
    if not p:
        return None, None
    prof = json.loads(Path(p).read_text(encoding="utf-8"))
    errs = check_profile(prof)
    if errs:
        raise ValueError(f"{p}: " + "; ".join(errs))
    return prof, Path(p)


def main(argv):
    if len(argv) != 3 or argv[1] not in ("find", "check", "show"):
        print(__doc__)
        return 2
    cmd, arg = argv[1], argv[2]
    if cmd == "find":
        p = find_profile(arg)
        if not p:
            print(json.dumps({"found": False, "searched_from": str(Path(arg).resolve())}))
            return 1
        print(json.dumps({"found": True, "path": str(p)}))
        return 0
    p = Path(arg) if cmd == "check" else find_profile(arg)
    if not p or not p.is_file():
        print(json.dumps({"error": f"no profile found from {arg}"}))
        return 1
    try:
        prof = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as e:
        print(json.dumps({"error": f"{p} is not valid JSON: {e}"}))
        return 1
    errs = check_profile(prof)
    print(json.dumps({"path": str(p), "valid": not errs, "errors": errs, "profile": prof}, indent=2))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
