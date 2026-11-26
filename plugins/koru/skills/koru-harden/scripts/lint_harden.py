#!/usr/bin/env python3
"""Harden-only structure and coverage checks. Run after koru-core lint_core.py and lint_lines.py.

Usage:
  python lint_harden.py <file-or-folder> [...] [--scope <scope artefact>]

Per artefact type (read from the front matter `type:`):
  scope             Screens, Roles and Target viewports tables (each viewport has a width×height size),
                    "Inherited from Explore", "Out of scope"
  feasibility       table header; an answered row must cite a source
  states            table header; allowed state names; every screen has Empty, Loading, Error, Success;
                    a screen with any AI state has all four; one "AI touchpoints" block per touchpoint with
                    every field; "Accepted suggestions audit-logged" is never No; "not yet known" carries a Q id
  roles             table header; See/Change/Undo/Approve values are Yes, No, Own only or not yet known;
                    "If the person who must act is away" section
  edge-cases        table header; the standard cases appear: long text, no data, a lot of data,
                    double submit, no delegate (approver or owner away), session timeout
  accessibility     a "Standard:" line; table header; Result is Pass, Fail or Not checked
  tokens            the four token tables and the contrast pairs table; colour values are hex;
                    contrast pairs name existing colour tokens
  screens (.html)   self-contained; "Step N:", "State:" and "Viewport:" labels; "Fixes applied in this version";
                    "Design system gaps"; no add-ons
  rulebook-chapter  the seven chapter headings; rules as "- R<n> (must|must not): ... src: ..."
  rulebook-check    table header; Result is Pass, Break or Not applicable; every Break has an action
  checklist         table header; the ten items; Result is Pass, Gap or Not applicable
  ship-notes        the four sections; note ids SN<n>
  hardened-design   links the screens, tokens, checklist, rulebook check and Ship notes

Across files (no --scope needed): when a states and a roles artefact are both among the files checked,
every screen where a roles row has a No must have a No permission state.

--scope <file>: coverage. Reads the scope artefact and fails if any screen is missing from states (with
its four base states, Partial for a screen with data from another system, and the AI states for a screen
with an AI touchpoint), roles, edge-cases, accessibility or the hardened screens HTML among the files
checked; and if the hardened screens do not show the smallest target viewport.
Exit 1 if there are errors.
"""
import argparse
import os
import re
import sys
from pathlib import Path


def _core_scripts():
    """Find koru-core/scripts: $KORU_CORE, or the sibling skill folder."""
    for c in (os.environ.get("KORU_CORE"), str(Path(__file__).resolve().parent.parent.parent / "koru-core")):
        if c and (Path(c) / "scripts" / "_common.py").is_file():
            return str(Path(c) / "scripts")
    sys.exit("ERROR: koru-core not found. Install it next to koru-harden or set KORU_CORE to its folder.")


sys.path.insert(0, _core_scripts())
from _common import front  # noqa: E402

TYPES = ("scope", "feasibility", "states", "roles", "edge-cases", "accessibility", "tokens", "screens",
         "rulebook-chapter", "rulebook-check", "checklist", "ship-notes", "hardened-design")
HDR = {
    "scope_screens": "| Step | Screen | What the user does | Data shown or changed | Data from another system | AI touchpoint | Source |",
    "scope_viewports": "| Viewport | Size | Devices and context | Source |",
    "scope_roles": "| Role | Who they are | Source |",
    "feasibility": "| Question | Screen | Engineer's answer | Design impact | Source |",
    "states": "| Screen | State | What the user sees | Copy (draft) | How they recover or move on | Source |",
    "roles": "| Role | Screen or action | See | Change | Undo | Approve | Must not see | Source |",
    "edge-cases": "| Edge case | Screen | What happens in Design v1 | Design response | Source |",
    "accessibility": "| Check | Screen | Result | Detail | Fix |",
    "token": "| Token | Value | Use | Source |",
    "pairs": "| Foreground | Background | Use |",
    "rulebook-check": "| Rule | Screen and state | Result | Reason | Action |",
    "checklist": "| Item | Result | Evidence | Gaps or notes |",
    "ship-notes": "| Id | Note | Screen and state | Why it was not fixed in Harden | Owner |",
}
BASE_STATES = ["Empty", "Loading", "Error", "Success"]
AI_STATES = ["AI thinking", "AI low confidence", "AI wrong", "AI override"]
ALL_STATES = BASE_STATES + ["Partial", "Stale", "No permission"] + AI_STATES
AI_FIELDS = ["Trigger:", "Who sees a wrong answer:", "Who fixes it:", "How the user overrides or undoes it:",
             "How it is logged:", "Accepted suggestions audit-logged:"]
