#!/usr/bin/env python3
"""Frame pipeline, step 1 adapter: turn cleaned session files into synthesis.json.

Usage:
  python frame_build_synthesis.py build <frame-dir> [--profile research-profile.json]
  python frame_build_synthesis.py check <synthesis.json>

build  Reads 00-raw/manifest.json and the formatter's cleaned .md files in 01-clean/, checks them,
       and writes 02-synthesis/<project>-frame-synthesis-vN-draft.json: one entry per session with
       its manifest facts, the cleaned file, the sections the formatter marked (with line ranges)
       and how to cite it (timestamp or line). No AI, no interpretation: same input, same output.
check  The contract the classify step relies on: every session has an ID and a role, IDs are
       unique, every transcript and cleaned file listed exists.

Any failed check: nothing is written, an entry goes to <frame-dir>/break-log.md, exit 1.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame_common as fc  # noqa: E402

sys.path.insert(0, str(fc.SKILL_SCRIPTS))
from research_profile import load_profile  # noqa: E402

CALL_TYPES = {"fresh_start", "informed", "ad_hoc"}
PATHS = {"roadmap_hypothesis", "discovery_question"}
ARTEFACT_KEYS = {"heuristic_evaluation", "accessibility_check", "competitive_scan", "secondary_research"}
TEXT_EXT = {".txt", ".md", ".vtt", ".srt"}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TS_RE = re.compile(r"^\s*\[?\(?\d{1,2}:\d{2}(:\d{2})?([.,]\d+)?\]?\)?")
SPEAKER_RE = re.compile(r"^\s*(?:\[?\(?[\d:.,]+\]?\)?\s*)?([^:\[\]]{1,40}?):\s")
HEADING_RE = re.compile(r"^(#{2,6}) (.+)$")
STEP = "frame-build-synthesis"


def check_manifest(m, frame_dir):
    errs = []
    if not isinstance(m, dict):
        return ["manifest.json must be a JSON object"]
    if not isinstance(m.get("project"), str) or not KEBAB.match(m.get("project", "")):
        errs.append("manifest.project must be a kebab-case string")
    sessions = m.get("sessions")
    if not isinstance(sessions, list) or not sessions:
        return errs + ["manifest.sessions must be a non-empty list"]
    seen = set()
    for n, s in enumerate(sessions, 1):
        sid = s.get("session_id") if isinstance(s, dict) else None
        tag = f"session #{n}" + (f" ({sid})" if sid else "")
        if not isinstance(s, dict):
            errs.append(f"{tag}: must be an object")
            continue
        if not isinstance(sid, str) or not ID_RE.match(sid):
            errs.append(f"{tag}: session_id missing or not letters/digits/hyphens")
        elif sid in seen:
            errs.append(f"{tag}: session_id is used twice")
        else:
            seen.add(sid)
        if not str(s.get("participant_role") or "").strip():
            errs.append(f"{tag}: participant_role missing")
        if not DATE_RE.match(str(s.get("date", ""))):
            errs.append(f"{tag}: date must be YYYY-MM-DD")
        if s.get("call_type") not in CALL_TYPES:
            errs.append(f"{tag}: call_type must be one of {sorted(CALL_TYPES)}")
        if s.get("path") is not None and s.get("path") not in PATHS:
            errs.append(f"{tag}: path must be one of {sorted(PATHS)} or null")
        for b in ("sorted_before_call", "is_proxy", "screener_used"):
            if b in s and s[b] is not None and not isinstance(s[b], bool):
                errs.append(f"{tag}: {b} must be true, false or null")
        tp = s.get("transcript_path")
        if not tp:
            errs.append(f"{tag}: transcript_path missing")
        elif not (frame_dir / tp).is_file():
            errs.append(f"{tag}: transcript not found: {tp}")
        for k in ("discussion_guide", "clean_path"):
            if s.get(k) and not (frame_dir / s[k]).is_file():
                errs.append(f"{tag}: {k} not found: {s[k]}")
    arts = m.get("artefacts", {})
    if not isinstance(arts, dict):
        errs.append("manifest.artefacts must be an object")
    else:
        for k, v in arts.items():
            if k not in ARTEFACT_KEYS:
                errs.append(f"artefacts.{k}: unknown key (allowed: {sorted(ARTEFACT_KEYS)})")
            elif v and not (frame_dir / v).is_file():
                errs.append(f"artefacts.{k}: file not found: {v}")
    return errs


def find_clean(frame_dir, s, clean_index):
    """Cleaned .md for a session: manifest clean_path, else the highest version whose
    front matter source_file equals the transcript's file name."""
    if s.get("clean_path"):
        return frame_dir / s["clean_path"], None
    name = Path(s["transcript_path"]).name
    hits = [(v, p) for p, (src, v) in clean_index.items() if src == name]
    if not hits:
        return None, f"no cleaned file in 01-clean/ has source_file: {name} (run the formatter on it)"
    best = max(v for v, _ in hits)
    top = [p for v, p in hits if v == best]
    if len(top) > 1:
        return None, f"several cleaned files claim {name} at v{best}: {[p.name for p in top]}; set clean_path in the manifest"
    return top[0], None


