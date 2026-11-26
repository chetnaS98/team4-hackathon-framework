#!/usr/bin/env python3
"""Hooks around the koru reviewer agents (evidence-auditor, feasibility-engineer, hardening-critic, handoff-reviewer).

PreToolUse (Agent): refuses to launch a koru reviewer in the background. A background agent reports back later as
  a separate message, the user ends up talking to the agent instead of the main session, and the step stalls.
  In the foreground the report comes back as the tool result, in the same turn, and the step carries on.
PostToolUse (Agent): when a koru reviewer returns, puts the engagement's position and the next moves in context,
  so the main session folds the findings in and records progress (step.py --note) instead of stopping.

Prints nothing and allows everything for other agents and outside a koru engagement.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _koru as k  # noqa: E402

REVIEWERS = {"evidence-auditor", "feasibility-engineer", "hardening-critic", "handoff-reviewer"}


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    ti = data.get("tool_input") or {}
    agent = str(ti.get("subagent_type") or "").split(":")[-1]
    if agent not in REVIEWERS:
        return
    event = data.get("hook_event_name", "")
    if event == "PreToolUse":
        if ti.get("run_in_background"):
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "deny",
                "permissionDecisionReason": f"koru: run {agent} in the foreground (run_in_background false) so its report "
                "comes back in this turn and the step continues. Before launching, record progress: step.py --step <id> "
                f"--status drafted --note \"{agent} running\"."}}))
        return
    if event != "PostToolUse":
        return
    found = k.find_engagements(Path(data.get("cwd") or ".").resolve())
    status = ""
    if len(found) == 1:
        r = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "route.py"), "--engagement", str(found[0])],
                           capture_output=True, text=True, timeout=60)
        status = "\n".join(l for l in r.stdout.splitlines() if l.startswith(("Engagement", "Next step", "Progress", "Waiting", "ACTION")))
    ctx = (f"koru: the {agent} has reported. It only reports; the step is not finished and nobody has passed it. "
           "Continue the same step now, in this turn, without asking the user to talk to the agent:\n"
           "1. Spot-check its main findings against the sources; fold the accepted ones into NEW versions of the drafts "
           "(old versions to superseded/; the review file lists what it audited under `reviews:`).\n"
           "2. Run the lints and the stale-check.\n"
           "3. Record it: step.py --step <id> --status \"in check\" --waiting-on \"<named checker>\" --note \"<one line: what is done>\".\n"
           "4. Ask the named checker for ONE verdict (pass, or changes). Ask any other decision separately.\n"
           + (f"Current position:\n{status}" if status else ""))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}}))


if __name__ == "__main__":
    main()
