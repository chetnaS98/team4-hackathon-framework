#!/usr/bin/env python3
"""PreToolUse guard for Write, Edit and MultiEdit inside a koru engagement.

Blocks (exit 2, reason on stderr, shown to Claude):
  1. editing a source that already exists in stages/<stage>/sources/ (sources are never edited; add a new version)
  2. overwriting an existing file whose name ends in -final (make the next version instead)
  3. writing into a stage's final folder (for example 01-framed-brief/) unless the file name ends in -final
     AND the decisions log already records that name (the sign-off comes first)
Anything outside a koru engagement (no .koru/project.json above it) is ignored.
"""
import json
import sys
from pathlib import Path


def engagement_of(p):
    for d in [p.parent, *p.parent.parents]:
        if (d / ".koru" / "project.json").is_file() and (d / "00-read-me-first.md").is_file():
            return d
    return None


def final_folders(eng):
    try:
        stages = json.loads((eng / ".koru" / "stages.json").read_text(encoding="utf-8")).get("stages", {})
    except (OSError, ValueError):
        stages = {}
    out = set()
    for s in stages.values():
        out.update(s.get("final_folders", []))
    return out


def block(msg):
    print(f"Blocked by koru: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    fp = (data.get("tool_input") or {}).get("file_path")
    if not fp:
        return
    p = Path(fp).expanduser()
    if not p.is_absolute():
        p = Path(data.get("cwd") or ".").resolve() / p
    eng = engagement_of(p)
    if not eng:
        return
    rel = p.relative_to(eng)
    parts = rel.parts
    stem = p.stem

    if len(parts) >= 3 and parts[0] == "stages" and parts[2] == "sources" and p.exists():
        block(f"'{rel}' is a source. Sources are never edited. Save the change as a new version (for example _v2) and run the stale-check.")
    if stem.endswith("-final") and p.exists():
        block(f"'{p.name}' is final. Never overwrite a final: make the next version as a draft, get it checked and signed off.")
    if parts and parts[0] in final_folders(eng):
        if not stem.endswith("-final"):
            block(f"'{rel}' is in a final folder but isn't named -final. Drafts stay in stages/<stage>/drafts/.")
        log = eng / "05-decisions-log.md"
        if not log.is_file() or stem not in log.read_text(encoding="utf-8"):
            block(f"no sign-off for '{stem}' in 05-decisions-log.md. Record the named sign-off first, then move the file.")


if __name__ == "__main__":
    main()
