# Additions to koru-core for Ship

The phase contract (`koru-core/references/phase-contract.md`) says a phase adds its sign-off rows, re-confirmation trigger, defaults section and stage-map entry to core when it is built. Core v1 still reads "to be defined by the Ship skill" in those places. Paste the blocks below into the named core files (or let Claude apply them, then log it in the decisions log, stage `core`). Until they are applied, Ship uses them as written here and logs that it did.

## 1. `koru-core/references/governance.md`, sign-off matrix

Replace the row `| Ship | to be defined by the Ship skill | | | |` with:

```markdown
| Ship | User stories | Design lead | (checked, not signed) | No (Proposed) |
| Ship | HTML deliverable | Design lead (clicks through every step and state) | Design lead | No (Proposed); a change to behaviour Harden defined is a send-back to Harden |
| Ship | Tickets | Design lead, then the engineer at the review checkpoint | Engineer | No (Proposed) |
| Ship | Handoff note, PR readiness note | Design engineer | Engineer | No |
| Ship | Review (agent pre-check) | Design lead (every question fixed or logged) | (checked, not signed) | No |
| Ship | Review (engineer) | Engineer (their own words, recorded verbatim as a source) | Engineer | No |
| Ship | Handoff card (Ship to the build team) | The build team's engineer | Engineer and design lead | No |
```

In "Re-confirmation triggers", replace the `Harden, Ship` row (or, if Harden's additions are already applied, add below Harden's row):

```markdown
| Ship | Any Ship artefact | None (Proposed: the client confirms nothing in Ship; a change to what a user sees or can do, or to the scope, is a send-back to Harden, and Harden's and Explore's triggers apply) |
```

## 2. `koru-core/references/defaults.md`, replace the "Ship" section

```markdown
## Ship

The `koru-ship` skill was built on these defaults from the hackathon workbook's Ship chapter. They are inferences, listed so the team can confirm or change them.

| Item | Status | Default used |
|---|---|---|
| Required roles | Proposed | Engineer, Design lead, Design engineer, second-person checker pool |
| Final folder | Proposed | `07-ship/` (generated ticket export in `07-ship/export/`) |
| Artefact types | Proposed | user-story, deliverable, ticket, handoff-note, pr-readiness, review |
| Size thresholds | Proposed | Small: one flow, 3 to 5 tickets; large: more than one flow or more than 5 stories, run as one Ship pass per flow |
| Ticket split | Proposed | One ticket per user story, 3 to 5 for one flow |
| Ticket home | Proposed | The Markdown ticket is the source of truth; Jira via CSV import (no Jira access), GitHub Issues optional; `koru-final` label on final tickets only |
| Screenshots | Proposed | Anchors in the HTML deliverable (`#step-N-state-<state>`); image files only if a person captures them |
| Early user stories | Proposed | Allowed once Explore's Design v1 is final, from final Explore and Frame artefacts only; stay draft until re-based at S2 |
| Who signs off | Proposed | The engineer signs tickets, the handoff note and PR readiness; the design lead signs the deliverable; both sign the handoff card |
| Pull request | Proposed | Out of scope; a `pr-readiness` note says what one would take |
| Client confirmation in Ship | Proposed | None |
| Who captures screenshots for Jira | Open | Whoever imports the tickets, from the anchors |
```

## 3. `koru-core/references/stages.md`, replace the "Ship" section

```markdown
## Ship

Described in `koru-ship` (Proposed until the team confirms). It takes Harden's `final` hardened design and everything it links (screens HTML, tokens with `tokens.css` and `tokens.json`, scope, states with AI touchpoints, roles, edge cases, accessibility, feasibility, rulebook check, checklist, Ship notes) and gets it to engineers with no handover gap. It runs five parts: 1 Intake (read the Harden handoff; refuse if it is not final or the stale-check has warnings), 2 Build (3 to 5 user stories, which may be drafted early; one self-contained HTML deliverable of the core flow with stable anchors per step and state; one ticket per story in the team template), 3 Handoff (a half-page handoff note and a PR readiness note), 4 Review (an agent cold read, then the engineer review checkpoint and sign-off), 5 Deliver (a Jira CSV import file and markdown, GitHub Issues optional; the handoff card to the build team). Checkpoint: S7, the engineer review.

Hands on: the deliverable, tickets, handoff note, PR readiness note and reviews, all `final`, in `07-ship/`, plus the export. Handoff test: "build the core flow without coming back to the design team". Ship is the last stage; its card goes to the build team. A gap that changes what a user sees is a send-back to Harden.
```

And in "The four stages in one table", the Ship row becomes:

```markdown
| Ship | The hardened design (final) and the tokens file | An HTML deliverable of the core flow, 3 to 5 tickets, a handoff note, a PR readiness note, an engineer's review | `07-ship/` (Proposed) |
```

## 4. `koru-core/references/engagement.md`, folder layout

Replace the line `07-...  unassigned: ...` with:

```
  07-ship/                   Ship finals: deliverable, user stories, tickets, handoff note, PR readiness, reviews; export/ holds the generated tickets.csv and tickets.md (Proposed)
```

(Harden's additions already place `08-harden/` after it.)

## 5. `koru-core/references/file-protocol.md`, "Where things live"

Replace the Tickets row with:

```markdown
| Tickets | Markdown ticket artefact (source of truth), copied to Jira (CSV import) or GitHub Issues | Only `final` tickets are copied, with the `koru-final` label; each copy is a registry row with its `jira:` or `github:` pointer |
```

## 6. `koru-core/registry/roles.json`

No change: `Engineer`, `Design lead`, `Design engineer` and `Second-person checker pool` already exist.
