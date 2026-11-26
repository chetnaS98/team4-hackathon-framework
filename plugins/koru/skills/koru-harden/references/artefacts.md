# Harden artefacts

The shared protocol (naming, status, front matter, claim lines, pointer forms, HTML artefacts) is in `koru-core/references/file-protocol.md`. Names are `[project]-harden-[artefact]-v[n]-[status]`. This file is only what is specific to Harden. Templates are in `assets/templates/`. `scripts/lint_harden.py` checks the exact headers below, so copy them as written.

## Contents
- Types at a glance
- `derives_from` chain
- Structures, one per type
- Feeding the registers

## Types at a glance

| Type | Step | Contains | Example name | Lives in (draft, then final) |
|---|---|---|---|---|
| `scope` | H2 | Screens, roles, data objects, AI touchpoints, target viewports, inherited gaps | `meridian-harden-scope-v1-draft` | `part-1-intake/`, `08-harden/` |
| `feasibility` | H3, H9 | Engineer questions, answers, design impact, limits | `meridian-harden-feasibility-v2-draft` | `part-2-harden/`, `08-harden/` |
| `states` | H5 | Every state of every screen, AI states included | `meridian-harden-states-v1-draft` | `part-2-harden/`, `08-harden/` |
| `roles` | H6 | Role by screen: see, change, undo, approve, must not see | `meridian-harden-roles-v1-draft` | `part-2-harden/`, `08-harden/` |
| `edge-cases` | H7 | Standard and domain edge cases, design response | `meridian-harden-edge-cases-v1-draft` | `part-2-harden/`, `08-harden/` |
| `accessibility` | H8 | Checks by screen, result, fix | `meridian-harden-accessibility-v1-draft` | `part-2-harden/`, `08-harden/` |
| `tokens` | H11 | Colour, type, spacing, radius tokens and contrast pairs | `meridian-harden-tokens-v1-draft` | `part-3-build/`, `04-design-library/` |
| `screens` | H12 | The hardened design: every screen, every state (`.html`) | `meridian-harden-screens-v1-draft.html` | `part-3-build/`, Figma and `08-harden/` |
| `rulebook-chapter` | H14 | One rulebook chapter | `meridian-harden-rulebook-chapter-request-status-v1-draft` | `part-4-rulebook/`, `03-rulebook/` |
| `rulebook-check` | H15 | Rule by screen and state: pass, break, action | `meridian-harden-rulebook-check-v1-draft` | `part-4-rulebook/`, `08-harden/` |
| `checklist` | H16 | The ten-item hardening checklist with evidence | `meridian-harden-checklist-v1-draft` | `part-4-rulebook/`, `08-harden/` |
| `ship-notes` | H18 | Fixes for Ship, API and data assumptions, open questions | `meridian-harden-ship-notes-v1-draft` | `part-5-handoff/`, `08-harden/` |
| `hardened-design` | H18 | Ties it all together; what Ship reads | `meridian-harden-hardened-design-v1-draft` | `part-5-handoff/`, `08-harden/` |

## `derives_from` chain

This is what lets the stale-check flag Harden when Explore changes, and flag Ship's tickets when Harden changes.

- `scope` ← Explore's `design`, the combined wireframe, the Frame brief, the design system row
- `feasibility` ← `scope`, the engineer's answer source(s)
- `states`, `roles`, `edge-cases`, `accessibility` ← `scope` (and `feasibility` once answered)
- `tokens` ← Design v1 (without DS) or the design system row (with DS)
- `screens` ← the combined wireframe, `scope`, `states`, `roles`, `edge-cases`, `accessibility`, `feasibility`, `tokens`, the design system row
- `rulebook-chapter` ← the decisions, insights or sources its rules trace to
- `rulebook-check` ← `screens`, each `rulebook-chapter` used
- `checklist` ← every Harden artefact above
- `ship-notes` ← `rulebook-check`, `feasibility`, `checklist`
- `hardened-design` ← `screens`, `tokens`, `checklist`, `rulebook-check`, `ship-notes`