def sections_of(lines, body_start, source_lines):
    """Headings the formatter inserted (not ones copied from the source), with 1-based line ranges in the cleaned file."""
    heads = []
    for i in range(body_start - 1, len(lines)):
        m = HEADING_RE.match(lines[i])
        if m and lines[i] not in source_lines:
            heads.append((i, len(m.group(1)), m.group(2).strip()))
    out = []
    for k, (i, lvl, title) in enumerate(heads):
        end = (heads[k + 1][0] if k + 1 < len(heads) else len(lines))
        summary = next((lines[j].strip()[1:-1] for j in range(i + 1, min(i + 4, end))
                        if lines[j].strip().startswith("*") and lines[j].strip().endswith("*")
                        and not lines[j].strip().startswith("**")), None)
        kind = ("overview" if title.lower() in ("session overview", "overview")
                else "figure" if title.startswith("Figure ")
                else "notes" if title.lower() == "moments of note" else "topic")
        out.append({"title": title, "level": lvl, "kind": kind, "summary": summary,
                    "start_line": i + 1, "end_line": end})
    return out


def build(frame_dir, profile_path=None):
    frame_dir = Path(frame_dir).resolve()
    mpath = frame_dir / "00-raw" / "manifest.json"
    inputs = [fc.rel(mpath, frame_dir)]
    if not mpath.is_file():
        fc.write_break(frame_dir, STEP, ["00-raw/manifest.json not found"])
        return None, ["00-raw/manifest.json not found"]
    try:
        m = json.loads(mpath.read_text(encoding="utf-8"))
    except ValueError as e:
        fc.write_break(frame_dir, STEP, [f"manifest.json is not valid JSON: {e}"], inputs)
        return None, [str(e)]
    errs = check_manifest(m, frame_dir)
    warnings = []

    try:
        prof, prof_path = load_profile(profile_path, start=frame_dir)
    except (ValueError, OSError) as e:
        prof, prof_path = None, None
        errs.append(f"research profile invalid: {e}")
    if prof is None and not errs:
        warnings.append("no research-profile.json found; cleaned files were not checked against a project profile")
    elif prof and prof.get("project") != m.get("project"):
        errs.append(f"manifest project '{m.get('project')}' != profile project '{prof.get('project')}' ({prof_path})")
    if errs:
        fc.write_break(frame_dir, STEP, errs, inputs)
        return None, errs

    import validate_md  # from the formatter skill

    clean_index = {}
    for p in sorted((frame_dir / "01-clean").glob("*.md")):
        try:
            fm, _, _ = fc.read_front_matter(p)
        except ValueError:
            continue
        mv = re.search(r"_v(\d+)\.md$", p.name)
        clean_index[p] = (fm.get("source_file"), int(mv.group(1)) if mv else 0)

    sessions = []
    for s in m["sessions"]:
        sid = s["session_id"]
        raw = frame_dir / s["transcript_path"]
        clean, why = find_clean(frame_dir, s, clean_index)
        if why:
            errs.append(f"{sid}: {why}")
            continue
        inputs.append(fc.rel(clean, frame_dir))
        is_text = raw.suffix.lower() in TEXT_EXT
        v_errs, v_warns = validate_md.validate(str(clean), str(raw) if is_text else None,
                                               str(prof_path) if prof_path else None)
        errs += [f"{sid}: {clean.name}: {e}" for e in v_errs]
        if not is_text:
            warnings.append(f"{sid}: transcript is {raw.suffix}; word-for-word check against it was skipped")
        if v_errs:
            continue
        fm, lines, body_start = fc.read_front_matter(clean)
        src_lines = raw.read_text(encoding="utf-8").splitlines() if is_text else []
        nonblank = [l for l in src_lines if l.strip()] or [l for l in lines[body_start - 1:] if l.strip()]
        ts_share = sum(1 for l in nonblank if TS_RE.match(l)) / max(len(nonblank), 1)
        speakers = Counter(mm.group(1).strip() for l in nonblank for mm in [SPEAKER_RE.match(l)] if mm)
        secs = sections_of(lines, body_start, set(src_lines))
        overview = next(("\n".join(l for l in lines[x["start_line"]:x["end_line"]] if l.strip())
                         for x in secs if x["kind"] == "overview"), None)
        role = s["participant_role"]
        if role not in (fm.get("personas") or []):
            warnings.append(f"{sid}: manifest role '{role}' is not in the cleaned file's personas {fm.get('personas')}")
        if s.get("date") and str(fm.get("date")) != s["date"]:
            warnings.append(f"{sid}: manifest date {s['date']} != cleaned file date {fm.get('date')}")
        sessions.append({
            **{k: s.get(k) for k in ("session_id", "date", "call_type", "sorted_before_call", "path",
                                      "participant_role", "cohort", "is_proxy", "moderator", "note_taker",
                                      "screener_used", "discussion_guide", "guide_reviewed_by")},
            "transcript_path": s["transcript_path"],
            "clean_path": fc.rel(clean, frame_dir),
            "clean_title": fm.get("title"),
            "personas": fm.get("personas"),
            "workflow": fm.get("workflow"),
            "lifecycle": fm.get("lifecycle"),
            "research_type": fm.get("research_type"),
            "locator_style": "timestamp" if ts_share >= 0.5 else "line",
            "line_count": len(lines),
            "speakers": dict(speakers.most_common()),
            "overview": overview,
            "sections": [x for x in secs if x["kind"] != "overview"],
        })

    if errs:
        fc.write_break(frame_dir, STEP, errs, inputs)
        return None, errs

    project = m["project"]
    out, ver = fc.output_path(frame_dir / "02-synthesis", project, "frame", "synthesis", "json")
    syn = {
        "schema": "frame-synthesis/1",
        "project": project, "stage": "frame", "artefact": "synthesis", "version": ver, "status": "draft",
        "generated_at": fc.now_iso(), "generated_by": "framework/scripts/frame_build_synthesis.py",
        "note": "Index of cleaned sessions for the classify step. No findings or interpretation here.",
        "manifest": fc.rel(mpath, frame_dir),
        "profile": str(prof_path) if prof_path else None,
        "categories": {
            "traces": ["T", "R", "A", "C", "E", "S"],
            "layers": ["data", "finding", "insight"],
            "cohorts": sorted({s["cohort"] for s in m["sessions"] if s.get("cohort")}),
            "roles": sorted({s["participant_role"] for s in m["sessions"]}),
        },
        "artefacts": m.get("artefacts", {}),
        "totals": {
            "sessions": len(sessions),
            "by_role": dict(Counter(s["participant_role"] for s in sessions)),
            "by_cohort": dict(Counter(s["cohort"] or "(none)" for s in sessions)),
            "by_call_type": dict(Counter(s["call_type"] for s in sessions)),
            "proxies": sum(1 for s in sessions if s.get("is_proxy")),
        },
        "warnings": warnings,
        "sessions": sessions,
    }
    fc.dump_json(syn, out)
    cerrs = check(out)
    if cerrs:
        return None, cerrs
    return out, warnings


