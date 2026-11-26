# Outside skills that can help in Harden

Core's principle holds: no outside skill overrides core rules. A skill may supply a method for a step, but its output goes into the Harden artefact in this skill's format, with claim lines, naming and status, and it never replaces the named checker. If a listed skill is not installed, do the step yourself from `steps.md` and do not claim to have used it.

## Cover part of a step

| Skill | Step | What it adds | What is missing |
|---|---|---|---|
| `design:accessibility-review` | H8 | A WCAG 2.1 AA audit method: contrast, keyboard, touch targets, screen reader | WCAG 2.2 additions (target size minimum, focus not obscured, redundant entry); this skill's table format; every-screen coverage |
| `design:design-system` | H11 | Audits naming and hardcoded values; documents a component's variants, states and accessibility notes | The tokens artefact format and `derives_from`; the rulebook owner's decision on new components |
| `design:design-critique` | H16 (system fit) | A structured usability, hierarchy and consistency review | The ten-item checklist; evidence pointers |
| `design:design-handoff` | H18 | A developer spec sheet: layout, tokens, props, states, breakpoints | It belongs mostly to Ship. In Harden use it only to check nothing a spec needs is missing from `ship-notes` |
| `design:ux-copy` | H5 | Wording for error messages, empty states and confirmations | The state table; the source column |

## Not a fit

- Anything that redesigns (idea generation, direction exploration): that is Explore's job, and in Harden it is a send-back.
- Ticket writers and PRD-to-ticket workflows: Ship's job. Harden hands Ship what it needs to write them.

## Already at Koru (find the people)

The workbook points to: the pre-approval checks designers already run before approval, the rulebook format on the Koru Delivery System page, the protocols written for the move to Figma, and the design change log skill. If the team uses one of these, record which in the decisions log and, where its checks are stricter than this skill's, follow the stricter one.