## Structures, one per type

### scope

```
## Screens
| Step | Screen | What the user does | Data shown or changed | Data from another system | AI touchpoint | Source |
## Roles
| Role | Who they are | Source |
## Data objects
- <object>: created, read, changed or deleted where. [medium] src: ...
## Target viewports
| Viewport | Size | Devices and context | Source |
## Inherited from Explore
- Design system gaps: <Q ids, or None>
- Assumptions blocking Harden: <A ids, or None>
## Out of scope
- <add-ons and anything outside Design v1's flow>
```

`Step` is the journey step number. `Data from another system` is `None` or the system the data comes from (the system of record; this product shows it but does not own it); any value but `None` makes a Partial state required. `AI touchpoint` is `None` or a short description. `Source` is a pointer or an assumption id. The `Screen` names in this table are the names every later artefact must use (the coverage check matches on them).

`Target viewports` lists every screen size the flow must work on, one row each. `Size` is `<width>×<height>` in CSS pixels (for example `1366×768`). `Devices and context` says what the device is and whether it is shared (a shared device needs the session timeout edge case). The row with the smallest width is the one the hardened screens must show.

### feasibility

```
| Question | Screen | Engineer's answer | Design impact | Source |
## Limits the engineer named
- <limit>. [medium] src: <engineer answer source> §<section>
```

Before H9 the answer, impact and source cells read `not yet known`. After H9 each answer cites the verbatim source file. An answer is never written by you.

### states

```
| Screen | State | What the user sees | Copy (draft) | How they recover or move on | Source |
```

`State` is one of: Empty, Loading, Error, Success, Partial, Stale, No permission, AI thinking, AI low confidence, AI wrong, AI override. Every screen needs Empty, Loading, Error and Success rows (with `Not applicable` and a reason in "What the user sees" if one cannot happen). Also required:

- **Partial** on every screen whose `Data from another system` in `scope` is not `None`.
- **No permission** on every screen where any row in `roles` has a `No`.
- The four AI states on every screen with an AI touchpoint in `scope`.

`Source` is a pointer, an assumption id, or `design decision` for a state the design team decided.

Then, if any screen has an AI touchpoint, one block per touchpoint (Ship checks and extends these rather than starting cold):

```
## AI touchpoints
### <touchpoint name> (<screen>)
- Trigger: <what makes the AI act>
- Who sees a wrong answer: <role>
- Who fixes it: <role, and how>
- How the user overrides or undoes it: <action>
- How it is logged: <where a wrong output and its fix are recorded, and who reviews them>
- Accepted suggestions audit-logged: <Yes: who accepted, what, when, where it is stored; or not yet known with a Q id>
```

No field is blank: unknown is `not yet known` with an open-question id. `Accepted suggestions audit-logged` is never `No`: if the system cannot log it, that is a gap for H10.

### roles

```
| Role | Screen or action | See | Change | Undo | Approve | Must not see | Source |
```

Cells in See, Change, Undo, Approve: `Yes`, `No`, `Own only`, or `not yet known`. `Screen or action` is a screen name from `scope`, or `<screen>: <action>` for an action on it. Any `No` makes a No permission state required on that screen.

Then two short sections, as plain lines or claim lines:

```
## If a permission changes mid-flow
## If the person who must act is away
```

The second says, for each approval or ownership step, who can act instead (a delegate, a fallback role) and what happens when nobody is named (who is told, after how long, how it is unblocked).

### edge-cases

```
| Edge case | Screen | What happens in Design v1 | Design response | Source |
```

The standard set must appear, each where it applies: long text, no data, a lot of data, concurrent edits, double submit, slow or no network, renamed or deleted item, permission removed, approver or owner away with no delegate, session timeout mid-task, and each target viewport (smallest first). `lint_harden.py` checks that long text, no data, a lot of data, double submit, no delegate and session timeout appear by name. A case that cannot happen in this flow stays as a row that says why. Domain cases cite their source.

### accessibility

```
Standard: WCAG 2.2 AA
| Check | Screen | Result | Detail | Fix |
## Contrast
<paste of contrast_check.py output, or the pairs table>
```

