# Additions to koru-core for Harden

The phase contract (`koru-core/references/phase-contract.md`) says a phase adds its sign-off rows, re-confirmation trigger, defaults section and stage-map entry to core when it is built. Core v1 still reads "to be defined by the Harden skill" in those places. Paste the blocks below into the named core files (or let Claude apply them, then log it in the decisions log, stage `core`). Until they are applied, Harden uses them as written here and logs that it did.

## 1. `koru-core/references/stages.md`, replace the "Harden" section

```markdown
## Harden

Described in `koru-harden` (Proposed until the team confirms). It takes Explore's `final` Design v1 (the `design` artefact, the combined wireframe, insight decisions, add-ons, the final direction and journeys), the design system path and its gaps, and the open assumptions and questions that block Harden. It runs five parts: 1 Intake (scope inventory, feasibility questions sent early), 2 Harden (states including Partial, No permission and AI states, roles and permissions, edge cases including an absent approver with no delegate, a session timeout and a double submit, accessibility to WCAG 2.2 AA, feasibility with an engineer, then the fix, note or send-back decision), 3 Build (tokens file, hardened screens as self-contained HTML), 4 Rulebook (chapters, rulebook checks, the ten-item hardening checklist, three sign-offs), 5 Handoff (Ship notes, the hardened design, the handoff card). Checkpoints: H4 scope, H10 fix or send back, H17 sign-offs.

Hands on: the `hardened-design` artefact and everything it links, all `final`. Final folders: `03-rulebook/`, `04-design-library/`, `08-harden/`. Handoff test: "write tickets and build the HTML deliverable without coming back to the design team". A direction that will not hold goes back to Explore as a send-back; small issues go to Ship as notes (SN ids, so they never read like Ship step numbers).
```

And in "The four stages in one table", the Harden row becomes:

```markdown
| Harden | Design v1 (final), the design system path and gaps | The hardened design: screens, states, roles, edge cases, accessibility, feasibility, tokens, rulebook check, checklist, Ship notes | `03-rulebook/`, `04-design-library/`, `08-harden/` (Proposed) |
```

## 2. `koru-core/references/governance.md`, sign-off matrix

Replace the row `| Harden | to be defined by the Harden skill | | | |` with:

```markdown
| Harden | Scope, states, roles, edge cases, accessibility, checklist | Design lead | (checked, not signed) | No (Proposed) |
| Harden | Feasibility | Design lead, against the engineer's answer source | Engineer | No (Proposed) |
| Harden | Tokens file, rulebook chapters, rulebook check | Rulebook owner | Rulebook owner | No (Proposed) |
| Harden | Hardened screens and hardened design | Design lead | Design lead | No (Proposed); a change to something the client confirmed in Explore is a send-back to Explore |
| Harden | Ship notes | Engineer | Design lead | No |
| Harden | Handoff card | Next stage's team | Design lead and rulebook owner | No |
```

In "Re-confirmation triggers", split the `Harden, Ship` row and add:

```markdown
| Harden | Any Harden artefact | None (Proposed: the client confirms nothing in Harden; a rule that conflicts with what the client wants is an open question for the rulebook owner and the client's decision maker; a change to something the client confirmed in Explore is a send-back, and Explore's trigger applies) |
```

## 3. `koru-core/references/defaults.md`, replace the "Harden" section

