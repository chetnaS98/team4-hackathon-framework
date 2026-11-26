# The rulebook: chapters, freshness, and the check

The rulebook is the brain of the project: if it is out of date or full of junk, everything built from it will be too. It lives in `03-rulebook/` (finals only) and is owned by the rulebook owner. Harden is where it is written and checked; Ship and later projects read it.

## Contents
- The chapter format
- Writing a chapter (H14)
- Keeping it fresh
- Running the rulebook check (H15)
- Example

## The chapter format

Every chapter uses the same parts, in this order, as `##` headings:

| Part | What goes in |
|---|---|
| Purpose | Why this chapter exists, in one sentence |
| Rules | Must and must-not statements, one per line: `- R<n> (must\|must not): <rule>. src: <pointer>` |
| Patterns | Approved ways of solving common problems, each with an example (a screen and state in the hardened HTML) |
| Decisions | What was decided and why, each linked to a decisions-log date |
| Checks | What to verify before a design moves on; one check per rule at least |
| Instructions for AI tools | How Claude should apply this chapter, written as instructions ("When designing any X screen, include Y. Flag any screen without it.") |
| Owner | A name |

Rule ids (`R1`, `R2`, ...) are never reused inside a chapter. A retired rule stays, marked `(retired <date>)`, so old checks still resolve.

## Writing a chapter (H14)

1. **Find what exists.** Read `03-rulebook/`. A chapter that covers this flow's topic is used as is; changing it is a new version, signed again.
2. **Decide which chapters this flow needs.** One per topic the flow raises (for example: status and progress, AI suggestions, approvals, notifications). Keep it to the few that change this flow's design.
3. **Only rules that change a design decision.** For each candidate rule ask: would any screen in the hardened design look or behave differently because of it? If not, leave it out. Generic advice ("be consistent") is not a rule.
4. **Every rule traces.** A rule cites the insight, decision, engineer answer, accessibility standard or client constraint behind it. A rule with no source is an assumption and needs the rulebook owner's explicit agreement, logged.
5. **Write the AI instructions last**, from the rules and checks, so a later Claude session can apply the chapter without reading this conversation.

With a design system: also read the design system's own guidance and do not restate it; point to it. Without one: the first chapters usually include one on the tokens and components this flow uses.

## Keeping it fresh

- The rulebook owner is the only signer. Only `final` chapters go in `03-rulebook/`.
- Each chapter lists in `derives_from` what its rules trace to, so the stale-check flags it when an insight, a decision or the design system changes.
- At each Harden handoff the rulebook owner answers one question in the decisions log: "Is any rule in the chapters used here no longer true?" A yes is a new chapter version.
- A rule that has been broken and overridden three times is flagged for review: it is either wrong or not being taught.

## Running the rulebook check (H15)

1. List every rule in every chapter that applies to the flow.
2. For each rule, find every screen and state it applies to in the hardened HTML (the `Step N` and `State:` labels). A rule that applies everywhere is checked on every screen.
3. Record Pass, Break or Not applicable, with a one-line reason that names what you saw.
4. For each Break propose the action (`steps.md`, H15). Small fixes are made now as a new `screens` version and the rule re-checked. A Break the team chooses not to fix becomes a Ship note, so it travels instead of stalling the run.
5. A rule conflict (the client wants what a rule forbids) is never resolved by you: raise an open question for the rulebook owner and the client's decision maker, and log it.
6. The rulebook owner reads the report and passes it, or sends it back with what to recheck.

## Example (Deskly, from the workbook, shortened)

```
## Purpose
Make sure booking is fast and members always know what has been booked for them.

## Rules
- R1 (must not): The AI confirms a booking without the member seeing room, time and duration. src: deskly-frame-brief-v2 §Where AI fits
- R2 (must): Every AI booking can be undone in one tap. src: deskly-explore-insight-decisions-v1 §Insight 2

## Patterns
- Suggestion at the top of the list, labelled with why it was suggested (screens v2, Step 2, State: Success)

## Decisions
- Admins approve AI room releases for the first month (decisions log, 2026-11-26)

## Checks
- Undo exists on every booking confirmation (R2)
- Every suggestion shows its reason (R1)

## Instructions for AI tools
When designing any booking screen, include an undo and a visible reason for each suggestion. Flag any screen without them.

## Owner
<rulebook owner name>
```
