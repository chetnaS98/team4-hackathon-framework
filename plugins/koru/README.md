# koru: the Koru delivery playbook

Runs an engagement through **Frame → Explore → Harden → Ship** from one command. Claude drafts; named people check and sign off; nothing a person hasn't signed becomes project knowledge.

## Install

In Claude Code, from this repo:

```
/plugin marketplace add ./
/plugin install koru@team4-koru
```

Or from GitHub: `/plugin install koru --marketplace chetnaS98/team4-hackathon-framework`. Restart Claude Code after installing.

## Use

| Command | What it does |
|---|---|
| `/koru:next` | The only one you need. First time: asks the intake questions and sets the project up. After that: runs the next step, or hands a finished stage on to the next. |
| `/koru:status` | Where the engagement is, without changing anything |
| `/koru:break` | Log something that broke or needed a workaround |
| `/koru:change` | Log a change to the playbook itself, with the reason |

## How it fits together

- **koru-core** (skill): the shared rules, file naming, logs, registers, roles gate and stale-check. Every stage skill loads it first.
- **Stage skills**: `koru-frame` (framed brief and research pack), `koru-explore` (directions, two ideas, Design v1), `koru-harden` (states, roles, edge cases, accessibility, feasibility, rulebook checks), `koru-ship` (HTML deliverable with a guided walkthrough, tickets, handoff note).
- **Reviewer agents** (fresh context, read-only or own report only): `evidence-auditor` (Frame 5 and 7), `feasibility-engineer` (Harden H3, a pre-check before the real engineer), `hardening-critic` (Harden after H7), `handoff-reviewer` (Ship, cold read before the engineer).
- **Scripts** (`scripts/`): `route.py` decides the next action; `intake.py` sets a project up; `step.py` records step status (a pass needs a named checker); `signoff.py` promotes a draft to final after the checks; `advance_stage.py` hands a stage on; `log.py` writes the break and playbook-change logs.
- **Hooks**: a guard blocks editing sources, overwriting finals and putting unsigned files in final folders; a session-start hook shows the engagement's status; an agent hook keeps reviewer agents in the foreground and, when one reports, tells the session to fold the findings in and record progress. If an agent is launched in the background anyway, the hook says it has not reported yet, so the session records the step as waiting instead of moving on.
- **Progress inside a step**: `step.py --note` and `--waiting-on` keep a one-line note per open step in `.koru/progress.json`. `route.py` shows it, and says `CHECK` (ask the named checker for one verdict) instead of re-running a step that is waiting on its checker.
- **Optional steps**: each stage's `stage.json` lists them with a default skip reason (Frame 8, 9, 10, 11, 14b, 20; Explore A6, A15; Harden H13). `route.py` says `OPTIONAL` and the team lead decides; `step.py --skip-optional --by <name> [--keep 14b]` skips them in one go. Other steps can only be skipped as a logged override.
- **Ship checkpoints**: Ship has three hard stops where people decide, not Claude. S2: the design lead and the engineer agree the 3 to 5 user stories before anything is built. S3: someone new to the flow takes the deliverable's walkthrough, their words are recorded as a source, and the design lead confirms. S7: the named engineer reviews and signs the handoff.
- **Guided walkthrough (Intro.js)**: the Ship HTML deliverable carries an Intro.js tour of its features and interactions for a new user (a "Take the tour" button; steps kept as JSON in the page). Intro.js 7.2.0 from cdnjs is the one external script allowed; if it can't load, the button hides and the page still works. `lint_ship.py` checks every tour step points at a real element. Intro.js is AGPL or paid commercial, so the design lead confirms the licence per client (`koru-ship/references/client-setup.md`); how to write the tour is in `koru-ship/references/walkthrough.md`.
- **Ship iterations**: each handoff to the build team is an iteration with its own card (`<project>-ship-handoff-card-v1.md`, `-v2.md`, ...) and export folder (`07-ship/export/iteration-<n>/`). `iteration.py --by <name> --reason <feedback>` starts the next round after a handoff; from round 2 the handoff note needs a "What changed since iteration n" section. Nothing earlier is overwritten.

## Where things live (inside an engagement folder)

`00-read-me-first.md` (project, roles, stage table, step trackers) · `01-framed-brief/` `02-research/` (Frame finals) · `03-rulebook/` `04-design-library/` `08-harden/` (Harden finals) · `06-explore/` (Explore finals) · `07-ship/` (Ship finals) · `05-decisions-log.md`, `ai-quality-log.md`, `break-log.md`, `playbook-changes.md` · registers · `handoff-cards/` · `stages/<stage>/drafts/` and `stages/<stage>/sources/`.

Only `-final` files in the numbered folders go into Claude project knowledge. The **context keeper** uploads them and runs the stale-check rhythm.

## Tickets without Jira

Ship writes each ticket as markdown in the workbook template, plus `tickets.csv` in Jira's import format (anyone with Jira imports it in one step) and a combined `tickets.md`. GitHub Issues are optional once `gh auth login` is done, and are only created after you confirm.