```markdown
## Harden

The `koru-harden` skill was built on these defaults from the hackathon workbook's Harden chapter. They are inferences, listed so the team can confirm or change them.

| Item | Status | Default used |
|---|---|---|
| Required roles | Proposed | Designer, Design lead, Rulebook owner, Engineer, second-person checker |
| Final folders | Proposed | `03-rulebook/`, `04-design-library/` (reserved by core), `08-harden/` for the hardened design set (07 is left for Ship) |
| Artefact types | Proposed | scope, states, roles, edge-cases, accessibility, feasibility, tokens, screens, rulebook-chapter, rulebook-check, checklist, ship-notes, hardened-design |
| Size thresholds | Proposed | Small: one flow, 5 or fewer screens, 1 or 2 roles; large: several flows, more than 5 screens, or 3 or more roles |
| Accessibility standard | Proposed | WCAG 2.2 AA |
| When the engineer is involved | Proposed | Questions sent at H3, before state work; answers recorded at H9 as a verbatim source |
| Fix, Ship note or send back | Proposed | Fix here by default; Ship note for small items that do not change visible behaviour; send back only if the direction cannot be built, tested or made accessible as stated, or the fix changes the idea, key job, a journey step, or a client-confirmed item |
| Client confirmation in Harden | Proposed | None; rule conflicts are open questions for the rulebook owner and the client's decision maker |
| Tokens without a design system | Proposed | Derived from Design v1, named by role; missing values marked `(proposed)` and agreed by the rulebook owner |
| Design library home | Proposed | `04-design-library/` until a repo exists, then GitHub with `koru-final` on the release |
| Standard states | Proposed | Empty, Loading, Error, Success on every screen; Partial on every screen showing data from another system; No permission on every screen where a role is denied anything; the four AI states on every screen with an AI touchpoint |
| Standard edge cases | Proposed | Long text, no data, a lot of data, concurrent edits, double submit, slow or no network, renamed or deleted item, permission removed, approver or owner away with no delegate, session timeout mid-task, every target viewport |
| When the AI is wrong | Proposed | Every AI touchpoint states who sees a wrong output, who fixes it, how it is logged, and that every accepted suggestion is audit-logged with who accepted it, what and when |
| Target viewports | Proposed | Listed in the scope from the client's material (size and whether the device is shared); the hardened screens show the smallest one; checklist item 10 |
| Session timeout on shared devices | Open | Taken from the client's security rules; until known, an open question for the engineer at H3 |
| Who owns theme exploration when there is no design system | Open | Explore's tail if started there; otherwise Harden uses derived tokens and notes in the Ship notes that the theme is not final |
```

## 4. `koru-core/references/engagement.md`, folder layout

Add after `06-explore/` (`07` is left for Ship, so Harden takes the next free number):

```
  07-ship/                   Ship finals (left for Ship, Proposed)
  08-harden/                 Harden finals: the hardened design set (Proposed)
```

## 5. `koru-core/registry/roles.json`

No change: `Rulebook owner` and `Engineer` already exist.

## 6. Core now has `scripts/lint_lines.py` (created with this change)

`koru-core/scripts/lint_lines.py` is the phase-neutral traceable-line lint every phase runs after `lint_core.py`: one assertion per line (or per table cell), confidence `high`, `medium` or `low`, a `src:` on every line, the `high` rule, `(inferred)` only on `low`, `src: none` never under a "known" heading, and `--count` for the handoff card. Three core texts still need to say so:

- `koru-core/references/integrity.md`, "The lint split": add to the core checks: "Traceable lines (`scripts/lint_lines.py`, run on every derived artefact after `lint_core.py`): the rules above, plus `--count` for the confidence counts and `--must-cite` for sources that must be used." Then change the next paragraph to "Phase checks stay with the phase skill and run after both core lints. Frame's are in `koru-frame/scripts/lint_claims.py` (its stricter claim rules and `--must-cite` for request sources)."
- `koru-core/SKILL.md`: in the step loop, step 3, change "Run the lint (`scripts/lint_core.py`, plus the phase's own checks)" to "Run the lints (`scripts/lint_core.py`, `scripts/lint_lines.py`, then the phase's own checks)". In "Bundled resources", add the row `| scripts/lint_lines.py | Traceable-line checks on every derived artefact, and the confidence counts |`.
- `koru-core/references/file-protocol.md`, end of "Traceable lines and pointers": add "`scripts/lint_lines.py` checks this format."

## 7. `koru-core/scripts/init_stage.py`: copy HTML templates too

`init_stage.py` copies only `*.md` from a phase's templates folder, so Harden's `screens.html` template never reaches `stages/harden/templates/`. Change `tdir.glob("*.md")` to copy `*.md` and `*.html`. Until then, copy `koru-harden/assets/templates/screens.html` by hand at H12.

