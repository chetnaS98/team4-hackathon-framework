# Harden review: who checks, checkpoints, fix or send back, sign-off

The general checking rules, the roles registry, the sign-off matrix and the size thresholds are in `koru-core/references/governance.md`; checkpoints are defined in `koru-core/SKILL.md`. This file adds only what is specific to Harden. Everything here is Proposed until the team confirms it (see `core-additions.md`).

## Who does what

| Person | Role in Harden |
|---|---|
| Designer | Runs the session with Claude; confirms checkpoints 1 and 2; sends the engineer the questions; asks for changes |
| Design lead | The second person for design artefacts (scope, states, roles, edge cases, accessibility, screens, checklist); signs the hardened design |
| Rulebook owner | Owns `03-rulebook/` and `04-design-library/`; checks and signs chapters and the tokens file; passes the rulebook checks; decides proposed new components |
| Engineer | Answers the feasibility questions; signs the feasibility check; reads the Ship notes as Ship would |
| Second-person checker | Stands in when the usual checker ran the step |
| Client | Confirms nothing in Harden (Proposed). A rule that conflicts with what the client wants is an open question for the rulebook owner and the client's decision maker |

Pairs that may not be the same person: designer and design lead (the design lead checks what the designer ran); rulebook owner and whoever drafted a chapter by hand; the engineer who answered and the person who checks the feasibility artefact against the answer source (the design lead does that check). If the team is small, name a different checker from the pool and log it.

## Checkpoints

1. **Checkpoint 1 (H4): scope.** The designer confirms the scope; the design lead has passed it; the engineer is booked. Hardening does not start without all three.
2. **Checkpoint 2 (H10): fix, note or send back.** The designer and the design lead decide each gap. Nothing is built at H12 until this is logged.
3. **Checkpoint 3 (H17): sign-offs.** The engineer, the rulebook owner and the design lead each sign. Ship notes and the handoff do not start until all three are in.

Log each confirmation in the decisions log (stage `harden`, who, date, artefact affected).

## Fix here, Ship note, or send back

Default to **fix here**. Hardening exists to fix things.

| Decision | When | Examples |
|---|---|---|
| **Fix here** | The gap can be closed by adding or changing a state, a message, a permission, a component choice, a label or a layout detail, without changing what the idea is or which job it serves | A missing empty state; an error with no way back; a role that can see too much; a contrast failure; a list with no paging |
| **Ship note** | Small, does not change behaviour a user would notice, and an engineer can handle it while building; or it depends on something only known at build time | Exact debounce time; a copy tweak pending legal; which API field holds a value |
| **Send back to Explore** | The direction will not hold as stated: it cannot be built (the engineer says the data or action does not exist and no fix keeps the idea), it cannot be made accessible without changing the interaction model, it cannot be tested, or the fix changes the idea, the key job, a journey step, or something the client confirmed in Explore | An AI agent that must act instantly but the system syncs hourly; a drag-only interaction with no accessible equivalent that keeps the idea; removing the step users valued in concept testing |

When unsure between fix here and send back, ask: "After this fix, would the designer still describe the idea the same way?" If yes, fix here. If no, send back. When unsure between fix here and Ship note, fix here.

## Harden-specific checks (added to core's hand-over checklist)

1. Does every screen in the scope appear in states, roles, edge cases, accessibility and the hardened screens, with Partial where it shows data from another system, No permission where a role is denied, and the smallest target viewport shown? (`lint_harden.py --scope` proves it.)
2. Does every screen with an AI touchpoint have all four AI states, including how the user overrides or undoes it, who sees and fixes a wrong output, how it is logged, and the audit log of accepted suggestions?
3. Pick three permissions and three system behaviours: does each cite the feasibility source or an assumption id?
4. Is any engineer answer written in words the source does not contain?
5. Does the hardened HTML use only tokens and design system components, and list every gap?
6. Does every Break in the rulebook check have an action?
7. Was anything redesigned rather than hardened? Compare the hardened screens with Design v1's journey.
8. Is the version numbering unbroken?

## Sign-off rows (Proposed)

| Artefact | Checked by | Signed by | Client confirms |
|---|---|---|---|
| Scope, states, roles, edge cases, accessibility, checklist | Design lead | (checked, not signed) | No |
| Feasibility | Design lead (against the answer source) | Engineer | No |
| Tokens file, rulebook chapters | Rulebook owner | Rulebook owner | No |
| Rulebook check | Rulebook owner | Rulebook owner (passes it) | No |
| Hardened screens, hardened design | Design lead | Design lead | No (a change to something the client confirmed in Explore is a send-back) |
| Ship notes | Engineer (reads as Ship would) | Design lead | No |
| Handoff card | Ship's team | Design lead and rulebook owner | No |

## Size

Harden's size is set by screens and roles, not source files (`stage.json`):

| | Small | Large |
|---|---|---|
| Size | One flow, 5 or fewer screens, 1 or 2 roles | Several flows, more than 5 screens, or 3 or more roles |
| Review | Async: checkers comment within 1 working day, then the owner decides | Live: 45 to 60 minutes at each checkpoint |

Ask at H2 once the scope is known, propose a size, and log it.

## The Harden AI quality log

Use core's log and categories. Typical Harden entries: an engineer answer paraphrased into something the engineer did not say (`fabricated`); a screen skipped in a check (`missed`); a token value invented (`fabricated`); a permission stated as fact with no source (`overconfident`); a redesign instead of a fix (`ignored-instruction`); a state labelled differently from the scope's screen name (`format`).