AUDIT = "Accepted suggestions audit-logged:"
STANDARD_EDGE = ["long text", "no data", "a lot of data", "double submit", "no delegate", "session timeout"]
SIZE = re.compile(r"(\d{3,5})\s*[x×]\s*(\d{3,5})")
PERM = {"yes", "no", "own only", "not yet known"}
CHECK_ITEMS = [
    "Empty, loading, error and success states for every screen",
    "Each role sees what it should, and nothing it shouldn't",
    "Permissions: who can see, change and undo each thing",
    "Edge data: long names, no data, a lot of data",
    "Keyboard use and colour contrast checked",
    "AI states: thinking, low confidence, wrong answer, override or undo",
    "Feasibility checked with an engineer, limits noted",
    "Checked against the system as a whole",
    "Rulebook checks passed, or fixes listed for Ship",
    "Every screen works at the smallest target viewport as well as large screens",
]
CHAPTER = ["Purpose", "Rules", "Patterns", "Decisions", "Checks", "Instructions for AI tools", "Owner"]


def norm(s):
    return re.sub(r"\s+", " ", s.strip())


def key(s):
    return norm(s).lower()


def is_sep(l):
    return set(l.strip()) <= set("|-: ")


def table(lines, header):
    """Rows (list of cells) of the table whose header line equals `header`."""
    out, on = [], False
    for l in lines:
        if not on:
            if l == header:
                on = True
            continue
        if not l.startswith("|"):
            break
        if is_sep(l):
            continue
        out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out


def placeholder(row):
    return all((not c) or c.startswith("<") for c in row[:2])


def headings(lines):
    return [l[3:].strip() for l in lines if l.startswith("## ")]


def ai_blocks(blk):
    """Check each '### <touchpoint>' block under '## AI touchpoints'."""
    errs, blocks, cur = [], [], None
    for l in blk:
        if l.startswith("## "):
            break
        if l.startswith("### "):
            cur = [l[4:].strip(), []]
            blocks.append(cur)
        elif cur and l.startswith("- "):
            cur[1].append(l[2:])
    if not blocks:
        return ["'## AI touchpoints' has no '### <touchpoint> (<screen>)' block"]
    for name, fields in blocks:
        for f in AI_FIELDS:
            hit = [x for x in fields if x.startswith(f)]
            if not hit:
                errs.append(f"AI touchpoint '{name}' missing '- {f}'")
                continue
            v = hit[0][len(f):].strip()
            if v.startswith("<"):
                continue  # template placeholder
            if not v:
                errs.append(f"AI touchpoint '{name}': '{f}' is blank (write 'not yet known' with a Q id)")
            elif key(v).startswith("not yet known") and not re.search(r"\bQ\d+", v):
                errs.append(f"AI touchpoint '{name}': '{f}' is not yet known with no Q id")
            elif f == AUDIT and not re.match(r"(yes|not yet known)\b", key(v)):
                errs.append(f"AI touchpoint '{name}': accepted suggestions must be audit-logged (Yes: who, what, when, where; or not yet known with a Q id). A No is a gap for H10")
    return errs


def matches(screen_key, row_key):
    """A roles row names a screen, or '<screen>: <action>'."""
    return row_key == screen_key or row_key.startswith(screen_key + ":") or row_key.startswith(screen_key + " (")


