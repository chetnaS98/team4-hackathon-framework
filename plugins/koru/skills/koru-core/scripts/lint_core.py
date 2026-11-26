#!/usr/bin/env python3
"""Core lint for derived artefacts (every phase). Phase-only checks stay with the phase skill.

Usage:
  python lint_core.py <file-or-folder> [...] [--engagement <folder>] [--client-name NAME ...]

Checks, per .md or .html file that has a `type:` in its front matter (HTML artefacts carry the front matter in a leading <!-- --> comment):
  - required front matter: title, description, type, stage, status, version, last_checked, owner
  - the file name matches [project]-[stage]-[artefact]-v[n]-[status]; stage, version and status agree with the front matter
  - the type is registered for the stage (reads <engagement>/.koru/types.json, or --engagement's parent search)
  - derives_from entries look like name-vN
  - client names (--client-name) do not appear in the body (src pointers and [[links]] are not checked)
  - no TODO or <placeholder> text when status is review or final
Older files with no `stage` field are accepted with a warning (stage taken from the file name).
Exit 1 if there are errors.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FILE_RE, STAGES, STATUSES, front, in_code_folder, load_json  # noqa: E402

REQUIRED = ["title", "description", "type", "stage", "status", "version", "last_checked", "owner"]
DERIVES = re.compile(r"^[a-z0-9][a-z0-9_-]*[-_]v\d+$")  # artefact or source name ending -vN or _vN, no status suffix


def find_types(start):
    p = Path(start).resolve()
    for d in [p] + list(p.parents):
        t = d / ".koru" / "types.json"
        if t.is_file():
            return load_json(t, {})
    return None


def lint(path, types, client_names):
    errors, warns = [], []
    text = Path(path).read_text(encoding="utf-8")
    fm, body, _ = front(text)
    if "type" not in fm:
        return None
    stem = Path(path).stem
    m = FILE_RE.match(stem)
    for k in REQUIRED:
        if k not in fm:
            if k == "stage" and m:
                warns.append(f"{path}: no 'stage' field; taking '{m.group('stage')}' from the file name (add it)")
            else:
                errors.append(f"{path}: missing front matter field '{k}'")
    stage = fm.get("stage") or (m.group("stage") if m else None)
    if not m:
        errors.append(f"{path}: file name does not match [project]-[stage]-[artefact]-v[n]-[status]")
    else:
        if stage and m.group("stage") != stage:
            errors.append(f"{path}: stage in name '{m.group('stage')}' != front matter '{stage}'")
        if fm.get("status") and m.group("status") != fm["status"]:
            errors.append(f"{path}: status in name '{m.group('status')}' != front matter '{fm['status']}'")
        if fm.get("version") and str(m.group("ver")) != str(fm["version"]):
            errors.append(f"{path}: version in name v{m.group('ver')} != front matter {fm['version']}")
    if stage and stage not in STAGES:
        errors.append(f"{path}: stage '{stage}' is not one of {', '.join(STAGES)}")
    if fm.get("status") and fm["status"] not in STATUSES:
        errors.append(f"{path}: status '{fm['status']}' not in {', '.join(STATUSES)}")
    if types is not None and stage:
        allowed = types.get(stage)
        if allowed is None:
            warns.append(f"{path}: stage '{stage}' has no registered types (run init_stage.py)")
        elif fm.get("type") not in allowed:
            errors.append(f"{path}: type '{fm.get('type')}' is not registered for stage '{stage}' ({', '.join(allowed)})")
    df = fm.get("derives_from", [])
    if isinstance(df, str):
        df = [df] if df else []
    for d in df:
        if not DERIVES.match(d):
            errors.append(f"{path}: derives_from entry '{d}' should be an artefact name ending -vN (no status suffix)")
    in_code = False
    for i, line in enumerate(body.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        visible = re.sub(r"\bsrc:.*$", "", line)
        visible = re.sub(r"\[\[[^\]]*\]\]", "", visible)
        for n in client_names:
            if re.search(r"\b" + re.escape(n) + r"\b", visible, re.I):
                errors.append(f"{path}:{i}: client name '{n}' appears in a derived artefact (use the role or 'the client')")
    placeholder = r"\bTODO\b" if str(path).endswith(".html") else r"\bTODO\b|<[A-Za-z][^>\n]{2,}>"
    if fm.get("status") in ("review", "final") and re.search(placeholder, body):
        errors.append(f"{path}: status is {fm['status']} but TODO or <placeholder> text remains")
    return errors, warns


def collect(paths):
    out = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            out += sorted(x for x in list(p.rglob("*.md")) + list(p.rglob("*.html"))
                          if "templates" not in x.parts and "superseded" not in x.parts and "sources" not in x.parts
                          and not in_code_folder(x))
        elif p.is_file():
            out.append(p)
        else:
            print(f"WARN: {p} not found", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--engagement", help="engagement folder (to find .koru/types.json)")
    ap.add_argument("--client-name", action="append", default=[])
    a = ap.parse_args()
    types = find_types(a.engagement or a.paths[0])
    bad = checked = 0
    for f in collect(a.paths):
        r = lint(f, types, a.client_name)
        if r is None:
            continue
        e, w = r
        checked += 1
        for x in e:
            print("ERROR", x)
        for x in w:
            print("warn ", x)
        bad += len(e)
        print(f"[{'FAIL' if e else 'ok'}] {f}")
    print(f"Checked {checked} derived artefacts; {bad} errors.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
