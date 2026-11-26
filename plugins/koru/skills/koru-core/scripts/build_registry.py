#!/usr/bin/env python3
"""Rebuild artefact-registry.md from the front matter of every derived artefact.

Usage: python build_registry.py --engagement <project-folder>

Columns: Artefact | Stage | Type | Version | Status | Home | External link | Pointer | Signer | Derives from.
File artefacts are filled from front matter (Home = project knowledge when in a numbered final folder,
else drafts). Manual columns (External link, Pointer, Signer) are kept for rows that already exist.
Rows whose Artefact matches no file (a Figma frame, a ticket) are kept exactly as written.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FILE_RE, front, table_rows  # noqa: E402

COLS = ["Artefact", "Stage", "Type", "Version", "Status", "Home", "External link", "Pointer", "Signer", "Derives from"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    a = ap.parse_args()
    eng = Path(a.engagement).expanduser()
    reg = eng / "artefact-registry.md"
    existing = {}
    head = ""
    if reg.is_file():
        text = reg.read_text(encoding="utf-8")
        head = text.split("| Artefact")[0].rstrip("\n")
        for cells in table_rows(text):
            if cells and cells[0] != "Artefact" and len(cells) >= len(COLS):
                existing[cells[0]] = dict(zip(COLS, cells))
    if not head:
        head = "# Artefact registry"
    rows, seen = {}, set()
    for p in sorted(list(eng.rglob("*.md")) + list(eng.rglob("*.html"))):
        if "templates" in p.parts or "superseded" in p.parts or "sources" in p.parts or p.name.startswith(("00-", "05-")):
            continue
        fm, _, _ = front(p.read_text(encoding="utf-8"))
        if "type" not in fm:
            continue
        stem = p.stem
        m = FILE_RE.match(stem)
        name = re.sub(r"-(draft|review|final)$", "", stem)
        status = fm.get("status") or (m.group("status") if m else "draft")
        stage = fm.get("stage") or (m.group("stage") if m else "")
        in_final = len(p.relative_to(eng).parts) > 1 and re.match(r"^\d\d-", p.relative_to(eng).parts[0]) is not None
        df = fm.get("derives_from", [])
        df = ", ".join(df) if isinstance(df, list) else df
        old = existing.get(name, {})
        rows[name] = {"Artefact": name, "Stage": stage, "Type": fm.get("type", ""), "Version": str(fm.get("version", "")),
                      "Status": status, "Home": "project knowledge" if in_final else "drafts",
                      "External link": fm.get("external_url", old.get("External link", "")), "Pointer": old.get("Pointer", ""),
                      "Signer": old.get("Signer", ""), "Derives from": df or old.get("Derives from", "")}
        seen.add(name)
    for n, r in existing.items():
        if n not in seen and n not in rows:
            rows[n] = r
    out = [head, "", "| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS)]
    for n in sorted(rows, key=lambda k: (rows[k]["Stage"], k)):
        out.append("| " + " | ".join(rows[n].get(c, "") for c in COLS) + " |")
    reg.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {reg} ({len(rows)} artefacts)")


if __name__ == "__main__":
    main()