def check(path):
    text = Path(path).read_text(encoding="utf-8")
    fm, body, _ = front(text)
    t = fm.get("type")
    if t not in TYPES:
        return None, t, {}
    status = fm.get("status", "draft")
    lines = [norm(l) for l in body.splitlines()]
    errs, info = [], {}

    def need_header(h):
        if h not in lines:
            errs.append(f"table header must be exactly: {h}")
            return False
        return True

    if t == "scope":
        if need_header(HDR["scope_screens"]):
            rows = [r for r in table(lines, HDR["scope_screens"]) if not placeholder(r[1:])]
            cell = lambda r, i: r[i] if len(r) > i else "None"  # noqa: E731
            info["screens"] = [(r[1], cell(r, 5), cell(r, 4)) for r in rows if len(r) >= 2 and r[1]]
            if not rows:
                errs.append("scope lists no screens")
            for r in rows:
                if len(r) < 7 or not r[6] or r[6].startswith("<"):
                    errs.append(f"screen '{r[1] if len(r) > 1 else '?'}' has no Source (a pointer or an A id)")
                if len(r) > 4 and not r[4]:
                    errs.append(f"screen '{r[1]}': 'Data from another system' is blank (write None or the system)")
        need_header(HDR["scope_roles"])
        if "Target viewports" not in headings(lines):
            errs.append("scope missing '## Target viewports'")
        elif need_header(HDR["scope_viewports"]):
            vps = []
            for r in table(lines[lines.index("## Target viewports"):], HDR["scope_viewports"]):
                if placeholder(r) or len(r) < 2:
                    continue
                m = SIZE.search(r[1])
                if not m:
                    errs.append(f"viewport '{r[0]}' size '{r[1]}' should be <width>×<height> in pixels")
                    continue
                vps.append((r[0], int(m.group(1)), int(m.group(2))))
            if not vps:
                errs.append("scope lists no target viewports")
            else:
                info["smallest"] = min(vps, key=lambda v: v[1])
        for h in ("Inherited from Explore", "Out of scope"):
            if h not in headings(lines):
                errs.append(f"scope missing '## {h}'")

    elif t == "feasibility":
        if need_header(HDR["feasibility"]):
            for r in table(lines, HDR["feasibility"]):
                if placeholder(r) or len(r) < 5:
                    continue
                answered = key(r[2]) not in ("", "not yet known")
                if answered and key(r[4]) in ("", "not yet known", "none"):
                    errs.append(f"answered question '{r[0][:50]}' cites no source (engineer answers are sources)")
                if answered and "src" not in r[4] and "§" not in r[4] and not re.search(r"[a-z0-9]_v\d|-v\d", r[4]):
                    errs.append(f"answer to '{r[0][:50]}' should point to the verbatim engineer source")

    elif t == "states":
        if need_header(HDR["states"]):
            got = {}
            for r in table(lines, HDR["states"]):
                if placeholder(r) or len(r) < 2:
                    continue
                if r[1] not in ALL_STATES:
                    errs.append(f"state '{r[1]}' on '{r[0]}' is not one of: {', '.join(ALL_STATES)}")
                got.setdefault(key(r[0]), set()).add(r[1])
            info["states"] = got
            for scr, sts in got.items():
                miss = [s for s in BASE_STATES if s not in sts]
                if miss:
                    errs.append(f"screen '{scr}' is missing base states: {', '.join(miss)}")
                if sts & set(AI_STATES) and not set(AI_STATES) <= sts:
                    errs.append(f"screen '{scr}' has some AI states but not all four: {', '.join(s for s in AI_STATES if s not in sts)}")
            if any(set(AI_STATES) & s for s in got.values()):
                if "AI touchpoints" not in headings(lines):
                    errs.append("screens have AI states but there is no '## AI touchpoints' block")
                else:
                    errs += ai_blocks(lines[lines.index("## AI touchpoints") + 1:])

    elif t == "roles":
        if need_header(HDR["roles"]):
            seen, deny = set(), {}
            for r in table(lines, HDR["roles"]):
                if placeholder(r) or len(r) < 6:
                    continue
                seen.add(key(r[1]))
                for i, col in zip(range(2, 6), ("See", "Change", "Undo", "Approve")):
                    if key(r[i]) not in PERM:
                        errs.append(f"{r[0]} / {r[1]}: {col} = '{r[i]}' (use Yes, No, Own only or not yet known)")
                    elif key(r[i]) == "no":
                        deny.setdefault(key(r[1]), set()).add(r[0])
            info["roles"] = seen
            info["deny"] = deny
        if "If the person who must act is away" not in headings(lines):
            errs.append("roles missing '## If the person who must act is away' (who acts instead, and what happens if nobody is named)")

    elif t == "edge-cases":
        if need_header(HDR["edge-cases"]):
            rows = [r for r in table(lines, HDR["edge-cases"]) if not placeholder(r)]
            cases = {key(r[0]) for r in rows}
            for c in STANDARD_EDGE:
                if not any(c in x for x in cases):
                    errs.append(f"standard edge case '{c}' does not appear")
            info["edge"] = {key(r[1]) for r in rows if len(r) > 1}

    elif t == "accessibility":
        if not any(l.startswith("Standard:") for l in lines):
            errs.append("accessibility needs a 'Standard: ...' line (default WCAG 2.2 AA)")
        if need_header(HDR["accessibility"]):
            rows = [r for r in table(lines, HDR["accessibility"]) if not placeholder(r)]
            for r in rows:
                if len(r) > 2 and r[2] not in ("Pass", "Fail", "Not checked"):
                    errs.append(f"accessibility result '{r[2]}' (use Pass, Fail or Not checked)")
                if len(r) > 4 and r[2] == "Fail" and not r[4]:
                    errs.append(f"'{r[0]}' on '{r[1]}' fails with no fix (add one, or carry it to H10)")
            info["a11y"] = {key(r[1]) for r in rows if len(r) > 1}

    elif t == "tokens":
        hs = headings(lines)
        for h in ("Colour", "Type", "Spacing", "Radius", "Contrast pairs"):
            if h not in hs:
                errs.append(f"tokens missing '## {h}'")
        colours = {}
        for h in ("Colour", "Type", "Spacing", "Radius"):
            if h not in hs:
                continue
            seg = lines[lines.index(f"## {h}"):]
            if HDR["token"] not in seg:
                errs.append(f"'{h}' table header must be exactly: {HDR['token']}")
                continue
            for r in table(seg, HDR["token"]):
                if placeholder(r) or len(r) < 4:
                    continue
                if not re.fullmatch(r"[a-z][a-z0-9-]*", r[0]):
                    errs.append(f"token name '{r[0]}' should be lowercase with hyphens (no leading dashes)")
                if h == "Colour":
                    colours[r[0]] = r[1]
                    if not re.fullmatch(r"#[0-9a-fA-F]{6}", r[1]):
                        errs.append(f"colour '{r[0]}' value '{r[1]}' must be #rrggbb")
                if not r[3] or r[3].startswith("<"):
                    errs.append(f"token '{r[0]}' has no Source")
        if "Contrast pairs" in hs:
            seg = lines[lines.index("## Contrast pairs"):]
            for r in table(seg, HDR["pairs"]):
                if placeholder(r):
                    continue
                for c in r[:2]:
                    if c not in colours:
                        errs.append(f"contrast pair names '{c}', which is not a colour token")

    elif t == "screens":
        raw = text
        if re.search(r"<script[^>]+src\s*=", raw, re.I) or re.search(r"<link[^>]+href\s*=\s*[\"']?(https?:)?//", raw, re.I) \
                or re.search(r"<img[^>]+src\s*=\s*[\"']?(https?:)?//", raw, re.I) or re.search(r"@import\s+url\(", raw, re.I):
            errs.append("screens file is not self-contained (external script, stylesheet or image)")
        visible = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
        steps = re.findall(r"Step\s*(\d+)\s*:\s*([^<\n]+)", visible)
        if not steps:
            errs.append("each screen must be labelled 'Step N: <screen name from scope>'")
        if not re.search(r"State:\s*\w", visible):
            errs.append("each state must be labelled 'State: <name>'")
        if not re.search(r"Viewport:\s*\S", visible):
            errs.append("each screen must show the smallest target viewport, labelled 'Viewport: <name> <width>×<height>'")
        for h in ("Fixes applied in this version", "Design system gaps"):
            if h.lower() not in visible.lower():
                errs.append(f"screens file needs a '{h}' section")
        if re.search(r"\badd-?ons?\b", visible, re.I):
            errs.append("add-ons must stay out of the hardened screens")
        if re.search(r"\bTODO\b", raw) and status in ("review", "final"):
            errs.append("screens file still has TODO text")
        info["html"] = {key(n) for _, n in steps}
        info["html_text"] = key(visible)
        info["viewports"] = {int(w) for w, _ in SIZE.findall(" ".join(re.findall(r"Viewport:[^<\n]*", visible)))}

    elif t == "rulebook-chapter":
        hs = headings(lines)
        for h in CHAPTER:
            if h not in hs:
                errs.append(f"chapter missing '## {h}'")
        if "Rules" in hs:
            i = lines.index("## Rules")
            rules = []
            for l in lines[i + 1:]:
                if l.startswith("## "):
                    break
                if l.startswith("- "):
                    rules.append(l)
            if not rules:
                errs.append("chapter has no rules")
            ids = []
            for l in rules:
                m = re.match(r"^- (R\d+) \((must|must not)\): .+", l)
                if not m:
                    errs.append(f"rule not in the form '- R<n> (must|must not): ... src: ...': {l[:60]}")
                    continue
                ids.append(m.group(1))
                if "src:" not in l and "(retired" not in l:
                    errs.append(f"{m.group(1)} has no 'src:' (every rule traces to a decision, insight or source)")
            dup = {x for x in ids if ids.count(x) > 1}
            if dup:
                errs.append(f"rule ids reused: {', '.join(sorted(dup))}")

    elif t == "rulebook-check":
        if need_header(HDR["rulebook-check"]):
            for r in table(lines, HDR["rulebook-check"]):
                if placeholder(r) or len(r) < 5:
                    continue
                if r[2] not in ("Pass", "Break", "Not applicable"):
                    errs.append(f"result '{r[2]}' for {r[0]} (use Pass, Break or Not applicable)")
                if r[2] == "Break" and not re.match(r"^(Fixed in screens v\d+|Ship note SN\d+|Send back|Rule conflict Q\d+)$", r[4]):
                    errs.append(f"Break on {r[0]} ({r[1]}) needs an action: Fixed in screens v<n>, Ship note SN<n>, Send back, or Rule conflict Q<n>")
                if not re.match(r".+\bR\d+$", r[0]):
                    errs.append(f"rule reference '{r[0]}' should be '<chapter topic> R<n>'")

    elif t == "checklist":
        if need_header(HDR["checklist"]):
            rows = table(lines, HDR["checklist"])
            items = [re.sub(r"^\d+\.\s*", "", r[0]) for r in rows]
            for it in CHECK_ITEMS:
                if it not in items:
                    errs.append(f"checklist missing item: {it}")
            for r in rows:
                if len(r) > 1 and r[1] and r[1] not in ("Pass", "Gap", "Not applicable"):
                    errs.append(f"checklist result '{r[1]}' (use Pass, Gap or Not applicable)")
                if status in ("review", "final") and (len(r) < 3 or not r[1] or not r[2]):
                    errs.append(f"checklist item '{r[0][:40]}' needs a result and evidence before review")

    elif t == "ship-notes":
        hs = headings(lines)
        for h in ("Fixes travelling to Ship", "API and data assumptions", "Open questions for Ship", "Out of scope"):
            if h not in hs:
                errs.append(f"ship-notes missing '## {h}'")
        if need_header(HDR["ship-notes"]):
            for r in table(lines, HDR["ship-notes"]):
                if r and r[0] and not re.fullmatch(r"SN\d+", r[0]):
                    errs.append(f"Ship note id '{r[0]}' should be SN<n> (S<n> reads like a Ship step)")

    elif t == "hardened-design":
        j = "\n".join(lines).lower()
        for kw in ("screens", "tokens", "checklist", "rulebook check", "ship notes"):
            if kw not in j:
                errs.append(f"hardened-design should link the {kw}")

    return errs, t, info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--scope", help="scope artefact; turns on the every-screen coverage check")
    a = ap.parse_args()
    files = []
    for p in a.paths:
        p = Path(p)
        if p.is_dir():
            files += sorted(x for x in list(p.rglob("*.md")) + list(p.rglob("*.html"))
                            if not ({"templates", "superseded", "sources"} & set(x.parts)))
        else:
            files.append(p)
    bad = n = 0
    seen = {}
    for f in files:
        r, t, info = check(f)
        if r is None:
            continue
        n += 1
        seen.setdefault(t, []).append(info)
        for e in r:
            print(f"ERROR {f}: {e}")
        bad += len(r)
        print(f"[{'FAIL' if r else 'ok'}] {f}")

    last = lambda typ: seen.get(typ, [{}])[-1]  # noqa: E731
    if "states" in seen and "roles" in seen:
        sts_all = last("states").get("states", {})
        for rk, who in sorted(last("roles").get("deny", {}).items()):
            hit = [s for s in sts_all if matches(s, rk)]
            for s in hit:
                if "No permission" not in sts_all[s]:
                    bad += 1
                    print(f"ERROR states: '{s}' needs a No permission state ({', '.join(sorted(who))} has a No in roles for '{rk}')")

    if a.scope:
        sr, st, sinfo = check(a.scope)
        if st != "scope":
            print(f"ERROR --scope {a.scope} is not a scope artefact")
            bad += 1
        else:
            screens = sinfo.get("screens", [])
            print(f"Coverage against {len(screens)} screens in {Path(a.scope).name}:")
            for scr, ai, other in screens:
                k = key(scr)
                miss = []
                if "states" in seen:
                    sts = last("states").get("states", {}).get(k, set())
                    need = BASE_STATES + (["Partial"] if key(other) not in ("none", "", "no") else []) \
                        + (AI_STATES if key(ai) not in ("none", "", "no") else [])
                    lack = [s for s in need if s not in sts]
                    if lack:
                        miss.append("states: " + ", ".join(lack))
                if "roles" in seen and not any(matches(k, rk) for rk in last("roles").get("roles", set())):
                    miss.append("roles")
                if "edge-cases" in seen and k not in last("edge-cases").get("edge", set()):
                    miss.append("edge-cases")
                if "accessibility" in seen and k not in last("accessibility").get("a11y", set()):
                    miss.append("accessibility")
                if "screens" in seen and k not in last("screens").get("html", set()):
                    miss.append("screens HTML (no 'Step N: " + scr + "')")
                if miss:
                    bad += 1
                    print(f"ERROR coverage: '{scr}' missing from {'; '.join(miss)}")
                else:
                    print(f"  [ok] {scr}")
            small = sinfo.get("smallest")
            if small and "screens" in seen:
                if small[1] in last("screens").get("viewports", set()):
                    print(f"  [ok] smallest target viewport shown: {small[0]} {small[1]}×{small[2]}")
                else:
                    bad += 1
                    print(f"ERROR coverage: hardened screens do not show the smallest target viewport "
                          f"({small[0]} {small[1]}×{small[2]}); label it 'Viewport: {small[0]} {small[1]}×{small[2]}'")
            not_checked = [x for x in ("states", "roles", "edge-cases", "accessibility", "screens") if x not in seen]
            if not_checked:
                print(f"Note: no {', '.join(not_checked)} artefact among the files checked, so coverage for it was not tested.")
    print(f"Checked {n} Harden artefacts; {bad} errors.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
