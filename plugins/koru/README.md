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
- **Stage skills**: `koru-frame` (framed brief and research pack), `koru-explore` (directions, two ideas, Design v1), `koru-harden` (states, roles, edge cases, accessibility, feasibility, rulebook checks), `koru-ship` (HTML deliverable with a guided walkthrough, an optional React starter, tickets, handoff note).
- **Reviewer agents** (fresh context, read-only or own report only): `evidence-auditor` (Frame 5 and 7), `feasibility-engineer` (Harden H3, a pre-check before the real engineer), `hardening-critic` (Harden after H7), `handoff-reviewer` (Ship, cold read before the engineer).
- **Scripts** (`scripts/`): `route.py` decides the next action; `intake.py` sets a project up; `step.py` records step status (a pass needs a named checker); `signoff.py` promotes a draft to final after the checks; `advance_stage.py` hands a stage on; `log.py` writes the break and playbook-change logs.
- **Hooks**: a guard blocks editing sources, overwriting finals and putting unsigned files in final folders; a session-start hook shows the engagement's status; an agent hook keeps reviewer agents in the foreground and, when one reports, tells the session to fold the findings in and record progress. If an agent is launched in the background anyway, the hook says it has not reported yet, so the session records the step as waiting instead of moving on.
- **Progress inside a step**: `step.py --note` and `--waiting-on` keep a one-line note per open step in `.koru/progress.json`. `route.py` shows it, and says `CHECK` (ask the named checker for one verdict) instead of re-running a step that is waiting on its checker.
- **Optional steps**: each stage's `stage.json` lists them with a default skip reason (Frame 8, 9, 10, 11, 14b, 20; Explore A6, A15; Harden H13). `route.py` says `OPTIONAL` and the team lead decides; `step.py --skip-optional --by <name> [--keep 14b]` skips them in one go. Other steps can only be skipped as a logged override.
- **Ship checkpoints**: Ship has three hard stops where people decide, not Claude. S2: the design lead and the engineer agree the 3 to 5 user stories before anything is built. S3: someone new to the flow takes the deliverable's walkthrough, their words are recorded as a source, and the design lead confirms. S7: the named engineer reviews and signs the handoff.
- **Guided walkthrough (Intro.js)**: the Ship HTML deliverable carries an Intro.js tour of its features and interactions for a new user (a "Take the tour" button; steps kept as JSON in the page). Intro.js 7.2.0 from cdnjs is the one external script allowed; if it can't load, the button hides and the page still works. `lint_ship.py` checks every tour step points at a real element. Intro.js is AGPL or paid commercial, so the design lead confirms the licence per client (`koru-ship/references/client-setup.md`); how to write the tour is in `koru-ship/references/walkthrough.md`.
- **React starter (optional, S3b)**: when the engineer asks for it and the client builds in React, Ship also makes a small Vite + React 18 + TypeScript project of the core flow: one component per screen, the deliverable's anchors and states, Harden's `tokens.css` verbatim, sample data only. It is a reference, not production code; the HTML deliverable stays the reference. `lint_ship.py` checks it, Claude never installs packages (the design engineer runs `npm install` and `npm run build`), and sign-off promotes the whole folder to `07-ship/` without `node_modules/`.
- **Ship iterations**: each handoff to the build team is an iteration with its own card (`<project>-ship-handoff-card-v1.md`, `-v2.md`, ...) and export folder (`07-ship/export/iteration-<n>/`). `iteration.py --by <name> --reason <feedback>` starts the next round after a handoff; from round 2 the handoff note needs a "What changed since iteration n" section. Nothing earlier is overwritten.

## Site map

What's in the plugin, and where to look for each thing.

