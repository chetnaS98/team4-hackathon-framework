#!/usr/bin/env python3
"""Build a research .md (any content_type) from the ORIGINAL text plus a small plan, without altering the source.

Usage: python build_verbatim.py plan.json source.txt <out_dir> [--profile research-profile.json]
The plan's product/lifecycle are checked against the project profile (given, or the nearest
research-profile.json above <out_dir>) before anything is written.
Source lines are copied byte-for-byte; only headings/summaries and figure blocks are inserted between lines.
Exits 1 if the source cannot be reproduced exactly from the output.

Optional plan key "figures": [{"id":"fig01","image":"<path from extract_images.py>","alt":"one line",
  "title":"Slide 3: Booking flow","after_line":42,"transcription":"every visible element","level":3}]
Each image is copied to <out_dir>/assets/<md-stem>_<id>.<ext> and embedded right after source line
`after_line` (0 = before the source text), followed by its transcription.
"""
import json
import re
import shutil
import sys
from pathlib import Path


def yv(v):
    if isinstance(v, list):
        return "[" + ", ".join(json.dumps(str(x), ensure_ascii=False) if re.search(r"[:#|\[\]]", str(x)) else str(x) for x in v) + "]"
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, int):
        return str(v)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", str(v)) or re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(v)):
        return str(v)
    return json.dumps(str(v), ensure_ascii=False)


