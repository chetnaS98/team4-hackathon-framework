#!/usr/bin/env python3
"""WCAG contrast check for the Harden tokens artefact (H8, H11).

Usage:
  python contrast_check.py <tokens-artefact.md>          check every row in "## Contrast pairs"
  python contrast_check.py --pair "#767676" "#ffffff"    check one pair

Thresholds (WCAG 2.2 AA): 4.5:1 for normal text; 3:1 for large text and for UI components and
graphics. A pair counts as large text or UI when its Use says "large", "heading", "icon", "border",
"focus", "control" or "UI". Prints a Markdown table to paste into the accessibility artefact.
Exit 1 if any pair fails.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tokens import read_tokens  # noqa: E402

LOOSE = re.compile(r"\b(large|heading|icon|border|focus|control|ui)\b", re.I)


def lum(hexv):
    h = hexv.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tokens", nargs="?")
    ap.add_argument("--pair", nargs=2, metavar=("FG", "BG"))
    a = ap.parse_args()
    rows = []
    if a.pair:
        rows.append((a.pair[0], a.pair[1], a.pair[0], a.pair[1], "text"))
    elif a.tokens:
        toks, pairs = read_tokens(a.tokens)
        colours = {n: v for n, v, _ in toks.get("Colour", [])}
        if not pairs:
            sys.exit("ERROR: no rows under '## Contrast pairs'")
        for fg, bg, use in pairs:
            if fg not in colours or bg not in colours:
                print(f"ERROR: pair {fg} on {bg}: unknown colour token")
                continue
            rows.append((fg, bg, colours[fg], colours[bg], use))
    else:
        ap.error("give a tokens file or --pair")
    fails = 0
    print("| Foreground | Background | Use | Ratio | Needs | Result |")
    print("| --- | --- | --- | --- | --- | --- |")
    for fg, bg, fv, bv, use in rows:
        try:
            r = ratio(fv, bv)
        except ValueError:
            print(f"| {fg} | {bg} | {use} | invalid colour | | Fail |")
            fails += 1
            continue
        need = 3.0 if LOOSE.search(use or "") else 4.5
        ok = r >= need
        fails += not ok
        print(f"| {fg} ({fv}) | {bg} ({bv}) | {use} | {r:.2f}:1 | {need}:1 | {'Pass' if ok else 'Fail'} |")
    print(f"\n{len(rows)} pairs checked; {fails} fail.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
