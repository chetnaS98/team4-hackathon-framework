#!/usr/bin/env python3
"""Stale-check across stages: find artefacts built on something that has changed.

Usage: python stale_check.py --engagement <project-folder> [--kb <folder> ...]

Nodes: every derived artefact (front matter has `type:`) in the engagement; sources (Markdown and HTML)
in stages/*/sources/ and --kb folders; and rows of artefact-registry.md that match no file (Figma frames,
tickets...), with their version, status and `Derives from`.
Edges: `derives_from` in front matter, `src:` pointers on traceable lines, and [[name]] pinned links.
`reviews:` in front matter lists what an artefact audited or reviewed (an evidence audit of traces v1, a
critique of design v1). Those pointers must resolve, but a newer version of a reviewed file does not make the
review stale: the review is a record of that version, and is usually why the newer version exists.
Files in a `superseded/` folder are indexed so pointers to them resolve; they are never checked themselves.
Pointer forms: file names (with optional §section), and figma:/jira:/github:/url: pointers resolved through
the registry's Pointer column (an optional @vN pins a version).

Names that differ only in version (_v2, -v2, -v2-final) are one family. Rules:
  1. Stale if anything it derives from has a newer version.
  2. Stale if a `final` artefact derives from something that is `review` or `draft`.
  3. A pointer matching nothing is broken (stale). A non-file pointer not in the registry is unregistered (warning).
  4. Staleness cascades across stages.
Prints changed or broken, the cascade, and the order to revise (sources first, latest stage last).
Exit 0 = clean, 1 = warnings.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import front, in_code_folder, parse_name, table_rows  # noqa: E402

STAGE_RANK = {"frame": 1, "explore": 2, "harden": 3, "ship": 4}
TYPE_RANK = {"source": 0, "insight": 1, "persona": 2, "workflow": 2, "jtbd": 2, "competitive-scan": 2,
             "opportunity": 3, "research-pack": 4, "brief": 5}
SKIP_NAMES = {"ai-quality-log.md", "decisions-log.md", "handoff-card.md", "assumptions-register.md",
              "open-questions-register.md", "artefact-registry.md", "README.md"}
EXT = re.compile(r"^(figma|jira|github|url):(.+?)(?:@v(\d+))?$")


def pointers_of(body):
    out, in_code = [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in re.finditer(r"\[\[([^\]]+)\]\]", line):
            out.append(m.group(1).strip())
        m = re.search(r"\[(?:high|medium|low)\][^\n]*?\bsrc:\s*(.*)$", line, re.I)
        if m:
            for part in m.group(1).split(";"):
                part = part.strip()
                if EXT.match(part.split(" ")[0]):
                    out.append(part.split(" ")[0])
                else:
                    name = re.split(r"\s*§", part)[0].strip().removesuffix(".md").removesuffix(".html")
                    if name and name.lower() != "none":
                        out.append(name)
    seen, uniq = set(), []
    for d in out:
        if d not in seen:
            seen.add(d)
            uniq.append(d)
    return uniq


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--kb", action="append", default=[])
    a = ap.parse_args()
    eng = Path(a.engagement).expanduser()
    if not eng.is_dir():
        sys.exit(f"ERROR: engagement folder not found: {eng}")

    nodes = {}
    def add(path, derived_ok, superseded=False):
        stem = path.stem
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body, _ = front(text)
        fam, ver, st = parse_name(stem)
        derived = derived_ok and "type" in fm and not superseded
        status = fm.get("status") or st or ("draft" if derived else "raw")
        if stem in nodes and nodes[stem]["derived"] and not derived:
            return
        deps, reviews = [], []
        if derived:
            rv = fm.get("reviews", [])
            reviews = [rv] if isinstance(rv, str) and rv else list(rv or [])
            df = fm.get("derives_from", [])
            df = [df] if isinstance(df, str) and df else (df or [])
            deps = list(df) + pointers_of(body)
        nodes[stem] = {"path": path, "fam": fam, "ver": ver, "status": status, "derived": derived,
                       "stage": fm.get("stage") or "", "kind": fm.get("type") if derived else "source",
                       "deps": list(dict.fromkeys(d for d in deps if d not in reviews)), "reviews": reviews,
                       "superseded": superseded, "external": False, "pointer": None}

    for p in sorted(eng.rglob("*.md")):
        if p.name.startswith(("00-", "05-")) or p.name in SKIP_NAMES or "templates" in p.parts \
                or ".koru" in p.parts or "handoff-cards" in p.parts or in_code_folder(p):
            continue
        add(p, True, superseded="superseded" in p.parts)
    for p in sorted(eng.rglob("*.html")):
        parts = p.parts
        if "templates" in parts or ".koru" in parts or in_code_folder(p):
            continue
        add(p, "sources" not in parts, superseded="superseded" in parts)  # HTML artefacts (wireframes) count as derived; HTML in sources/ is a source
    for kb in a.kb:
        kbp = Path(kb).expanduser()
        if not kbp.is_dir():
            print(f"WARN: --kb folder not found: {kbp}", file=sys.stderr)
            continue
        for p in sorted(list(kbp.rglob("*.md")) + list(kbp.rglob("*.html"))):
            add(p, False)

    # registry rows for non-file artefacts
    pointer_map = {}
    base_to_stem = {re.sub(r"-(draft|review|final)$", "", stem): stem for stem in nodes}
    reg = eng / "artefact-registry.md"
    if reg.is_file():
        for cells in table_rows(reg.read_text(encoding="utf-8")):
            if len(cells) >= 10 and cells[0] not in ("Artefact", ""):
                name, stage, typ, ver, status, home, link, ptr, signer, derives = cells[:10]
                if name in nodes or name in base_to_stem:
                    if ptr:
                        pointer_map[ptr] = name if name in nodes else base_to_stem[name]
                    continue  # a file artefact: its own front matter is the source of truth
                fam, v, _ = parse_name(name if re.search(r"-v\d+$", name) else f"{name}-v{ver or 1}")
                nodes[name] = {"path": reg, "fam": fam, "ver": int(ver) if str(ver).isdigit() else v, "status": status or "draft",
                               "derived": True, "stage": stage, "kind": typ or "external",
                               "deps": [d.strip() for d in derives.split(",") if d.strip()], "external": True, "pointer": ptr}
                if ptr:
                    pointer_map[ptr] = name

    fams = {}
    for stem, n in nodes.items():
        fams.setdefault(n["fam"], []).append((n["ver"], stem))
    newest = {fam: max(v)[0] for fam, v in fams.items()}

    direct, resolved, warnings = {}, {}, []
    for stem, n in nodes.items():
        if not n["derived"]:
            continue
        resolved[stem] = []
        for d in n.get("reviews", []):
            dfam, dver, _ = parse_name(d)
            if not any(v == dver for (v, s) in fams.get(dfam, [])):
                direct.setdefault(stem, []).append(f"broken pointer in reviews: '{d}' matches no artefact or source")
        for d in n["deps"]:
            m = EXT.match(d)
            if m:
                target = pointer_map.get(m.group(1) + ":" + m.group(2))
                if not target:
                    warnings.append(f"{stem}: unregistered external pointer '{d}' (add it to artefact-registry.md to stale-check it)")
                    continue
                t = nodes[target]
                resolved[stem].append(target)
                pinned = int(m.group(3)) if m.group(3) else None
                if pinned and t["ver"] > pinned:
                    direct.setdefault(stem, []).append(f"'{d}' has a newer version (v{t['ver']})")
                if n["status"] == "final" and t["status"] in ("review", "draft"):
                    direct.setdefault(stem, []).append(f"final artefact depends on '{d}' which is {t['status']}")
                continue
            dfam, dver, _ = parse_name(d)
            cand = [s for (v, s) in fams.get(dfam, []) if v == dver]
            if not cand:
                direct.setdefault(stem, []).append(f"broken pointer: '{d}' matches no artefact or source")
                continue
            t = nodes[cand[0]]
            resolved[stem].append(cand[0])
            if newest[dfam] > dver:
                direct.setdefault(stem, []).append(f"'{d}' has a newer version (v{newest[dfam]})")
            if n["status"] == "final" and t["derived"] and t["status"] in ("review", "draft"):
                direct.setdefault(stem, []).append(f"final artefact depends on '{d}' which is {t['status']}")

    stale = set(direct)
    changed = True
    while changed:
        changed = False
        for stem, deps in resolved.items():
            if stem not in stale and any(d in stale for d in deps):
                stale.add(stem)
                changed = True

    for w in warnings:
        print("warn ", w)
    if not stale:
        print("Stale-check clean: no artefact is built on a changed source.")
        print(f"Checked {sum(1 for n in nodes.values() if n['derived'])} derived artefacts against {len(nodes)} nodes.")
        sys.exit(0)
    print("STALE-CHECK: warnings found\n")
    print("Changed or broken (direct):")
    for stem in sorted(direct):
        for r in direct[stem]:
            print(f"  - {stem}: {r}")
    cascade = sorted(stale - set(direct))
    if cascade:
        print("\nAffected by cascade (built on a stale artefact):")
        for stem in cascade:
            via = [d for d in resolved.get(stem, []) if d in stale]
            print(f"  - {stem}  (via {', '.join(via)})")
    order = sorted(stale, key=lambda s: (STAGE_RANK.get(nodes[s]["stage"], 0), TYPE_RANK.get(nodes[s]["kind"], 9), s))
    print("\nOrder to revise (sources first, later stages last):")
    for i, stem in enumerate(order, 1):
        n = nodes[stem]
        print(f"  {i}. {stem}  [{n['stage'] or '?'} {n['kind']}, {n['status']}]")
    print("\nA stale artefact cannot be marked final. Revise (a new version if it was final), get it checked, then re-run.")
    sys.exit(1)


if __name__ == "__main__":
    main()