```
.claude-plugin/marketplace.json      (repo root) makes this repo the team4-koru marketplace
plugins/koru/
├── .claude-plugin/plugin.json       plugin name, version, description
├── README.md                        this file
├── docs/koru-flow.html              the whole flow on one page, stage by stage
├── commands/                        what you type
│   ├── next.md                      /koru:next   intake the first time, then the next step
│   ├── status.md                    /koru:status where things stand, changes nothing
│   ├── break.md                     /koru:break  log something that broke
│   └── change.md                    /koru:change log a change to the playbook
├── agents/                          independent reviewers; they report, people decide
│   ├── evidence-auditor.md          Frame steps 5 and 7
│   ├── feasibility-engineer.md      Harden H3, before the real engineer
│   ├── hardening-critic.md          Harden, after H7
│   └── handoff-reviewer.md          Ship S6, cold read before the engineer
├── hooks/                           run automatically
│   ├── hooks.json                   wires the hooks to Claude Code events
│   ├── guard.py                     blocks editing sources, overwriting finals, unsigned files in final folders
│   ├── session_start.py             shows the engagement's status when a session opens
│   └── agent_done.py                keeps reviewer agents in the foreground; folds their findings in
├── scripts/                         the rules that must hold every time
│   ├── route.py                     decides the next action (NEW, START, DISPATCH, CHECK, OPTIONAL, HANDOFF ...)
│   ├── intake.py                    sets a project up from the intake answers
│   ├── step.py                      records step status, notes, waiting-on, skips (a pass needs a named checker)
│   ├── signoff.py                   promotes a draft to final after the checks (a starter folder as a whole)
│   ├── advance_stage.py             hands a finished stage on to the next
│   ├── iteration.py                 starts the next Ship round (handoff v2, v3 ...)
│   ├── log.py                       writes the break and playbook-change logs
│   └── _koru.py                     shared helpers
└── skills/
    ├── koru-core/                   shared by every stage: rules, naming, logs, registers, roles
    │   ├── SKILL.md
    │   ├── references/              file protocol, governance, integrity, registers, defaults ...
    │   ├── assets/templates/        read-me, logs, registers, handoff card shell
    │   ├── registry/roles.json      the roles every stage needs
    │   └── scripts/                 init_engagement, init_stage, check_roles, lint_core,
    │                                lint_lines, stale_check, build_registry
    ├── koru-frame/                  stage 1: framed brief and research pack (24 steps)
    │   ├── SKILL.md, stage.json
    │   ├── references/              steps, TRACES handbook, brief, paths, file specs, handoff ...
    │   └── assets/                  templates and the step tracker
    ├── koru-explore/                stage 2: directions, two ideas, concept tests, Design v1
    │   ├── SKILL.md, stage.json
    │   ├── references/, assets/
    │   └── scripts/export_frame.py  reads the Frame export
    ├── koru-harden/                 stage 3: states, roles, edge cases, accessibility, feasibility,
    │   │                            tokens, rulebook checks (H1 to H19)
    │   ├── SKILL.md, stage.json
    │   ├── references/              steps, artefacts, rulebook, design library, review, handoff ...
    │   ├── assets/                  templates and the step tracker
    │   └── scripts/                 lint_harden, contrast_check, export_tokens
    └── koru-ship/                   stage 4: HTML deliverable with walkthrough, optional React starter,
        │                            tickets, handoff (S1 to S9, plus optional S3b)
        ├── SKILL.md, stage.json
        ├── references/              steps, tickets, handoff, client setup, walkthrough (Intro.js)
        ├── assets/                  deliverable.html, react-starter/, ticket and handoff templates, step tracker
        └── scripts/                 lint_ship (tour and React checks), export_tickets (Jira CSV + markdown)
```

## Where things live (inside an engagement folder)

`00-read-me-first.md` (project, roles, stage table, step trackers) · `01-framed-brief/` `02-research/` (Frame finals) · `03-rulebook/` `04-design-library/` `08-harden/` (Harden finals) · `06-explore/` (Explore finals) · `07-ship/` (Ship finals) · `05-decisions-log.md`, `ai-quality-log.md`, `break-log.md`, `playbook-changes.md` · registers · `handoff-cards/` · `stages/<stage>/drafts/` and `stages/<stage>/sources/`.

Only `-final` files in the numbered folders go into Claude project knowledge. The **context keeper** uploads them and runs the stale-check rhythm.

## Tickets without Jira

Ship writes each ticket as markdown in the workbook template, plus `tickets.csv` in Jira's import format (anyone with Jira imports it in one step) and a combined `tickets.md`. GitHub Issues are optional once `gh auth login` is done, and are only created after you confirm.
