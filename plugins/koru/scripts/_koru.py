"""Shared helpers for the koru orchestrator scripts.

The orchestrator holds no rules of its own. It finds koru-core and the phase skills, reads the
engagement's read-me, and calls core's scripts. Everything it checks is defined by koru-core.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent  # plugins/koru
DONE = ("passed", "skipped")


def skill_roots():
    """Folders that may hold koru-core and phase skills, in search order."""
    roots = []
    env = os.environ.get("KORU_SKILLS_PATH")
    if env:
        roots += [Path(p).expanduser() for p in env.split(os.pathsep) if p]
    roots.append(PLUGIN / "skills")                   # the plugin's own skills
    roots.append(Path.home() / ".claude" / "skills")  # personal skills (a team's extra phase skills)
    seen, out = set(), []
    for r in roots:
        r = r.resolve()
        if r not in seen and r.is_dir():
            seen.add(r)
            out.append(r)
    return out


def find_skill(name):
    for r in skill_roots():
        d = r / name
        if (d / "SKILL.md").is_file():
            return d
    return None


def core_dir():
    d = find_skill("koru-core")
    if not d or not (d / "scripts" / "check_roles.py").is_file():
        sys.exit("ERROR: koru-core is not installed next to this skill or in ~/.claude/skills. Install it first.")
    return d


def core_version(core):
    m = re.search(r"\*\*Version:\*\*\s*koru-core v(\d+)", (core / "SKILL.md").read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def run_core(core, script, *args):
    """Run a koru-core script in isolated mode. Returns (exit code, combined output)."""
    p = subprocess.run([sys.executable, "-I", str(core / "scripts" / script), *map(str, args)],
                       capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def is_engagement(path):
    return (path / "00-read-me-first.md").is_file() and (path / ".koru" / "project.json").is_file()


def find_engagements(start):
    """Engagement folders at or below start (max depth 4), skipping hidden and vendor folders."""
    start = Path(start).expanduser().resolve()
    if is_engagement(start):
        return [start]
    found = []
    for root, dirs, _ in os.walk(start):
        depth = len(Path(root).relative_to(start).parts)
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "venv", ".venv")]
        if depth >= 4:
            dirs[:] = []
        if is_engagement(Path(root)):
            found.append(Path(root))
            dirs[:] = []
    return sorted(found)


def load_json(p, default=None):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else default


def section_table(text, heading, with_header=False):
    """Rows (list of cells) of the first table under a '## heading' line. Header row excluded
    unless with_header is true (then it is the first row)."""
    lines = text.splitlines()
    try:
        i = next(n for n, l in enumerate(lines) if re.match(rf"^##\s+{re.escape(heading)}\s*$", l, re.I))
    except StopIteration:
        return []
    rows, started, header_seen = [], False, False
    for l in lines[i + 1:]:
        if l.startswith("## "):
            break
        if l.strip().startswith("|"):
            started = True
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if not header_seen:
                header_seen = True
                if not with_header:
                    continue
            rows.append(cells)
        elif started:
            break
    return rows


def stage_table(readme_text):
    """[{title, skill, status, lead, card}] in read-me order."""
    out = []
    for c in section_table(readme_text, "Stages"):
        c += [""] * (5 - len(c))
        out.append({"title": c[0], "skill": c[1], "status": c[2].lower(), "lead": c[3], "card": c[4]})
    return out


def step_tracker(readme_text, title):
    """[{step, status, checker, date}] for '## <title> step tracker'. Columns are found by their
    header names, so phases may add columns (Harden adds "Who")."""
    rows = section_table(readme_text, f"{title} step tracker", with_header=True)
    if not rows:
        return []
    head = [h.strip().lower() for h in rows[0]]
    col = lambda name, default: head.index(name) if name in head else default
    i_step, i_status, i_checker, i_date = col("step", 0), col("status", 1), col("checker", 2), col("date", 3)
    out = []
    for c in rows[1:]:
        c = c + [""] * (max(i_step, i_status, i_checker, i_date) + 1 - len(c))
        out.append({"step": c[i_step], "status": c[i_status].lower(), "checker": c[i_checker], "date": c[i_date]})
    return out


def stage_key(title):
    return title.strip().lower()
