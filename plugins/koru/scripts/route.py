#!/usr/bin/env python3
"""Decide what the koru orchestrator does next for an engagement.

Usage:
  python route.py [--engagement <folder>] [--search <folder>] [--json]

Finds the engagement (a folder with 00-read-me-first.md and .koru/), reads its stage table and the
active stage's step tracker, runs koru-core's roles gate and stale-check, checks that the phase skill
is installed, and prints one ACTION:

  NEW        no engagement found: set one up (init_engagement, then init_stage for the first stage)
  CHOOSE     several engagements found: ask which one
  START      no stage active: start the next stage with init_stage
  BLOCKED    something must be fixed by a person first (roles, missing phase skill, core version)
  DISPATCH   invoke the phase skill for the next step
  HANDOFF    every step of the active stage is passed or skipped: run advance_stage.py
  DONE       every stage is handed off

Exit 0 always (the action is the answer); exit 2 on a usage error.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _koru as k  # noqa: E402


def decide(eng, core):
    text = (eng / "00-read-me-first.md").read_text(encoding="utf-8")
    proj = k.load_json(eng / ".koru" / "project.json", {})
    stages = k.stage_table(text)
    out = {"engagement": str(eng), "project": proj.get("project"), "stages": stages, "reasons": []}

    cv = k.core_version(core)
    if cv is not None and proj.get("core_version") not in (None, cv):
        out.update(action="BLOCKED", reasons=[f"engagement expects koru-core v{proj.get('core_version')}, installed core is v{cv}"])
        return out

    active = [s for s in stages if s["status"] == "active"]
    if len(active) > 1:
        out["reasons"].append("more than one stage is active: " + ", ".join(s["title"] for s in active) + " (routing to the earliest)")

    if not active:
        nxt = next((s for s in stages if s["status"] == "not started"), None)
        if nxt is None:
            out["action"] = "DONE"
            return out
        d = k.find_skill(nxt["skill"]) if nxt["skill"] else None
        out.update(stage=nxt["title"], skill=nxt["skill"], skill_dir=str(d) if d else None)
        if not d or not (d / "stage.json").is_file():
            out.update(action="BLOCKED", reasons=[f"stage {nxt['title']} has no installed phase skill ({nxt['skill'] or 'none named'}). It is not built yet; do not improvise its process."])
        else:
            out["action"] = "START"
        return out

    cur = active[0]
    d = k.find_skill(cur["skill"]) if cur["skill"] else None
    out.update(stage=cur["title"], skill=cur["skill"], skill_dir=str(d) if d else None)

    rc, roles_out = k.run_core(core, "check_roles.py", eng)
    sc, stale_out = k.run_core(core, "stale_check.py", "--engagement", eng)
    out["roles_gate"] = {"passed": rc == 0, "output": roles_out}
    out["stale_check"] = {"clean": sc == 0, "output": stale_out}

    tracker = k.step_tracker(text, cur["title"])
    out["tracker"] = tracker
    open_steps = [t for t in tracker if t["status"] not in k.DONE]
    in_progress = next((t for t in open_steps if t["status"] in ("drafted", "in check")), None)
    nxt = in_progress or (open_steps[0] if open_steps else None)
    out["next_step"] = nxt

    if not d:
        out["action"] = "BLOCKED"
        out["reasons"].append(f"phase skill '{cur['skill']}' for {cur['title']} is not installed")
    elif rc != 0:
        out["action"] = "BLOCKED"
        out["reasons"].append("roles gate failed: name the missing owners in 00-read-me-first.md")
    elif not tracker:
        out["action"] = "BLOCKED"
        out["reasons"].append(f"no '{cur['title']} step tracker' table in the read-me")
    elif nxt is None:
        out["action"] = "HANDOFF"
    else:
        out["action"] = "DISPATCH"
    if sc != 0:
        out["reasons"].append("stale-check has warnings: no artefact may be marked final until they are cleared")
    return out


def render(o):
    lines = []
    if o.get("engagement"):
        lines.append(f"Engagement: {o.get('project')} ({o['engagement']})")
    if o.get("stages"):
        lines.append("Stages: " + " · ".join(f"{s['title']} {s['status']}" for s in o["stages"]))
    if o.get("stage"):
        lines.append(f"Current stage: {o['stage']} (skill: {o.get('skill') or '-'}{'' if o.get('skill_dir') else ', NOT INSTALLED'})")
    if "roles_gate" in o:
        lines.append("Roles gate: " + ("passed" if o["roles_gate"]["passed"] else "FAILED"))
        if not o["roles_gate"]["passed"]:
            lines += ["  " + l for l in o["roles_gate"]["output"].splitlines()[1:]]
    if "stale_check" in o:
        lines.append("Stale-check: " + ("clean" if o["stale_check"]["clean"] else "WARNINGS"))
        if not o["stale_check"]["clean"]:
            lines += ["  " + l for l in o["stale_check"]["output"].splitlines()[1:12]]
    if o.get("tracker"):
        done = sum(1 for t in o["tracker"] if t["status"] in k.DONE)
        lines.append(f"Steps: {done}/{len(o['tracker'])} passed or skipped")
    if o.get("next_step"):
        n = o["next_step"]
        lines.append(f"Next step: {n['step']} ({n['status']})")
    for r in o.get("reasons", []):
        lines.append(f"Note: {r}")
    if o.get("candidates"):
        lines += ["Engagements found:"] + [f"  - {c}" for c in o["candidates"]]
    lines.append(f"ACTION: {o['action']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engagement")
    ap.add_argument("--search", default=".")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    core = k.core_dir()

    if a.engagement:
        eng = Path(a.engagement).expanduser().resolve()
        if not k.is_engagement(eng):
            print(f"ERROR: {eng} is not a koru engagement (no 00-read-me-first.md and .koru/)", file=sys.stderr)
            sys.exit(2)
        o = decide(eng, core)
    else:
        found = k.find_engagements(a.search)
        if not found:
            o = {"action": "NEW", "reasons": [f"no koru engagement at or below {Path(a.search).resolve()}"]}
        elif len(found) > 1:
            o = {"action": "CHOOSE", "candidates": [str(f) for f in found]}
        else:
            o = decide(found[0], core)
    print(json.dumps(o, indent=2) if a.json else render(o))


if __name__ == "__main__":
    main()
