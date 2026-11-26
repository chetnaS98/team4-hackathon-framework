"""Shared helpers for the Frame intent pipeline: folder layout, artefact naming/versioning,
front matter reading and the break log.

Folder layout of one project's Frame stage (paths are relative to this folder):
  <project>/frame/
    00-raw/          transcripts + manifest.json (human-provided)
    01-clean/        formatter output (.md per session, verbatim + sections)
    02-synthesis/    <project>-frame-synthesis-vN-<status>.json
    03-ledger/       ledger (next step)
    04-audit/        audit, gap report, open questions (step after)
    break-log.md     every stopped run, appended
    decisions-log.md every human sign-off, appended
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ("draft", "review", "final")
SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "markdown-research-formatter" / "scripts"


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def artefact_name(project, stage, artefact, version, status, ext):
    return f"{project}-{stage}-{artefact}-v{version}-{status}.{ext}"


def output_path(folder, project, stage, artefact, ext):
    """Where to write a new draft. Overwrites the latest version only if it is still a draft;
    if the latest is in review or final, starts the next version. A final file is never touched."""
    folder = Path(folder)
    pat = re.compile(rf"^{re.escape(project)}-{re.escape(stage)}-{re.escape(artefact)}-v(\d+)-({'|'.join(STATUSES)})\.{ext}$")
    found = []
    if folder.is_dir():
        for f in folder.iterdir():
            m = pat.match(f.name)
            if m:
                found.append((int(m.group(1)), m.group(2), f))
    if not found:
        return folder / artefact_name(project, stage, artefact, 1, "draft", ext), 1
    ver, status, f = max(found, key=lambda x: (x[0], STATUSES.index(x[1])))
    if status == "draft" and not any(v == ver and s != "draft" for v, s, _ in found):
        return f, ver
    return folder / artefact_name(project, stage, artefact, ver + 1, "draft", ext), ver + 1


def write_break(frame_dir, step, errors, inputs=None):
    """Append one entry to break-log.md. The run must stop after this; the next step never guesses."""
    log = Path(frame_dir) / "break-log.md"
    new = not log.exists()
    with open(log, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Break log\n\nEvery run the pipeline stopped, newest last. "
                     "Fix the cause, then re-run the step.\n")
        fh.write(f"\n## {now_iso()} | {step} | contract failed\n\n")
        if inputs:
            fh.write(f"Inputs: {', '.join(str(i) for i in inputs)}\n\n")
        for e in errors:
            fh.write(f"- {e}\n")
        fh.write("\nNext step was not run.\n")
    return log


def read_front_matter(md_path):
    """Return (front_matter_dict, body_lines, body_start_line_1based)."""
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required: pip3 install -r requirements.txt")
    text = Path(md_path).read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{md_path}: no front matter")
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if end is None:
        raise ValueError(f"{md_path}: front matter not closed")
    fm = yaml.safe_load("\n".join(lines[1:end])) or {}
    return fm, lines, end + 2


def rel(path, base):
    try:
        return str(Path(path).resolve().relative_to(Path(base).resolve()))
    except ValueError:
        return str(path)


def dump_json(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
