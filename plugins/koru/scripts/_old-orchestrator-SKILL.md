---
name: koru
description: Master entry point for a Koru engagement (Frame, Explore, Harden, Ship). Works out where the engagement is, runs koru-core's gates, and hands the work to the right phase skill (koru-frame and its successors); hands a finished stage off and starts the next. Use it whenever someone says "koru", "where are we", "what's next", "next step", "carry on", "resume the engagement", "hand off to Explore", "start the next stage", "set up a new koru engagement", or asks for the status of a Koru project, even if they don't name a stage. It does no step work itself and holds no rules: the rules are koru-core's, the steps are each phase skill's.
---

# koru: the orchestrator

This skill is the single entry point. It answers one question every time it runs: **what happens next, and which skill does it?** It never does step work and never restates a rule. The rules, file protocol, logs and integrity checks are **koru-core**'s. The steps are each **phase skill**'s (`koru-frame` today; `koru-explore`, `koru-harden`, `koru-ship` when built).

```
you ──> koru (route) ──gates──> koru-core scripts (roles gate, stale-check)
                      ──dispatch──> phase skill (koru-frame …) ──loads──> koru-core rules
                      ──handoff──> advance_stage.py ──> koru-core init_stage (next stage)
```

## Every time you run

1. **Route.** Run from the repo root:
   ```bash
   python3 -I .claude/skills/koru/scripts/route.py [--engagement <folder>]
   ```
   Without `--engagement` it searches the working folder for engagements (a folder holding `00-read-me-first.md` and `.koru/`). Show the user its summary in a few lines, then act on its `ACTION`.
2. **Act on the action** (below). Do exactly one action per turn unless the user asks you to continue.
3. **After a phase skill finishes a step**, run `route.py` again and show the new state in one or two lines.

## Actions

| ACTION | What you do |
|---|---|
| `NEW` | No engagement. Ask for the project code name (lowercase, never the client's real name), the parent folder and the engagement size. Run koru-core's `init_engagement.py`, then `init_stage.py` for the first stage in the stage table. Then route again (it will say BLOCKED on roles). |
| `CHOOSE` | Several engagements. List them and ask which one. Pass it as `--engagement` from then on. |
| `BLOCKED` | Say each reason in plain words and what unblocks it. For a failed roles gate, ask the user for the missing names in one message and write **only the names they give** into the read-me's Roles and Client sections; never invent or assume a name. For a missing phase skill, say the stage is not built yet and stop; do not improvise its process. |
| `START` | No stage active and the next one's phase skill is installed. Confirm with the user, run koru-core `init_stage.py --engagement <e> --stage-dir <skill_dir>`, then route again. |
| `DISPATCH` | Invoke the phase skill with the Skill tool, passing `engagement=<path> step=<next step>`. The phase skill loads koru-core itself and runs core's step loop (announce, do, write, hand to checker, record). Do not run several steps unless the user asks to draft ahead. |
| `HANDOFF` | Every step of the active stage is passed or skipped. Run `advance_stage.py --engagement <e> --dry-run` and show the result. If it refuses, say what is missing and, where a phase skill owns the fix (for example the handoff card or the final files), dispatch to it. If it passes, ask a named person to confirm the handoff, then run it with `--confirmed-by "<their name>"`. |
| `DONE` | Every stage is handed off. Say so; offer the stale-check or a send-back if something changed. |

Stale-check warnings never block a step, but they block anything becoming `final`. Always report them; when the user is about to sign off, say the sign-off cannot happen until they are cleared.

## Requests that are not "next step"

- **"Status" / "where are we"**: route only; do not dispatch.
- **"Run the stale-check" / "check roles"**: run that koru-core script directly and report.
- **A send-back** (a later stage changes an earlier output): follow koru-core's send-back protocol (`references/registers.md`), then dispatch to the phase skill that **owns** the earlier artefact, not the current stage's.
- **A request for a specific step or stage**: check the route first; if it would skip an unfinished step or a failed gate, say so and let the user decide. A person decides overrides and koru-core says how to log them.

## Handoff checks (what `advance_stage.py` enforces)

All are koru-core rules applied at the stage boundary: every step passed or skipped; roles gate passes; stale-check clean; the handoff card `handoff-cards/<project>-<stage>-handoff-card.md` exists with every row filled except "Checked by the next stage"; the stage's final folders hold only `final` artefacts (at least one); a sign-off line for the stage is in the decisions log; and a named person confirms. On success it logs the handoff, marks the stage `handed off`, and starts the next stage if its phase skill is installed.

## Finding skills

The scripts look for `koru-core` and phase skills next to this skill (`.claude/skills/`), then in `~/.claude/skills`, then in any folder listed in `KORU_SKILLS_PATH`. A phase skill counts as installed when it has `SKILL.md` and `stage.json`.

## Living next to the other frameworks in this repo

A koru engagement is identified by `.koru/`. This skill ignores koru-ai-dlc projects (`koru-state.md`) and the repo's `framework/` projects (`state.md`). Don't mix their files into a koru engagement.
