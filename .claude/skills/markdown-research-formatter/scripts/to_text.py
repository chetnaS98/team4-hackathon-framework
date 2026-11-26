#!/usr/bin/env python3
"""Extract ALL text from a source file to plain text/Markdown with nothing dropped, so it can be
passed to build_verbatim.py instead of being retyped.

Usage: python to_text.py <input> <output.txt>
  .xlsx/.xlsm  every sheet, every row (hidden too), one H2 per sheet, Markdown table
  .csv/.tsv    every row as a Markdown table
  .pptx        '## Slide N' + all text, tables, speaker notes
  .docx/.html/.epub  pandoc -> GFM   |  .pdf  pdftotext -layout
  .txt/.md/.vtt/.srt/other text      copied byte-for-byte
Only mechanical changes: '|' escaped as '\\|' and in-cell newlines as <br> inside tables.
"""
import csv
import subprocess
import sys
from pathlib import Path


def cell(v):
    s = "" if v is None else str(v)
    return s.replace("|", "\\|").replace("\r\n", "<br>").replace("\n", "<br>")


def table(rows):
    if not rows:
        return "(empty)\n"
    w = max(len(r) for r in rows)
    rows = [list(r) + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(cell(c) for c in rows[0]) + " |", "|" + "---|" * w]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(out) + "\n"


def xlsx(p):
    import openpyxl
    wb = openpyxl.load_workbook(p, data_only=True)
    parts = []
    for ws in wb.worksheets:
        for rng in list(ws.merged_cells.ranges):  # repeat merged values so no cell is blank
            v = ws.cell(rng.min_row, rng.min_col).value
            ws.unmerge_cells(str(rng))
            for r in ws.iter_rows(rng.min_row, rng.max_row, rng.min_col, rng.max_col):
                for c in r:
                    c.value = v
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        while rows and all(c is None for c in rows[-1]):
            rows.pop()
        parts.append(f"## {ws.title}\n\n{table(rows)}")
    return "\n".join(parts)


def delim(p, d):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return table(list(csv.reader(f, delimiter=d)))


def pptx(p):
    from pptx import Presentation
    parts = []
    for i, s in enumerate(Presentation(p).slides, 1):
        title = s.shapes.title.text if s.shapes.title is not None and s.shapes.title.has_text_frame else ""
        buf = [f"## Slide {i}: {title}".rstrip(": ")]
        for sh in s.shapes:
            if sh.has_text_frame and sh != s.shapes.title:
                buf += [l for l in sh.text_frame.text.split("\n") if l.strip()]
            if getattr(sh, "has_table", False) and sh.has_table:
                buf.append(table([[c.text for c in r.cells] for r in sh.table.rows]))
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
            buf.append("**Speaker notes:** " + s.notes_slide.notes_text_frame.text)
        parts.append("\n".join(buf) + "\n")
    return "\n".join(parts)


def main(a):
    if len(a) != 3:
        print(__doc__)
        return 2
    src, dst = Path(a[1]), Path(a[2])
    ext = src.suffix.lower()
    if ext in (".xlsx", ".xlsm"):
        dst.write_text(xlsx(src), encoding="utf-8")
    elif ext == ".csv":
        dst.write_text(delim(src, ","), encoding="utf-8")
    elif ext == ".tsv":
        dst.write_text(delim(src, "\t"), encoding="utf-8")
    elif ext == ".pptx":
        dst.write_text(pptx(src), encoding="utf-8")
    elif ext in (".docx", ".html", ".htm", ".epub"):
        subprocess.run(["pandoc", str(src), "-t", "gfm", "--wrap=none", "-o", str(dst)], check=True)
    elif ext == ".pdf":
        subprocess.run(["pdftotext", "-layout", str(src), str(dst)], check=True)
    else:
        dst.write_bytes(src.read_bytes())
    print(f"Wrote {dst} ({len(dst.read_text(encoding='utf-8').splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