def main(argv):
    profile_path = None
    if "--profile" in argv:
        k = argv.index("--profile")
        profile_path = argv[k + 1] if k + 1 < len(argv) else None
        argv = argv[:k] + argv[k + 2:]
    if len(argv) != 4:
        print(__doc__)
        return 2
    plan = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    raw = Path(argv[2]).read_bytes()
    src = raw.decode("utf-8")
    lines = src.splitlines(keepends=True)
    out_dir = Path(argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from research_profile import load_profile
    try:
        prof, prof_path = load_profile(profile_path, start=out_dir)
    except (ValueError, OSError) as e:
        print(f"ERROR: project profile invalid: {e}")
        return 1
    if prof is None:
        print("note: no research-profile.json found; product/lifecycle not checked against a project.")
    else:
        if plan["product"] not in prof["products"]:
            print(f"ERROR: product '{plan['product']}' not in {prof_path}: {sorted(prof['products'])}")
            return 1
        allowed = set(prof.get("lifecycle") or {}) | {"multi"}
        bad = [x for x in plan.get("lifecycle", []) if prof.get("lifecycle") and x not in allowed]
        if bad:
            print(f"ERROR: lifecycle {bad} not in {prof_path}: {sorted(allowed)}")
            return 1

    wf = plan["workflow"]
    q = plan.get("qualifier")
    ver = int(plan.get("version", 1))
    ct = plan.get("content_type", "transcript")
    ctype = ct + (f"-{q}" if q else "")
    fname = f"{plan['product']}_{wf[0]}_{ctype}_v{ver}.md"
    wf_title = " ".join(w.capitalize() for w in wf[0].split("-"))
    ct_title = " ".join(w.capitalize() for w in ct.split("-")) + (f" {q.upper()}" if q else "")
    h1 = f"{plan['product'].capitalize()} | {wf_title} | {ct_title}"
    title = f"{h1} | v{ver}"

    fm = {
        "title": title,
        "description": plan["description"],
        "product": plan["product"],
        "personas": plan["personas"],
        "lifecycle": plan["lifecycle"],
        "workflow": wf,
        "research_type": plan["research_type"],
        "content_type": ct,
        "date": plan["date"],
    }
    if plan.get("customer"):  # only when research relates to a particular customer
        fm["customer"] = plan["customer"]
    for k in ("participants",):
        if k in plan:
            fm[k] = plan[k]
    fm["status"] = plan.get("status", "raw")
    if plan.get("source_file"):
        fm["source_file"] = plan["source_file"]
    for k in ("related", "jira_confluence", "tags", "confidentiality"):
        if plan.get(k):
            fm[k] = plan[k]
    fm["schema_version"] = 1

    secs = sorted(plan.get("sections", []), key=lambda s: s["line"])
    if secs and secs[0]["line"] > 1:
        secs.insert(0, {"line": 1, "title": "Preamble",
                        "summary": "Opening lines of the source before the first topic."})
    for s in secs:
        if not 1 <= s["line"] <= max(len(lines), 1):
            print(f"ERROR: section line {s['line']} outside 1..{len(lines)}")
            return 1

    head = ["---"] + [f"{k}: {yv(v)}" for k, v in fm.items()] + ["---", "", f"# {h1}", "",
            f"*{plan['context']}*", ""]
    if plan.get("overview"):
        oh = "Session overview" if ct == "transcript" else "Overview"
        head += [f"## {oh}", "", plan["overview"].strip(), ""]
    stem = fname[:-3]
    figs = plan.get("figures", [])
    figs_after = {}
    for n, f in enumerate(figs, 1):
        for k in ("id", "image", "alt", "transcription"):
            if not str(f.get(k, "")).strip():
                print(f"ERROR: figure #{n} missing '{k}'")
                return 1
        if not Path(f["image"]).is_file():
            print(f"ERROR: figure {f['id']}: image not found: {f['image']}")
            return 1
        al = int(f.get("after_line", 0))
        if not 0 <= al <= len(lines):
            print(f"ERROR: figure {f['id']}: after_line {al} outside 0..{len(lines)}")
            return 1
        figs_after.setdefault(al, []).append((n, f))

    titled = {s["line"] - 1: s for s in secs if s.get("title")}
    sec_levels = sorted((s["line"], int(s.get("level", 2))) for s in secs if s.get("title"))

    def fig_block(n, f, after):
        prior = [lv for ln, lv in sec_levels if ln <= after]
        lvl = int(f.get("level", (prior[-1] + 1) if prior else (2 if not lines else 3)))
        lvl = min(lvl, 6)
        ext = Path(f["image"]).suffix.lower()
        rel = f"assets/{stem}_{f['id']}{ext}"
        (out_dir / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f["image"], out_dir / rel)
        title = f.get("title") or f["id"]
        alt = re.sub(r"\s+", " ", f["alt"]).replace("[", "(").replace("]", ")").strip()
        return (f"\n{'#' * lvl} Figure {n}: {title}\n\n![{alt}]({rel})\n\n"
                f"**Transcription:** {f['transcription'].strip()}\n\n")

    body, emitted = [], []
    if 0 in figs_after:
        body += [fig_block(n, f, 0) for n, f in figs_after[0]]
    if not titled:
        body.append("\n")
    for i, line in enumerate(lines):
        if i in titled:
            s = titled[i]
            body.append(f"\n{'#' * int(s.get('level', 2))} {s['title']}\n\n*{s['summary']}*\n\n")
        body.append(line)
        emitted.append(line)
        if i + 1 in figs_after:
            if not line.endswith("\n"):
                body.append("\n")
            body += [fig_block(n, f, i + 1) for n, f in figs_after[i + 1]]
    tail = ""
    if plan.get("notes"):
        tail = "\n\n## Moments of note\n\n" + plan["notes"].strip() + "\n"
    elif lines and not lines[-1].endswith("\n") and not figs_after.get(len(lines)):
        tail = "\n"

    # Exact reproduction check: the source lines must come back out unchanged.
    if "".join(emitted) != src:
        print("ERROR: transcript body does not reproduce the source exactly; not writing file.")
        return 1

    out = out_dir / fname
    # open(newline="") keeps the source's line endings; Path.write_text(newline=) needs Python 3.10+
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(head) + "".join(body) + tail)
    pat = "#" if ct == "transcript" else "# "
    hashes = sum(1 for l in lines if l.startswith(pat))
    if hashes:
        print(f"note: {hashes} source line(s) start with '{pat.strip()}' (kept as-is); chunkers may read them as headings.")
    print(f"Wrote {out}  ({len(lines)} source lines kept verbatim, {len(titled)} sections, {len(figs)} figures embedded)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
