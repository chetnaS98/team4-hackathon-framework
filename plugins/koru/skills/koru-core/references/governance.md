# Governance: roles, sign-offs, size, defaults, outside skills

## Contents
- Checking AI output
- The roles registry
- The sign-off matrix
- Re-confirmation triggers
- Engagement size and review scaling
- The defaults register
- Approved and third-party skills

## Checking AI output

Every AI-led step has a named second person who checks it. The checker is never the person who ran the step. Roles are roles, not names; names for an engagement go in `00-read-me-first.md`.

A checker reads the output as a reviewer would: what is it sure about, where did that come from, what is missing. Give them a hand-over checklist with every artefact. The core items (a phase adds its own):

1. Which assertions are `high`, and do they really have two independent sources or direct data?
2. Pick three at random and open their sources. Does the source say that?
3. Is anything stated with no source that is not marked an assumption?
4. What is missing that a reader would expect?
5. Any client names left in the text?
6. Are the stage's sources all used (nothing skipped, including transcripts, tickets or designs)?
7. Is every list in the sources reproduced in full where the artefact says so?

Mistakes caught go in the AI quality log with a category.

## The roles registry

The registry is `registry/roles.json`. A phase skill's `stage.json` says which roles it requires; `check_roles.py` checks the union for the active stages.

| Role | Does |
|---|---|
| Researcher | Runs the AI-led steps with Claude, converts sources, judges synthesis, drafts |
| Research owner | Checks TRACES, the pack and the problem space; signs the research pack |
| Senior | Checks opportunities, constraints and success outcomes; signs the brief |
| Team lead | Leads the engagement day to day; owns the review rhythm and the handoff between stages |
| Designer | Runs a design session with Claude and decides at the checkpoints (the person in charge in Explore) |
| Design lead | Leads design work in later stages; checks design artefacts as the second person |
| Rulebook owner | Owns the rulebook and design library in Harden |
| Developer | Takes part through the constraints review: tech limits, the existing system and integrations |
| Engineer | Builds and checks feasibility in later stages |
| Design engineer | Bridges design and code (components, tokens) in later stages |
| Second-person checker | Any person other than the one who ran the step; names go in the read-me |
| Client | Confirms the artefacts the matrix says they confirm; answers open questions |

A single person may hold several roles, but never the runner and the checker of the same step. Which later-stage roles each stage requires is declared by that stage's skill; do not assume.

## The sign-off matrix

One table, artefact against signer, for every stage. A phase skill adds its rows when its skill is built; core requires every artefact type to have a signer, and a re-confirmation trigger where the client confirms, before the type is used.

| Stage | Artefact | Checked by | Signed by | Client confirms |
|---|---|---|---|---|
| Frame | Research pack | Research owner | Research owner | No |
| Frame | Framed brief | Senior | Senior | Yes (problem, who it is for, success looks like, answers to open questions) |
| Frame | Insight, persona, workflow, JTBD, competitive scan | Research owner | (checked, not signed) | No |
| Frame | Opportunities | Senior | (checked, not signed) | No |
| Frame | Handoff card | Next stage's team | Senior and research owner | No |
| Explore | Final direction, journeys, rationale, add-ons | Design lead | Designer (confirms at the checkpoint) | No (Proposed) |
| Explore | Wireframes for Idea A and Idea B | Design lead (must be `review` before they are shared for feedback) | Designer | No (Proposed) |
| Explore | Insight decisions and Design v1 | Design lead | Designer | No (Proposed); a change to the brief's problem or success outcomes is a send-back to Frame |
| Explore | Handoff card | Next stage's team | Design lead and designer | No |
| Harden | to be defined by the Harden skill | | | |
| Ship | to be defined by the Ship skill | | | |

Rules that hold for every stage: the client-confirmation rule (an artefact the matrix marks as client-confirmed is not `final` until the client has confirmed; record who, the date and the channel in the decisions log); you prepare each sign-off but never sign or confirm for anyone; record the name and date the person gives you.

## Re-confirmation triggers

When a client-confirmed artefact gets a new version, the client re-confirms only if a defined trigger is met; anything else is logged and shown in the new version.

| Stage | Artefact | Re-confirm when |
|---|---|---|
| Frame | Framed brief | The problem statement or the success outcomes change in meaning (wording and layout edits do not count; when unsure, ask the senior) |
| Explore | Any Explore artefact | None defined in the source document (Proposed: the client confirms nothing in Explore; a change that touches the brief's problem or success outcomes is sent back to Frame and Frame's trigger applies) |
| Harden, Ship | to be defined by each phase skill | A phase must define its trigger before it asks for client confirmation of anything |

## Engagement size and review scaling

Set at kickoff and logged. Size sets review style and depth.

| | Small | Large |
|---|---|---|
| Rough size (Proposed, from Frame) | One workflow, about 10 or fewer source files, 1 or 2 personas | Several workflows, more sources, or 3 or more stakeholder groups |
| Review | Async: reviewers comment by a deadline, then the owner decides | Live meeting, then the owner decides in the room |
| Time box (Proposed) | Comments within 1 working day, decision the next day | 45 to 60 minutes |

These thresholds were written for Frame. Explore has a fixed shape (2 to 3 directions, 2 journeys, 2 ideas, one combined design), so its size is better set by journeys, screens and flows; the thresholds are not defined yet (`stages.md`). Each later phase must check whether it needs its own thresholds (for example by number of screens, flows or tickets) and declare them in its `stage.json`; until it does, use these and log that you did. To set the size, ask the phase's size questions, propose a size, and log the reasoning. For a live review, prepare a one-page agenda: what is being decided, the confidence counts, the top assumptions and the open questions.

## The defaults register

`references/defaults.md` is the one register of items the source documents mark Open or Proposed, with the default used and a section per stage. At kickoff, tell the user once that the defaults exist, show the relevant sections, and log "defaults accepted" (or any change) in the decisions log. If the team decides differently, edit `defaults.md`; nothing else needs to change. Team rules set during use are recorded there too.

## Approved and third-party skills

The principle: no outside skill overrides core rules. A third-party skill may supply a method for a step, but its output still follows the traceable-line format, naming, status and logs, and it never replaces a check. Community skills are not Koru's own, so the user reads each one before installing it. Each phase skill keeps its own list (what is used, what covers only part of a step, what is not a fit); core keeps none. If a listed skill is not installed, do the step yourself and do not claim to have used it.
