---
description: Show where the Koru engagement is (stage, step, gates, stale-check) without doing anything
argument-hint: "[engagement folder]"
---

Run `python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/route.py" $ARGUMENTS` and report in a few lines: the stage table, the active stage's progress and next step, the roles gate, the stale-check warnings (with the order to revise), and the open rows in `break-log.md` and `open-questions-register.md`. Do not dispatch or change anything. End with: "Run /koru:next to continue."