`Result`: `Pass`, `Fail`, or `Not checked` (needs a real test; say which). Every screen appears at least once.

### tokens

```
## Colour
| Token | Value | Use | Source |
## Type
| Token | Value | Use | Source |
## Spacing
| Token | Value | Use | Source |
## Radius
| Token | Value | Use | Source |
## Contrast pairs
| Foreground | Background | Use |
```

Token names are CSS custom property names without the dashes (`color-text`, `space-2`). Colour values are hex. `Source` points to the design system version (with DS) or the Design v1 wireframe (without DS). `export_tokens.py` reads this file; `contrast_check.py` reads the Colour and Contrast pairs tables.

### screens (`.html`)

Self-contained HTML, front matter in a leading comment. Each screen is a section containing `Step N: <screen name from scope>`; each state inside it carries `State: <state>`. Each screen is shown at the smallest target viewport, labelled `Viewport: <name> <width>×<height>`. Ends with a "Fixes applied in this version" list and a "Design system gaps" section. Add-ons never appear in it.

### rulebook-chapter

Uses the chapter format in `rulebook.md`: `## Purpose`, `## Rules`, `## Patterns`, `## Decisions`, `## Checks`, `## Instructions for AI tools`, `## Owner`. Each rule is a line `- R<n> (must|must not): <rule>. src: <pointer>`. The chapter's topic goes in the name (`rulebook-chapter-request-status`).

### rulebook-check

```
| Rule | Screen and state | Result | Reason | Action |
```

`Rule` is `<chapter topic> R<n>`. `Result`: `Pass`, `Break`, `Not applicable`. `Action` for a Break: `Fixed in screens v<n>`, `Ship note SN<n>`, `Send back`, or `Rule conflict Q<n>`; otherwise `-`.

### checklist

```
| Item | Result | Evidence | Gaps or notes |
```

The ten items, in this order and wording (the first nine are the workbook's; the tenth covers screen sizes):

1. Empty, loading, error and success states for every screen
2. Each role sees what it should, and nothing it shouldn't
3. Permissions: who can see, change and undo each thing
4. Edge data: long names, no data, a lot of data
5. Keyboard use and colour contrast checked
6. AI states: thinking, low confidence, wrong answer, override or undo
7. Feasibility checked with an engineer, limits noted
8. Checked against the system as a whole
9. Rulebook checks passed, or fixes listed for Ship
10. Every screen works at the smallest target viewport as well as large screens

`Result`: `Pass`, `Gap`, `Not applicable`. `Evidence` names the artefact and version.

### ship-notes

```
## Fixes travelling to Ship
| Id | Note | Screen and state | Why it was not fixed in Harden | Owner |
## API and data assumptions
- <assumption the build relies on>. [medium] src: <feasibility source> §<section>
## Open questions for Ship
- <Q ids and one line each, or None>
## Out of scope
- <what Ship should not build from this>
```

Ids are `SN1`, `SN2`, ... (Ship note, so they never clash with Ship's step numbers) and match the `Action` column in `rulebook-check`.

### hardened-design

Links, by name and version: `screens` (and its Figma link), `tokens`, `scope`, `states`, `roles`, `edge-cases`, `accessibility`, `feasibility`, every `rulebook-chapter` used, `rulebook-check`, `checklist`, `ship-notes`. Then the counts (screens, states, roles, Ship notes, open questions) and a Basis list of claim lines.

## Feeding the registers

- A role, permission, data behaviour or system behaviour with no source becomes an assumptions-register row (stage `harden`). A Harden finding that confirms or challenges an Explore or Frame assumption updates that row and is logged.
- Every engineer question is an open-questions row, asked of the engineer, blocking Harden H9 until answered. Questions that remain at handoff block Ship.
- Explore's design system gaps are closed in H11 (resolved, a proposed component, or carried to Ship as a note).
- The hardened screens pasted on Figma, the tokens file and the design library repo are artefact-registry rows with their pointer, link and version.
