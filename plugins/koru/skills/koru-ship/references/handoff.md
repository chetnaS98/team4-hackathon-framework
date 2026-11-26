# Ship handoff: the note, PR readiness, the reviews, the card

The handoff card shell, where it is stored and the registers that travel with it are core's (`koru-core/references/engagement.md`; template `koru-core/assets/templates/handoff-card.md`). Ship fills the phase-specific lines. Ship is the last stage, so its card hands on to the build team, not to another stage.

## Contents
- The handoff note
- The PR readiness note
- The cold read brief (S6)
- Recording the engineer review (S7)
- Ship's handoff card entries
- Send-back to Harden
- Files created through Ship

## The handoff note

Half a page (about 250 to 300 words across the four parts). Plain words, links rather than copies. Template: `assets/templates/handoff-note.md`. The four parts, as level-2 headings (`lint_ship.py` checks them):

1. **What's in the deliverable**: the flow, the steps and states, the number of tickets, where each file is.
2. **What's not**: other flows, add-ons, anything the tickets mark out of scope, no pull request.
3. **Decisions engineers should know about**: the few decisions that would surprise an engineer (a data source chosen, a limit accepted, an AI behaviour), each linked to its decisions-log line or source.
4. **Who to ask**: names and roles from the read-me, by topic (design, data, AI behaviour, the client).

Then, only if any are left, "Harden Ship notes": each Ship note SN<n> not closed in a ticket, with why it is carried and who owns it.

## The PR readiness note

A pull request is out of scope. The `pr-readiness` note (`assets/templates/pr-readiness.md`) says what one would take, so the build team can start without a planning meeting. It follows the team's Ship approach:

- **Spec per unit**: the journey split into buildable units, one `spec.md` each (states, edge cases, WCAG AA, Given/When/Then criteria traced to journey steps). Here, each ticket is a unit.
- **Plan per ticket**: a coding agent in plan mode writes `plan.md` for each ticket; nothing is built until the engineer approves it.
- **Questions file**: anything the agent cannot work out goes in `questions.md` with an `[Answer]:` slot; the design engineer answers, and the spec or ticket gets a new version.
- **Component build**: components built from the ticket, the deliverable and `tokens.json`, then wired into the journey; new components first, from the design system gaps.
- **Journey tests in CI**: end-to-end and accessibility tests for every journey path and state, run on each pull request.
- **Review action**: a review bot comments on each pull request and never approves; a person (the code owner) merges.
- **Setup still missing**: the open items from `client-setup.md`.

## The cold read brief (S6)

The plugin agent `handoff-reviewer` holds this brief. If the agent is not installed, give a general subagent exactly this, plus the file list:

> You are an engineer, or a coding agent, picking this up on Monday. You were in no meeting. Read only these files: the tickets, the HTML deliverable, the handoff note, the PR readiness note, and the design library (`04-design-library/`). For each ticket, try to build it in your head and list every point where you would have to guess: behaviour no acceptance criterion covers; a state in the deliverable but not in the ticket, or the other way round; a component not in the library; a value not available as a token; data whose source, format or freshness is not stated; a role or permission left unclear; what happens when the AI is wrong, and how it is logged; an anchor that does not resolve. Output a table `Ticket | Question I'd have to ask | Where the answer should go`, then "Buildable without questions: n of N" (tickets with no questions, out of all tickets). Be strict. Do not fix anything.

Give it only the Ship drafts and the design library: not the Harden files, not this conversation. The point is a cold read.

## Recording the engineer review (S7)

The engineer's words are a source: save them verbatim in `stages/ship/sources/`. The `review` artefact (reviewer: name and role) lists each question with its source pointer and a resolution: `Fixed in <artefact> v<n>`, `Open question Q<n>` (with an owner), or `Not needed: <reason>` (the engineer agrees). Never write an engineer's question or answer yourself. The engineer signs off the handoff once their list is covered; log it with "sign-off" in the decision text.

## Ship's handoff card entries (Proposed)

| Field | Ship's entry |
|---|---|
| What we hand on | The HTML deliverable of the core flow, 3 to 5 tickets, the user stories, the handoff note, the PR readiness note, the agent and engineer reviews, and the ticket export (`tickets.csv`, `tickets.md`). All `final` |
| Format and template | Markdown artefacts with front matter in the Ship templates; the deliverable as one self-contained HTML file with front matter in a leading comment; tickets in the team ticket template; the export in Jira's CSV import format |
| Where it lives and what it's called | `07-ship/` (for example `demo-ship-ticket-01-book-room-v1-final`, `demo-ship-deliverable-v1-final.html`), `07-ship/export/`, and the delivered copies in Jira or GitHub with the `koru-final` label (registry rows with their pointers) |
| What the next stage must be able to do with it | Build the core flow from the tickets, the HTML deliverable and the tokens without coming back to the design team: every ticket has acceptance criteria for every state, role permission, AI behaviour and edge case it covers, every Harden Ship note is closed or carried, every remaining question has an owner, and the engineer's review questions are answered or listed |
| What it doesn't include | Production code, a pull request or merged changes, journey tests running in CI, flows other than the core flow, anything a ticket lists as out of scope, and screenshot image files (tickets link to the deliverable's anchors instead) |
| Who signs it off | The engineer and the design lead, by name |
| Checked by the next stage (name) | The build team's engineer, by name |
| Stale-check result | No open warnings on any artefact in the handoff, with the date |
| Assertion confidence | `lint_lines.py --count` across the handed-on artefacts |
| Open assumptions and questions handed on | From core's registers: counts, and the ids the build team owns |

How to fill it: run `koru-core/scripts/build_registry.py` and `stale_check.py`; count open rows in the registers; read signers from the decisions log; list the exact final file names. **Self-test:** pick one ticket and try to build it in your head from the handed-on files only. Anything you would ask is either added now (a new version) or an open question with an owner.

When the card is signed, tell the orchestrator. It runs `advance_stage.py`, which checks every step, the stale-check, the card, the final folder, a sign-off line and a named confirmer. Ship is the last stage: the engagement is then done. List which `final` files go to Claude project knowledge, and remind the user that only `koru-final` tickets count in Jira or GitHub.

## Send-back to Harden

If writing tickets shows that Harden's design will not hold as stated (a state, permission or AI behaviour is missing and the fix would change what a user sees or can do), follow core's send-back protocol (`koru-core/references/registers.md`). Raise it with the evidence (usually the engineer review source or the agent review), log it (stage `core`), and let Harden issue the new version with `koru-harden`. The stale-check then flags every Ship artefact built on the old version; re-run only those steps, in its order. Small gaps that do not change behaviour are open questions, answered by the design lead, not send-backs.

## Files created through Ship

| Artefact | Created at | Updated at | Checked by | Signed by | Final home |
|---|---|---|---|---|---|
| User stories | S2 (or early) | S2 re-base | Design lead | (checked) | `07-ship/` |
| HTML deliverable | S3 | S4 (anchors), S6, S7 | Design lead | Design lead | `07-ship/` |
| Tickets | S4 | S6, S7 | Design lead, then engineer | Engineer | `07-ship/`, Jira or GitHub with `koru-final` |
| Handoff note, PR readiness | S5 | S6, S7 | Design engineer | Engineer | `07-ship/` |
| Review (agent) | S6 | n/a | Design lead | (checked) | `07-ship/` |
| Review (engineer) | S7 | n/a | Engineer (their own words) | Engineer | `07-ship/` |
| Ticket export | S8 | Each new final ticket version | Engineer | (generated) | `07-ship/export/` |
| Handoff card | S9 | n/a | Build team's engineer | Engineer and design lead | `handoff-cards/` |
