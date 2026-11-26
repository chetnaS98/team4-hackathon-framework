---
name: koru-ship
description: Guides a Koru team through Ship (stage 4 of Frame, Explore, Harden, Ship), from Harden's final hardened design to engineers with no handover gap. Claude drafts; named people decide at three checkpoints - design lead and engineer agree the user stories before anything is built, someone new to the flow runs the deliverable's guided walkthrough and the design lead confirms it, and the engineer reviews and signs the handoff. Outputs a clickable HTML deliverable with an Intro.js walkthrough of its features and interactions, 3 to 5 tickets with acceptance criteria, a handoff note, a PR readiness note, an agent cold read, and tickets as a Jira CSV and markdown (no Jira access needed). Works with koru-core. Use when someone starts or resumes Ship, refers to the Harden handoff, or asks for user stories, tickets, the HTML deliverable, a product walkthrough or tour, the handoff note, an engineer review, or a ticket export, even without naming the skill.
---

# Koru Ship: the Ship phase

**Start every session by loading `koru-core`** (its `SKILL.md`: the never-bend rules, the step loop, checkpoints, the session start and resume protocol, the tone). Read its references as the moment arises: the file protocol, engagement scaffolding, governance, integrity checks, registers and `koru-core/references/stages.md`. This skill expects **koru-core v1**; if the installed core differs, say so before doing step work. This skill does not restate core's rules.

Ship gets an approved design to engineers with no handover gap: the design delivered as code, with specs an engineer or their coding agent can build from without coming back with questions. It starts from Harden's final hardened design and tokens file. It hands on an HTML deliverable of the core flow, tickets with descriptions, acceptance criteria and screenshot links, and a short handoff note. An engineer reviews the handoff and signs it off.

**Ship describes, it does not redesign.** If writing a ticket shows that Harden left a behaviour undefined, ask (open question) or send it back to Harden. Never decide what a user sees or can do in a ticket that Harden did not decide.

## At a glance (for the team's write-up)

Claude drafts everything; people decide at three **checkpoints** (hard stops) and check every other step.

1. AI drafts 3 to 5 user stories (it can start early, as drafts). **Checkpoint 1: the design lead and the engineer agree the stories are what will be built**, before anything is drawn.
2. AI turns Harden's hardened screens and tokens into one clickable HTML deliverable of the core flow, with a stable link for every step and state and an **Intro.js guided walkthrough** that shows a new user each feature and interaction. **Checkpoint 2: someone who has not seen the flow runs the walkthrough and clicks through every state; their words are recorded; the design lead confirms.**
3. AI writes one ticket per story with acceptance criteria for every state, role, AI behaviour and edge case (**checks: design lead**), then the half-page handoff note and a note on what a pull request would take (**checks: design engineer**).
4. An agent reads the handoff cold and lists every question an engineer would still ask (**the design engineer decides each fix**). **Checkpoint 3: a named engineer reviews the handoff, lists what they'd still need, and signs.**
5. A script exports the final tickets as a Jira CSV import file and markdown; **a person imports them** (GitHub Issues only after a yes). **Confirms: engineer.**

## Terms

- **Part** (1 Intake, 2 Build, 3 Handoff, 4 Review, 5 Deliver). "Stage" always means Frame, Explore, Harden or Ship.
- **The hardened design** is Harden's final `hardened-design` artefact and everything it links (screens HTML, tokens with `tokens.css` and `tokens.json`, scope, states, roles, edge cases, accessibility, feasibility, rulebook check, checklist, Ship notes).
- **Ship note SN<n>** is a note Harden handed on (`SN1`, `SN2`, ...). Steps in this skill are `S1` to `S9`; the different prefix keeps them apart.
- **Anchor**: a stable link into the deliverable, `#step-N` for a step and `#step-N-state-<state>` for a state (state in lower case, spaces as hyphens: `#step-2-state-ai-low-confidence`).
- **Checkpoint**: S2 (stories agreed), S3 (walkthrough test) and S7 (engineer review). Core's checkpoint rule applies: never start the next step before the named person confirms, and log the confirmation.
- **Walkthrough**: the Intro.js guided tour inside the deliverable. It shows a new user each screen, each feature and each interaction (what to click, what happens, how to undo), in plain words.

## Ship-only rules

The shared rules are in core. These apply in Ship.