def check(syn_path):
    """Contract before the classify step. Returns a list of errors (empty = pass); logs a break on failure."""
    syn_path = Path(syn_path).resolve()
    frame_dir = syn_path.parent.parent
    errs = []
    try:
        syn = json.loads(syn_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errs = [f"cannot read {syn_path.name}: {e}"]
        syn = {}
    if not errs:
        if syn.get("schema") != "frame-synthesis/1":
            errs.append("schema is not frame-synthesis/1")
        sessions = syn.get("sessions")
        if not isinstance(sessions, list) or not sessions:
            errs.append("no sessions listed")
            sessions = []
        ids = Counter(s.get("session_id") for s in sessions)
        for s in sessions:
            sid = s.get("session_id")
            if not sid:
                errs.append("a session has no session_id")
            elif ids[sid] > 1:
                errs.append(f"{sid}: session_id is not unique")
            if not s.get("participant_role"):
                errs.append(f"{sid or '?'}: no participant_role")
            for k in ("transcript_path", "clean_path"):
                if not s.get(k) or not (frame_dir / s[k]).is_file():
                    errs.append(f"{sid or '?'}: {k} missing or not found: {s.get(k)}")
            if s.get("locator_style") not in ("timestamp", "line"):
                errs.append(f"{sid or '?'}: locator_style must be timestamp or line")
    if errs:
        fc.write_break(frame_dir, STEP + " (contract check)", sorted(set(errs)), [fc.rel(syn_path, frame_dir)])
    return sorted(set(errs))


def main(argv):
    args = argv[1:]
    profile = None
    if "--profile" in args:
        k = args.index("--profile")
        profile = args[k + 1] if k + 1 < len(args) else None
        args = args[:k] + args[k + 2:]
    if len(args) != 2 or args[0] not in ("build", "check"):
        print(__doc__)
        return 2
    if args[0] == "build":
        out, msgs = build(args[1], profile)
        if out is None:
            print("STOPPED: contract failed, nothing written. Logged to break-log.md:")
            for e in msgs:
                print(f"  - {e}")
            return 1
        print(f"Wrote {out}")
        for w in msgs:
            print(f"  warn: {w}")
        return 0
    errs = check(args[1])
    if errs:
        print("FAIL: contract for the classify step not met (logged to break-log.md):")
        for e in errs:
            print(f"  - {e}")
        return 1
    print(f"OK: {args[1]} meets the contract for the classify step")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
