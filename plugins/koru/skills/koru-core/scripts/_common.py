"""Shared helpers for the koru-core scripts."""
import json
import re
from pathlib import Path

CORE = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^(?P<fam>.*?)[-_]v(?P<ver>\d+)(?:[-_](?P<st>draft|review|final))?$")
FILE_RE = re.compile(r"^(?P<project>[a-z][a-z0-9]*)-(?P<stage>[a-z]+)-(?P<artefact>[a-z0-9]+(?:-[a-z0-9]+)*)-v(?P<ver>\d+)-(?P<status>draft|review|final)$")
STATUSES = ("draft", "review", "final")
STAGES = ("frame", "explore", "harden", "ship")


def front(text):
    """Return (front matter dict, body, line offset). Handles inline lists [a, b]."""
    fm = {}
    m = re.match(r"^\s*<!--\s*\n---\n(.*?)\n---\s*\n-->\s*\n?", text, re.S)  # HTML artefacts: front matter inside a leading comment
    if not m:
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return fm, text, 0
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            v = re.sub(r"\s+#.*$", "", v).strip().strip('"')
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            fm[k.strip()] = v
    return fm, text[m.end():], text[:m.end()].count("\n")


def parse_name(stem):
    m = NAME_RE.match(stem)
    if m:
        return m.group("fam"), int(m.group("ver")), m.group("st")
    return stem, 1, None


def load_json(path, default=None):
    p = Path(path)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return default


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def table_rows(text, heading_re=None):
    """Return list of rows (list of cells) of the first markdown table (after an optional heading)."""
    lines = text.splitlines()
    start = 0
    if heading_re:
        for i, l in enumerate(lines):
            if re.match(heading_re, l):
                start = i
                break
    rows, in_table = [], False
    for l in lines[start:]:
        if l.strip().startswith("|"):
            in_table = True
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append(cells)
        elif in_table:
            break
    return rows