- **Never start from a draft.** Step S1 runs `scripts/lint_ship.py --intake <engagement>`. If the hardened design is not `final`, or the stale-check has warnings, say Harden has not handed on, and stop.
- **Stories may start early; tickets may not.** Draft user stories while Explore and Harden work, from `final` Explore and Frame artefacts only (never from Harden drafts). They stay `draft`. No ticket is `final` before the hardened design is `final` and the stale-check is clean.
- **One flow, 3 to 5 tickets, one per user story.** More than five stories means a second flow: run Ship again for it, logged.
- **Reuse, don't redraw.** The deliverable is built from Harden's screens markup and `tokens.css`. A component or token that is not in the design library is a design system gap, listed, never invented.
- **The deliverable is the reference among Ship's outputs.** Tickets link its anchors. If a ticket, Figma and the deliverable disagree, the deliverable wins and the others get a new version. If the deliverable disagrees with Harden, that is a send-back, not a fix.
- **Close every Ship note.** Each Harden Ship note SN<n> is closed in a ticket or carried in the handoff note (`lint_ship.py --ship-notes`).
- **Never fabricate screenshots, ticket keys, issue numbers or an engineer's words.** Screenshots are anchors; a person captures image files if they are needed. The engineer's review enters verbatim as a source.
- **Nothing leaves without a yes.** Only `final` tickets get the `koru-final` label. Importing into Jira is done by a person. `export_tickets.py --github` is a dry run; pass `--yes` only after the user says yes in chat to that exact list (it publishes outside the team).
- **No pull request.** It is out of scope. Write the `pr-readiness` note instead.
- **People decide, Claude drafts.** Claude never confirms a checkpoint, never answers as the new user or the engineer, and never marks a walkthrough test passed. A walkthrough test with nobody new to the flow is not done: ask for a name from the checker pool or an organiser.
- **The walkthrough explains, it does not sell.** Every tour step describes something the deliverable really does, using the labels on screen. No tour step for an add-on or for behaviour Harden did not define.
- **Intro.js is the one external script allowed**, pinned to the version in the template and loaded from cdnjs. If it does not load (offline), the deliverable still works and the "Take the tour" button hides itself. Intro.js is AGPL-3.0 or paid commercial licence: the design lead confirms the licence position before the deliverable goes to a client (open question in `client-setup.md`).

## Show where the work is

At the start of every reply, show:

```
Part: [1 Intake / 2 Build / 3 Handoff / 4 Review / 5 Deliver]
Step: [S1 to S9 from the map below]
Next: [what happens next, and whether it is a person's turn or Claude's]
```

End every reply that reaches a checkpoint (S2, S3, S7) with a clear question to the named person, and stop.

## Starting Ship

1. Follow core's session start and resume protocol. The orchestrator may call this skill with `engagement=<path> step=<id>`; use that engagement and run that step. If the engagement exists but Ship has not started, run `koru-core/scripts/init_stage.py --engagement <project> --stage-dir <this skill>`. It creates `stages/ship/` (drafts in `stories/`, `deliverable/`, `tickets/`, `handoff/`, `review/`, plus `sources/`), the final folder `07-ship/`, the Markdown templates and the step tracker. The deliverable template (`deliverable.html`) is copied with the others; if your core copies only Markdown templates, copy it from `assets/templates/` at S3.
2. **Core additions.** If `koru-core/references/governance.md` still says "Ship: to be defined", tell the user the rows in `references/core-additions.md` need adding to core and offer to apply them. Until they are added, use them as written there and log that you did.
3. **The roles gate.** Ship requires: Engineer, Design lead, Design engineer, Second-person checker pool, plus the client's decision makers and the review rhythm. `koru-core/scripts/check_roles.py` must pass before S1. The engineer who reviews at S7 must not be the person who ran S3 or S4.
4. **Early stories.** If asked to draft stories before Ship starts (`step=S2-early`), follow "S2 early" in `references/steps.md`. It writes to `stages/ship/drafts/stories/` and does not start the stage.
5. **New client?** Check the one-time setup list (`references/client-setup.md`) and record what is missing as open questions.

## The step map

| # | Who | Step | Mode | Output | Checker |
|---|---|---|---|---|---|
| S1 | Design lead | Share the Harden handoff; Claude reads everything and confirms back in 3 lines | Human-led | Intake check, tracker row | The person sharing |
| S2 | Claude, then Design lead + Engineer | User stories: 3 to 5, one flow. **Checkpoint 1:** the design lead and the engineer agree them | AI-assisted, checkpoint | `user-story` | Design lead and engineer confirm |
| S3 | Claude + Design engineer, then a new user + Design lead | HTML deliverable of the core flow with the Intro.js walkthrough. **Checkpoint 2:** a person new to the flow runs the walkthrough and clicks every state; the design lead confirms | AI-led, checkpoint | `deliverable` (.html), walkthrough test source | New user (their words), design lead confirms |
| S4 | Claude + Design engineer | Tickets, one per story | AI-led | `ticket` x 3 to 5 | Design lead |
| S5 | Claude + Design lead | Handoff note and PR readiness note | AI-led | `handoff-note`, `pr-readiness` | Design engineer |
| S6 | Claude (agent), then Design engineer | Agent pre-check: cold read by `handoff-reviewer` | AI-led | `review` (agent) | Design lead |
| S7 | Engineer | **Checkpoint:** engineer review; answers become new versions; sign-off | Human-led | Source, `review` (engineer) | Engineer signs |
| S8 | Claude, then Engineer | Deliver tickets: CSV and markdown export, GitHub optional | AI-led | `07-ship/export/iteration-<n>/` | Engineer |
| S9 | Claude, then signers | Close: handoff card to the build team; engagement done | AI-led | Handoff card | Build team's engineer |

