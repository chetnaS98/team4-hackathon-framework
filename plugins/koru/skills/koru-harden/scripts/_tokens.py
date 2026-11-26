"""Shared reader for the Harden tokens artefact (used by contrast_check.py and export_tokens.py)."""
import re
from pathlib import Path

SECTIONS = ("Colour", "Type", "Spacing", "Radius")


def _strip_front(text):
    m = re.match(r"^---\n.*?\n---\n?", text, re.S)
    return text[m.end():] if m else text


def _rows(lines):
    out, on = [], False
    for l in lines:
        s = l.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if set(s) <= set("|-: "):
                continue
            if not on:
                on = True  # header row
                continue
            out.append(cells)
        elif on:
            break
    return out


def read_tokens(path):
    """Return ({section: [(name, value, use)]}, [(fg, bg, use)])."""
    body = _strip_front(Path(path).read_text(encoding="utf-8")).splitlines()
    heads = {l.strip()[3:].strip(): i for i, l in enumerate(body) if l.strip().startswith("## ")}
    toks = {}
    for s in SECTIONS:
        if s in heads:
            toks[s] = [(r[0], r[1], r[2] if len(r) > 2 else "") for r in _rows(body[heads[s] + 1:])
                       if r and r[0] and not r[0].startswith("<")]
    pairs = []
    if "Contrast pairs" in heads:
        pairs = [(r[0], r[1], r[2] if len(r) > 2 else "") for r in _rows(body[heads["Contrast pairs"] + 1:])
                 if len(r) >= 2 and not r[0].startswith("<")]
    return toks, pairs
