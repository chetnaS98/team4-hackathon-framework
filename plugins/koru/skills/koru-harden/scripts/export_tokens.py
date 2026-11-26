#!/usr/bin/env python3
"""Write tokens.css and tokens.json from the Harden tokens artefact (H11).

Usage:
  python export_tokens.py <tokens-artefact.md> [--out <folder>]

Reads the Colour, Type, Spacing and Radius tables and writes, into --out (default: the artefact's
folder):
  tokens.css   :root { --<token>: <value>; ... } for Claude's HTML screens
  tokens.json  {"colour": {...}, "type": {...}, "spacing": {...}, "radius": {...}} for Figma variables
Both files carry a header naming the artefact and version they were generated from. They are
generated, never hand-edited: change the tokens artefact (a new version) and run this again.
Refuses to write if a value is empty or still a placeholder.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tokens import read_tokens  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tokens")
    ap.add_argument("--out")
    a = ap.parse_args()
    src = Path(a.tokens)
    stem = re.sub(r"-(draft|review|final)$", "", src.stem)
    toks, _ = read_tokens(src)
    if not any(toks.values()):
        sys.exit("ERROR: no tokens found (expected ## Colour, ## Type, ## Spacing, ## Radius tables)")
    bad = [(n, v) for rows in toks.values() for n, v, _ in rows if not v or v.startswith("<") or "TODO" in v]
    if bad:
        sys.exit("ERROR: placeholder or empty values: " + ", ".join(n for n, _ in bad))
    out = Path(a.out) if a.out else src.parent
    out.mkdir(parents=True, exist_ok=True)
    css = [f"/* Generated from {stem} by koru-harden/scripts/export_tokens.py. Do not edit by hand. */", ":root {"]
    data = {"_generated_from": stem}
    for sec, rows in toks.items():
        css.append(f"  /* {sec} */")
        data[sec.lower()] = {}
        for n, v, use in rows:
            css.append(f"  --{n}: {v};")
            data[sec.lower()][n] = {"value": v, "use": use}
    css.append("}")
    (out / "tokens.css").write_text("\n".join(css) + "\n", encoding="utf-8")
    (out / "tokens.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    n = sum(len(r) for r in toks.values())
    print(f"Wrote {n} tokens to {out / 'tokens.css'} and {out / 'tokens.json'} (from {stem})")


if __name__ == "__main__":
    main()