The playbook for each step is in `references/steps.md`; read the entry for the current step before doing it. After writing an artefact, run `koru-core/scripts/lint_core.py`, `koru-core/scripts/lint_lines.py`, then `scripts/lint_ship.py` (with `--tokens`, `--screens` and `--ship-notes` once those inputs exist), and fix what they report before handing it on.

## Iterations: handoff v1, v2, ...

Ship runs in **iterations**. Iteration 1 ends with the first handoff to the build team: `handoff-cards/<project>-ship-handoff-card-v1.md`, the handoff note with `iteration: 1`, and the export in `07-ship/export/iteration-1/`. When the build team comes back with feedback (questions, changes, a Harden send-back that has been answered), a named person starts the next round:

```bash
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/iteration.py" --engagement <e> --by "<name>" --reason "<the feedback>" [--from S2]
```

It refuses until the current iteration's card exists, reopens Ship, sets S3 to S9 (or from `--from`) back to not started, and logs it. In iteration n+1:
- every changed artefact is a **new version** (deliverable, tickets, handoff note, PR readiness, reviews); nothing from iteration n is overwritten, and the previous drafts go to `superseded/`;
- the handoff note carries `iteration: n+1` in its front matter and a `## What changed since iteration n` section (`lint_ship.py` checks it);
- the handoff card is a new file, `-v<n+1>`, listing the exact versions handed over; the export goes to `07-ship/export/iteration-<n+1>/`.

Rework *inside* an iteration (S6 agent findings, S7 engineer answers) is still new versions of the drafts, but no new iteration and no new card. `route.py` shows the current iteration.

## Inputs

All `final`, read at S1: the `hardened-design` artefact and everything it links (in `08-harden/`), the tokens artefact with `tokens.css` and `tokens.json` (in `04-design-library/`), the rulebook chapters (in `03-rulebook/`), the Harden handoff card, the final framed brief (for ticket context), the read-me (design system path, roles), the decisions log, and the open rows in the assumptions and open-questions registers that block Ship. Which Ship output uses which Harden artefact is in `koru-harden/references/handoff.md` ("What Ship uses from each artefact").

## Outputs

| Type | Step | Name | Final home |
|---|---|---|---|
| `user-story` | S2 | `<project>-ship-user-story-v1-draft.md` | `07-ship/` |
| `deliverable` | S3 | `<project>-ship-deliverable-v1-draft.html` | `07-ship/` |
| `ticket` | S4 | `<project>-ship-ticket-<nn>-<slug>-v1-draft.md` | `07-ship/`, then Jira or GitHub with `koru-final` |
| `handoff-note` | S5 | `<project>-ship-handoff-note-v1-draft.md` | `07-ship/` |
| `pr-readiness` | S5 | `<project>-ship-pr-readiness-v1-draft.md` | `07-ship/` |
| `review` | S6, S7 | `<project>-ship-review-agent-v1-draft.md`, `<project>-ship-review-engineer-v1-draft.md` | `07-ship/` |
| Ticket export | S8 | `tickets.csv`, `tickets.md` (generated, no front matter) | `07-ship/export/iteration-<n>/` |
| Handoff card | S9 | `<project>-ship-handoff-card-v<iteration>.md` (one per iteration) | `handoff-cards/` |

## Outside skills

None overrides core's rules. `koru-ai-dlc:ship-html-from-design`, `koru-ai-dlc:ship-tickets` and `design:design-handoff` may supply a method for S3 and S4, but the output still uses this skill's templates, naming, anchors and lints. The Jira (Atlassian) connector is not used: the team has no Jira access, so S8 exports a CSV instead. If a listed skill is not installed, do the step yourself and do not claim to have used it.

## Bundled resources

Read these when you reach the relevant moment. Shared references are in `koru-core`.

| File | Read it when |
|---|---|
| `references/steps.md` | Before running any step (one entry per step, plus S2 early) |
| `references/tickets.md` | S2, S4 and S8: the template, splitting, acceptance criteria rules, export and delivery, labels |
| `references/handoff.md` | S5 to S9: the handoff note, PR readiness, the cold read brief, the engineer review, the handoff card, send-back to Harden |
| `references/client-setup.md` | Once per new client: the one-time setup checklist |
| `references/walkthrough.md` | S3: building the Intro.js walkthrough, and checkpoint 2 (the walkthrough test) |
| `references/core-additions.md` | Once, when Ship first runs in an engagement whose core has no Ship rows |
| `stage.json` | Read by core's `init_stage.py` |
| `assets/templates/` | Starting point for every Ship artefact type |
| `scripts/lint_ship.py` | Ship's structure and coverage checks after core's lints; `--intake` at S1 |
| `scripts/export_tickets.py` | S8: Jira CSV and markdown export; optional GitHub Issues |
