# Harden handoff, Ship notes, send-back to Explore

The handoff card shell, where it is stored and the registers that travel with it are core's (`koru-core/references/engagement.md`; template `koru-core/assets/templates/handoff-card.md`). Harden fills the phase-specific lines.

## Harden's handoff card entries (Proposed)

| Field | Harden's entry |
|---|---|
| What we hand on | The hardened design (the `hardened-design` artefact and the `screens` HTML it links, with its Figma link), the tokens file with `tokens.css` and `tokens.json`, the scope, states, roles, edge cases, accessibility and feasibility artefacts, the rulebook chapters used, the rulebook check, the hardening checklist and the Ship notes. All `final` |
| Format and template | Markdown artefacts with front matter; the hardened screens as one self-contained HTML file with front matter in a leading comment; Figma frames with the `Final` section status, registered in the artefact registry |
| Where it lives and what it's called | `08-harden/` for the hardened design set (for example `meridian-harden-hardened-design-v1-final`), `03-rulebook/` for chapters, `04-design-library/` for tokens and the library files |
| What the next stage must be able to do with it | Write tickets and build the HTML deliverable without coming back to the design team: every screen has its states, roles, permissions, edge cases and AI states defined, every component and token is in the design library or listed as a gap, feasibility limits and API and data assumptions are written down, and every rulebook break is either fixed or listed as a Ship note |
| What it doesn't include | Jira tickets, user stories, the engineer-facing HTML deliverable, production code or a pull request, and any user testing beyond what Explore did |
| Who signs it off | The design lead and the rulebook owner, by name (the engineer has signed feasibility at H17) |
| Checked by the next stage (name) | To fill (Ship's team) |
| Stale-check result | No open warnings on any artefact in the handoff, with the date |
| Assertion confidence | `lint_lines.py --count` across the handed-on artefacts |
| Open assumptions and questions handed on | From core's registers: counts and the ids that block Ship |

How to fill it: run `koru-core/scripts/build_registry.py` and `stale_check.py`; count open rows in the registers; read signers from the decisions log; list the exact final file names.

**Self-test the "must be able to do" line.** Pick one screen and write, in your head, the ticket an engineer would need for it: the user story, the acceptance criteria for each state, the roles, the data it reads and writes. Is every piece of that in the handed-on files? Anything missing is either added now (a new version) or an open question blocking Ship.

## What Ship uses from each artefact

So the Ship skill (or a person writing tickets) knows where to look. Ship reads the hardened design set: it starts from the `hardened-design` artefact and the tokens file, and checks and extends Harden's work instead of repeating it. Harden counts as handed on when `final` artefacts with `stage: harden` exist in `08-harden/` and the handoff card is signed.

| Ship needs | From |
|---|---|
| The flow and screens to build | `screens` HTML (and Figma), `scope` |
| "States covered" on each ticket, coverage | `states`, `checklist` |
| Acceptance criteria for who can do what, including when the person who must act is away | `roles` |
| Edge cases to test (double submit, session timeout, no delegate, data volumes) | `edge-cases` |
| API and data assumptions, limits | `feasibility`, `ship-notes` |
| Component and token map | `tokens`, `tokens.css`, `components.md`, the screens' design system gaps |
| AI behaviour: who sees a wrong output, who fixes it, how it is logged, the audit log of accepted suggestions | the AI touchpoints block in `states` |
| Screen sizes to build and test, smallest first | `scope` (Target viewports), `screens` |
| Rules a build must keep | the rulebook chapters, `rulebook-check` |
| Known issues to handle while building | `ship-notes` (SN ids) |

## Ship notes

Ship notes are how small things travel without stalling Harden. Each note has an id (`SN1`, `SN2`, ...; never `S<n>`, which reads like a Ship step), the screen and state, why it was not fixed in Harden, and an owner. A note is not a place to park something that changes behaviour a user would notice: that is a fix here or a send-back (`harden-review.md`). Ship closes each note in its own artefacts and logs it.

## Send-back to Explore

If a direction will not hold (`harden-review.md`, "Fix here, Ship note, or send back"), do not patch it in Harden. Follow core's send-back protocol (`koru-core/references/registers.md`):

1. **Raise it.** What Harden found, where (the Harden artefact and the evidence pointer, usually the feasibility source or the accessibility result), and which Explore artefact it changes. A decisions-log line (stage `core`). Name who decides whether the revised direction needs the client again: by default the design lead, with the client's decision maker if Explore's client confirmation covered the part that changes.
2. **New source.** The evidence enters as a source (the engineer's answer, the accessibility test notes).
3. **Explore revises.** The designer makes the next version of the affected Explore artefacts (journey, combined wireframe, Design v1) with the Explore skill. The stale-check then flags every Harden artefact built on the old Design v1.
4. **Re-sign.** The revised Design v1 needs Explore's checks and sign-offs; the client re-confirms if Explore's trigger is met.
5. **Resume Harden** from H2 on the revised Design v1: re-run only the steps the stale-check flags, in its order. Mark the send-back resolved when the stale-check is clean.

Harden does not stop for the rest of the flow if the send-back touches only part of it: keep hardening the screens it does not touch, and log that you did.

## Files created and updated through Harden

| Artefact | Created at | Updated at | Checked by | Signed by | Final home |
|---|---|---|---|---|---|
| Scope | H2 | After a send-back | Design lead | (checked) | `08-harden/` |
| Feasibility | H3 | H9 | Design lead | Engineer | `08-harden/` |
| States, roles, edge cases | H5 to H7 | H13 | Design lead | (checked) | `08-harden/` |
| Accessibility | H8 | H13 | Design lead | (checked) | `08-harden/` |
| Tokens | H11 | When a value changes | Rulebook owner | Rulebook owner | `04-design-library/` |
| Screens | H12 | H13, H15 | Design lead | Design lead | `08-harden/`, Figma |
| Rulebook chapters | H14 | New version when a rule changes | Rulebook owner | Rulebook owner | `03-rulebook/` |
| Rulebook check | H15 | After each screens version | Rulebook owner | Rulebook owner | `08-harden/` |
| Checklist | H16 | Before H17 | Design lead | (checked) | `08-harden/` |
| Ship notes, hardened design | H18 | Before handoff | Engineer, design lead | Design lead | `08-harden/` |
| Handoff card | H19 | n/a | Ship's team | Design lead and rulebook owner | `handoff-cards/` |
