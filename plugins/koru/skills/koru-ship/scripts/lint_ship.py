#!/usr/bin/env python3
"""Ship-only structure and coverage checks. Run after koru-core lint_core.py and lint_lines.py.

Usage:
  python lint_ship.py <file-or-folder> [...] [--tokens <tokens.css>] [--screens <harden screens .html>]
                      [--ship-notes <harden ship-notes .md>]
  python lint_ship.py --intake <engagement>

Per artefact type (read from the front matter `type:`; only stage `ship` files are checked):
  ticket            the nine template fields as '## ' headings, in order; Title not empty; optional
                    Priority is a Jira priority; User story is "As a ..., I want ..., so that ...";
                    Context has Framed brief, Figma frame and HTML deliverable lines (the deliverable
                    with .html); every acceptance criterion is one "- Given ..., when ..., then ..." line;
                    States covered lists Empty, Loading, Error and Success, and every state listed has
                    a criterion; AI states need a criterion for a wrong answer and one for the audit log;
                    Screenshots link at least one #step-N-state-<state> anchor and no missing image file;
                    Tokens used, Out of scope and Open questions are not empty
  deliverable       (.html) self-contained; "Step N:" labels in order, each with id="step-N"; each
                    "State: X" label has id="step-N-state-<x>"; a state switcher (id or class
                    "state-switcher"); a "Design system gaps" section; no raw colour outside :root;
                    no add-ons
  handoff-note      the four parts (What's in the deliverable, What's not, Decisions engineers should
                    know about, Who to ask), none empty; warns above about half a page (350 words)
  pr-readiness      the seven sections, none empty
  user-story        1 to 5 stories ("### U<n>."), each with an "As a ..., I want ..., so that ..." line
                    (warns under 3)
  review            the questions table; a "Buildable without questions: n of N" line; at review or final,
                    every row has a resolution
Across files: warns if the latest tickets number fewer than 3 or more than 5.

--tokens <tokens.css or tokens .md>: every token in a ticket's "Tokens used" and every var(--x) in the
    deliverable must exist in the design library; the deliverable's :root values must match it.
--screens <harden screens .html>: every Step N and State in Harden's hardened screens must be in the
    deliverable.
--ship-notes <harden ship-notes .md>: every Ship note id (SN<n>) in Harden's table must appear as
    "Ship note SN<n>" in a ticket or the handoff note among the files checked.
--intake <engagement>: step S1's gate. Fails unless a final hardened design exists (and no newer draft or
    review version), a tokens.css exists under 04-design-library/, and core's stale-check is clean.
Exit 1 if there are errors.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def _core_scripts():
    """Find koru-core/scripts: $KORU_CORE, or the sibling skill folder."""
    for c in (os.environ.get("KORU_CORE"), str(Path(__file__).resolve().parent.parent.parent / "koru-core")):
        if c and (Path(c) / "scripts" / "_common.py").is_file():
            return Path(c) / "scripts"
    sys.exit("ERROR: koru-core not found. Install it next to koru-ship or set KORU_CORE to its folder.")


CORE_SCRIPTS = _core_scripts()
sys.path.insert(0, str(CORE_SCRIPTS))
from _common import front, parse_name  # noqa: E402

TICKET_FIELDS = ["Title", "User story", "Context", "Acceptance criteria", "States covered", "Screenshots",
                 "Tokens used", "Out of scope", "Open questions"]
NOTE_PARTS = ["What's in the deliverable", "What's not", "Decisions engineers should know about", "Who to ask"]
PR_PARTS = ["Spec per unit", "Plan per ticket", "Questions file", "Component build", "Journey tests in CI",
            "Review action", "Setup still missing"]
CONTEXT_LINKS = ["Framed brief", "Figma frame", "HTML deliverable"]
BASE_STATES = ["Empty", "Loading", "Error", "Success"]
PRIORITIES = {"highest", "high", "medium", "low", "lowest"}
REVIEW_HDR = "| Ticket | Question I'd have to ask | Where the answer should go | Resolution |"
STORY = re.compile(r"\bAs an? .+?, I want .+?, so that .+", re.I)
GWT = re.compile(r"^Given\b.+?,\s*when\b.+?,\s*then\b.+", re.I)
ANCHOR = re.compile(r"#step-\d+-state-[a-z0-9-]+")
SCORE = re.compile(r"Buildable without questions:\s*\d+\s+of\s+\d+", re.I)
RAW_COLOUR = re.compile(r"(?<![\w-])#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(", re.I)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def norm(s):
    return s.replace("’", "'").strip()


def sections(body, level=2):
    """{heading: [lines]} for headings of exactly this level, in order."""
    out, cur = {}, None
    mark = "#" * level + " "
    for line in body.splitlines():
        if line.startswith(mark):
            cur = norm(line[len(mark):])
            out[cur] = []
        elif re.match(r"^#{1,%d} " % level, line):
            cur = None
        elif cur is not None:
            out[cur].append(line)
    return out


def content(lines):
    return [l for l in lines if l.strip() and not l.strip().startswith("<!--")]


def items(lines, top_only=True):
    pat = r"^[-*]\s+(.*)$" if top_only else r"^\s*[-*]\s+(.*)$"
    return [m.group(1).strip() for l in lines for m in [re.match(pat, l)] if m]


def load_tokens(path):
    """{name: value} from tokens.css (--name: value;) or the Harden tokens .md (| name | value | ...)."""
    text = Path(path).read_text(encoding="utf-8")
    toks = {}
    if str(path).endswith(".css"):
        for m in re.finditer(r"--([a-z0-9-]+)\s*:\s*([^;]+);", text, re.I):
            toks[m.group(1)] = m.group(2).strip()
    else:
        for m in re.finditer(r"^\|\s*([a-z][a-z0-9-]+)\s*\|\s*([^|]+?)\s*\|", text, re.M | re.I):
            if m.group(1).lower() not in ("token", "foreground"):
                toks[m.group(1)] = m.group(2)
    return toks


def check_ticket(body, path, tokens):
    errs, warns = [], []
    secs = sections(body)
    names = [h for h in secs if h in TICKET_FIELDS]
    for f in TICKET_FIELDS:
        if f not in secs:
            errs.append(f"missing field '## {f}'")
        elif not content(secs[f]):
            errs.append(f"field '{f}' is empty")
    if names != [f for f in TICKET_FIELDS if f in secs]:
        warns.append("fields are not in the template order")
    # Title
    t = [l.strip() for l in content(secs.get("Title", [])) if not l.strip().lower().startswith("priority:")]
    if t and t[0].split()[0].lower() in ("the", "a", "an"):
        warns.append(f"Title should start with a verb (verb plus object): '{t[0]}'")
    for l in secs.get("Title", []):
        m = re.match(r"^\s*Priority:\s*(.*)$", l, re.I)
        if m and m.group(1).strip() and m.group(1).strip().lower() not in PRIORITIES:
            errs.append(f"Priority '{m.group(1).strip()}' is not Highest, High, Medium, Low or Lowest")
    # User story
    if secs.get("User story") is not None and not STORY.search(" ".join(secs["User story"])):
        errs.append("User story must read 'As a <role>, I want <thing>, so that <outcome>.'")
    # Context
    ctx = secs.get("Context", [])
    for lab in CONTEXT_LINKS:
        line = next((l for l in ctx if re.match(rf"^[-*]\s+{lab}:", l.strip(), re.I)), None)
        if line is None:
            errs.append(f"Context needs a '- {lab}: ...' line")
        elif not line.split(":", 1)[1].strip():
            errs.append(f"Context '{lab}' is empty")
        elif lab == "HTML deliverable" and ".html" not in line:
            errs.append("Context 'HTML deliverable' must link the deliverable .html file")
    # Acceptance criteria
    ac_lines = secs.get("Acceptance criteria", [])
    ac = items(ac_lines)
    if secs.get("Acceptance criteria") is not None and not ac:
        errs.append("Acceptance criteria has no '- Given ..., when ..., then ...' lines")
    for a in ac:
        if not GWT.match(a):
            errs.append(f"criterion is not one 'Given ..., when ..., then ...' line: '{a[:70]}'")
        elif len(re.findall(r"\bgiven\b", a, re.I)) > 1 or len(re.findall(r"\bthen\b", a, re.I)) > 1:
            errs.append(f"one criterion per line (split it): '{a[:70]}'")
    ac_text = " ".join(ac_lines).lower()
    # States covered
    st = items(secs.get("States covered", []))
    listed = {}
    for s in st:
        name = s.split(":", 1)[0].strip()
        listed[name.lower()] = s
    for b in BASE_STATES:
        if b.lower() not in listed:
            errs.append(f"States covered must list '{b}' (or '{b}: Not applicable: <reason>')")
    for name, s in listed.items():
        if "not applicable" in s.lower():
            continue
        if name not in ac_text:
            errs.append(f"state '{name}' is listed but no acceptance criterion names it")
        if ANCHOR.search(s) is None:
            warns.append(f"state '{name}' has no #step-N-state-<state> anchor")
    if any(n.startswith("ai") for n in listed if "not applicable" not in listed[n].lower()):
        if "wrong" not in ac_text:
            errs.append("AI states are covered but no criterion says what happens when the AI is wrong")
        if "log" not in ac_text:
            errs.append("AI states are covered but no criterion says how it is logged (audit log)")
    # Screenshots
    shots = " ".join(secs.get("Screenshots", []))
    if secs.get("Screenshots") is not None and not ANCHOR.search(shots):
        errs.append("Screenshots must link at least one deliverable anchor (#step-N-state-<state>)")
    for m in re.finditer(r"([\w./-]+\.(?:png|jpe?g|gif|webp))", shots, re.I):
        img = m.group(1)
        if img.startswith(("http:", "https:")):
            continue
        if not (Path(path).parent / img).is_file() and not Path(img).is_file():
            errs.append(f"Screenshots link an image file that does not exist: {img} (never make one up)")
    # Tokens used
    used = []
    for it in items(secs.get("Tokens used", [])):
        used += [x.strip().lstrip("-").strip("`") for x in re.split(r"[,;]", it) if x.strip()]
    if tokens is not None:
        for u in used:
            if u and u.lower() != "none" and u not in tokens:
                errs.append(f"token '{u}' is not in the design library's tokens")
    # Open questions
    for q in items(secs.get("Open questions", [])):
        if q.lower() != "none" and not re.search(r"\b[QA]\d+\b", q):
            warns.append(f"open question without a register id (Q<n>): '{q[:60]}'")
    return errs, warns


def html_labels(raw):
    """[(step, [states])] in document order, from 'Step N:' and 'State: X' labels."""
    m = re.search(r"<main\b.*?</main>", raw, re.S | re.I)
    part = m.group(0) if m else raw
    part = re.sub(r"<!--.*?-->", "", part, flags=re.S)
    out = []
    for mm in re.finditer(r"Step\s+(\d+):|State:\s*([^<\n]+)", part):
        if mm.group(1):
            out.append((int(mm.group(1)), []))
        elif out:
            out[-1][1].append(mm.group(2).strip())
    return out


def check_deliverable(raw, tokens, screens):
    errs, warns = [], []
    if re.search(r"<script[^>]+src\s*=", raw, re.I) or re.search(r"<link[^>]+href\s*=\s*[\"']?(https?:)?//", raw, re.I) \
            or re.search(r"<img[^>]+src\s*=\s*[\"']?(https?:)?//", raw, re.I) or re.search(r"@import\s+url\(", raw, re.I) \
            or re.search(r"url\(\s*[\"']?(https?:)?//", raw, re.I):
        errs.append("deliverable is not self-contained (external script, stylesheet, font or image)")
    labels = html_labels(raw)
    if not labels:
        errs.append("no 'Step N:' labels inside <main>")
    nums = [n for n, _ in labels]
    if nums != sorted(nums):
        errs.append(f"steps are not in journey order: {nums}")
    ids = set(re.findall(r"\bid\s*=\s*[\"']([^\"']+)[\"']", raw))
    for n, states in labels:
        if f"step-{n}" not in ids:
            errs.append(f"Step {n} has no id=\"step-{n}\" anchor")
        if not states:
            errs.append(f"Step {n} has no 'State:' labels")
        for s in states:
            a = f"step-{n}-state-{slug(s)}"
            if a not in ids:
                errs.append(f"Step {n} State '{s}' has no id=\"{a}\" anchor")
    if not re.search(r"(id|class)\s*=\s*[\"'][^\"']*\bstate-switcher\b", raw):
        errs.append("no state switcher (an element with id or class 'state-switcher')")
    if not re.search(r"Design system gaps", raw):
        errs.append("deliverable needs a 'Design system gaps' section (or 'None')")
    if not re.search(r"Viewport:", raw):
        warns.append("no 'Viewport:' label (keep Harden's smallest target viewport label on each screen)")
    if not re.search(r">\s*Anchors\s*<", raw):
        warns.append("no 'Anchors' appendix listing every step and state anchor")
    if re.search(r"\badd-ons?\b", re.sub(r"<!--.*?-->", "", raw, flags=re.S), re.I):
        errs.append("add-ons must stay out of the deliverable")
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", raw, re.S | re.I))
    css += " " + " ".join(re.findall(r"\bstyle\s*=\s*\"([^\"]*)\"", raw))
    roots = re.findall(r":root\s*\{([^}]*)\}", css)
    outside = re.sub(r":root\s*\{[^}]*\}", "", css)
    outside = re.sub(r"/\*.*?\*/", "", outside, flags=re.S)
    for m in RAW_COLOUR.finditer(outside):
        errs.append(f"raw colour '{outside[m.start():m.start() + 12].strip()}' outside :root; use var(--token)")
        break
    if tokens is not None:
        defined = {}
        for r in roots:
            for m in re.finditer(r"--([a-z0-9-]+)\s*:\s*([^;]+);", r, re.I):
                defined[m.group(1)] = m.group(2).strip()
        for k, v in defined.items():
            if k not in tokens:
                errs.append(f"token '--{k}' in :root is not in the design library (invented token)")
            elif tokens[k].lower() != v.lower():
                errs.append(f"token '--{k}' is {v} here but {tokens[k]} in the design library")
        for k in sorted(set(re.findall(r"var\(\s*--([a-z0-9-]+)", outside, re.I))):
            if k not in tokens:
                errs.append(f"var(--{k}) is not a design library token")
    if screens is not None:
        have = {(n, slug(s)) for n, ss in labels for s in ss}
        for n, ss in html_labels(Path(screens).read_text(encoding="utf-8")):
            for s in ss:
                if (n, slug(s)) not in have:
                    errs.append(f"Harden screens have Step {n} State '{s}' but the deliverable does not")
    return errs, warns


def check_parts(body, parts, what):
    errs = []
    secs = sections(body)
    for p in parts:
        if p not in secs:
            errs.append(f"{what} needs a '## {p}' section")
        elif not content(secs[p]):
            errs.append(f"{what} section '{p}' is empty")
    return errs, secs


def check(path, tokens, screens):
    raw = Path(path).read_text(encoding="utf-8")
    fm, body, _ = front(raw)
    t = fm.get("type")
    if not t or (fm.get("stage") and fm["stage"] != "ship"):
        return None
    errs, warns = [], []
    if t == "ticket":
        errs, warns = check_ticket(body, path, tokens)
    elif t == "deliverable":
        errs, warns = check_deliverable(raw, tokens, screens)
    elif t == "handoff-note":
        errs, secs = check_parts(body, NOTE_PARTS, "handoff note")
        words = sum(len(" ".join(secs.get(p, [])).split()) for p in NOTE_PARTS)
        if words > 350:
            warns.append(f"handoff note is {words} words across its four parts; half a page is about 250 to 300")
    elif t == "pr-readiness":
        errs, _ = check_parts(body, PR_PARTS, "PR readiness note")
    elif t == "user-story":
        stories = re.split(r"^### U\d+\.", body, flags=re.M)[1:]
        if not stories:
            errs.append("no stories ('### U1. <verb plus object>')")
        if len(stories) > 5:
            errs.append(f"{len(stories)} stories: 3 to 5 for one flow (more means a second flow)")
        elif 0 < len(stories) < 3:
            warns.append(f"{len(stories)} stories: 3 to 5 is the norm for one flow")
        for i, s in enumerate(stories, 1):
            if not STORY.search(s):
                errs.append(f"story {i} has no 'As a ..., I want ..., so that ...' line")
    elif t == "review":
        lines = body.splitlines()
        if not any(norm(l).replace(" ", "") == REVIEW_HDR.replace(" ", "") for l in lines):
            errs.append(f"review needs the table header: {REVIEW_HDR}")
        if not SCORE.search(body):
            errs.append("review needs 'Buildable without questions: n of N'")
        if fm.get("status") in ("review", "final"):
            for l in lines:
                c = [x.strip() for x in l.strip().strip("|").split("|")] if l.strip().startswith("|") else []
                if len(c) >= 4 and c[0] != "Ticket" and not set(c[0]) <= set("-: ") and not c[3]:
                    errs.append(f"review row has no resolution: {c[1][:60]}")
    else:
        return None
    return t, errs, warns


def collect(paths):
    out = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            out += sorted(x for x in list(p.rglob("*.md")) + list(p.rglob("*.html"))
                          if not {"templates", "superseded", "sources", "export", "export-preview"} & set(x.parts))
        elif p.is_file():
            out.append(p)
        else:
            print(f"WARN: {p} not found", file=sys.stderr)
    return out


def intake(eng):
    eng = Path(eng).expanduser()
    errs, found = [], {}
    if not (eng / "00-read-me-first.md").is_file():
        return [f"{eng} is not a koru engagement"], found
    fams = {}
    for p in list(eng.rglob("*.md")) + list(eng.rglob("*.html")):
        if {"templates", "superseded"} & set(p.parts):
            continue
        fm, _, _ = front(p.read_text(encoding="utf-8"))
        if fm.get("stage") == "harden" and fm.get("type"):
            fam, ver, st = parse_name(p.stem)
            fams.setdefault((fm["type"], fam), []).append((ver, fm.get("status"), p))
    hd = [v for (t, _), v in fams.items() if t == "hardened-design"]
    if not hd:
        errs.append("no hardened design (type hardened-design, stage harden) in the engagement: Harden has not handed on")
    for versions in hd:
        versions.sort(key=lambda x: x[0])
        finals = [v for v in versions if v[1] == "final"]
        if not finals:
            errs.append(f"hardened design is not final: {versions[-1][2].name}")
        elif versions[-1][1] != "final":
            errs.append(f"a newer non-final hardened design exists: {versions[-1][2].name}")
        else:
            found["hardened design"] = versions[-1][2]
    for t in ("screens", "tokens", "ship-notes", "states", "roles", "edge-cases", "feasibility"):
        latest = [sorted(v, key=lambda x: x[0])[-1] for (tt, _), v in fams.items() if tt == t]
        fin = [x for x in latest if x[1] == "final"]
        if fin:
            found[t] = fin[0][2]
        else:
            errs.append(f"no final Harden '{t}' artefact")
    css = sorted((eng / "04-design-library").rglob("tokens.css")) if (eng / "04-design-library").is_dir() else []
    if css:
        found["tokens.css"] = css[0]
    else:
        errs.append("no tokens.css under 04-design-library/ (Harden's export_tokens.py writes it)")
    r = subprocess.run([sys.executable, str(CORE_SCRIPTS / "stale_check.py"), "--engagement", str(eng)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        errs.append("core stale-check has warnings:\n    " + "\n    ".join(r.stdout.strip().splitlines()[:12]))
    return errs, found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--tokens")
    ap.add_argument("--screens")
    ap.add_argument("--ship-notes")
    ap.add_argument("--intake", metavar="ENGAGEMENT")
    a = ap.parse_args()

    if a.intake:
        errs, found = intake(a.intake)
        for k, v in found.items():
            print(f"found  {k}: {v}")
        for e in errs:
            print("ERROR", e)
        print("Intake: " + ("REFUSED. Harden has not handed on; do not start Ship." if errs else "ready for S1."))
        sys.exit(1 if errs else 0)
    if not a.paths:
        ap.error("give files or folders to check, or --intake <engagement>")

    tokens = load_tokens(a.tokens) if a.tokens else None
    bad, checked, texts, tickets = 0, 0, [], {}
    for f in collect(a.paths):
        r = check(f, tokens, a.screens)
        if r is None:
            continue
        t, e, w = r
        checked += 1
        if t in ("ticket", "handoff-note"):
            texts.append(f.read_text(encoding="utf-8"))
        if t == "ticket":
            fam, ver, _ = parse_name(f.stem)
            tickets[fam] = max(ver, tickets.get(fam, 0))
        for x in e:
            print(f"ERROR {f}: {x}")
        for x in w:
            print(f"warn  {f}: {x}")
        bad += len(e)
        print(f"[{'FAIL' if e else 'ok'}] {f}")
    if tickets and not 3 <= len(tickets) <= 5:
        print(f"warn  {len(tickets)} tickets checked: 3 to 5 is the norm for one flow")
    if a.ship_notes:
        ids = re.findall(r"^\|\s*(SN\d+)\s*\|", Path(a.ship_notes).read_text(encoding="utf-8"), re.M)
        joined = "\n".join(texts)
        for i in ids:
            if not re.search(rf"\bShip note {i}\b", joined):
                print(f"ERROR Ship note {i} from Harden is neither closed in a ticket nor carried in the handoff note")
                bad += 1
        print(f"Ship notes: {len(ids)} in Harden's list")
    print(f"Checked {checked} Ship artefacts; {bad} errors.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
