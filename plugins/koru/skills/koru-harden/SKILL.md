---
name: koru-harden
description: Guides a Koru team through the Harden stage (stage 3 of Frame, Explore, Harden, Ship), taking Explore's final Design v1 and turning it into a hardened design that Ship can build from. It covers every state, role and permission, edge cases, AI states, accessibility, a feasibility check with an engineer, the tokens file and design library, the rulebook and its checks, the hardening checklist, the Ship notes and the Harden handoff card. Works together with koru-core, which holds the shared rules, logs, naming, registers and integrity checks. Use this whenever someone says they are starting Harden or hardening, refers to Design v1 or the Explore handoff, or asks for states, edge cases, roles and permissions, an accessibility pass, a feasibility check, the rulebook or rulebook checks, the tokens file or design library, the hardening checklist, sending a direction back to Explore, or handing a design to Ship, even if they do not name the skill. Also use it to resume a Harden stage in progress.
---

# Koru Harden: the Harden phase

**Start every session by loading `koru-core`** (its `SKILL.md`: the never-bend rules, the step loop, checkpoints, the session start and resume protocol, the tone). Read its references as the moment arises: the file protocol, engagement scaffolding, governance, integrity checks, registers and `koru-core/references/stages.md`. This skill expects **koru-core v1**; if the installed core differs, say so before doing step work. This skill does not restate core's rules.

Harden takes the chosen direction from Explore (Design v1) and makes it hold up in a real product: every state, role and permission, the edge cases, the AI states, accessibility, and a feasibility check with an engineer. It ends with the rulebook checks, which are the gate into Ship. Most prototypes break here, so this stage is about finding what breaks before an engineer does.

## At a glance

1. **Intake (H1 to H4).** AI reads the final Design v1 and builds the scope inventory (screens, roles, data from other systems, AI touchpoints, target viewports) and drafts the engineer's questions. The design lead checks the scope; the designer confirms it.
2. **Harden (H5 to H10).** AI drafts every state of every screen (empty, loading, error, partial data, no permission, AI states), roles and permissions, edge cases and an accessibility pass. The design lead checks each one; the engineer answers the feasibility questions and signs them.
3. **Build (H11 to H13).** AI builds the tokens file and the hardened screens (every state, smallest target viewport shown). The rulebook owner checks the tokens; the design lead checks the screens.
4. **Rulebook (H14 to H17).** AI drafts rulebook chapters, checks every screen against every rule and fills the hardening checklist. The rulebook owner passes the checks; the engineer, rulebook owner and design lead sign.
5. **Handoff (H18, H19).** AI writes the Ship notes, the hardened design and the handoff card. The engineer reads the notes as Ship would; the design lead and rulebook owner sign the card.

**Harden fixes, it does not redesign.** If the direction will hold, fix it here. If it will not (it cannot be built, tested or made accessible as stated, or the fix would change the idea itself), send it back to Explore. Small issues travel to Ship as notes so the team keeps moving.

## Terms

- **Part** (1 Intake, 2 Harden, 3 Build, 4 Rulebook, 5 Handoff). "Stage" always means Frame, Explore, Harden or Ship.
- **Design v1** is Explore's final `design` artefact and everything it links: the combined wireframe, the insight decisions and the add-ons.
- **Gap**: anything Harden finds missing (a state, a permission, a component, a rule). Every gap ends in one of three places: fixed here, a Ship note, or a send-back.
- **Checkpoint**: a hard stop (H4, H10, H17). Core's checkpoint rule applies.

## Harden-only rules

The shared rules are in core. These apply in Harden.

- **Never start from a draft.** Harden reads Explore's `final` artefacts only. If Design v1 is not final, say Explore has not handed on, and stop.
- **Keep to the chosen direction.** Harden works on Design v1's flow only. Add-ons stay add-ons unless the designer moves one into scope, logged.
- **Every screen, every time.** Each check runs on every screen in the scope inventory. `scripts/lint_harden.py --scope` proves coverage; a check that skipped a screen is not done.
- **The standard set is always checked.** A Partial state for every screen that shows data from another system. A No permission state for every screen where any role is denied something. The standard edge cases, including an approver or owner who is away with no delegate, a session timeout mid-task and a double submit. For every AI touchpoint: who sees a wrong output, who fixes it, how it is logged, and an audit log of every accepted suggestion with who accepted it. Every screen at the smallest target viewport as well as large screens. `lint_harden.py` enforces these.
- **Fix here, send back only if it won't hold.** Use the decision rule in `references/harden-review.md`. Never send back for something Harden can fix; never patch around something that needs a send-back.
- **Book the engineer early.** The feasibility questions go out at H3, before the state work, so answers arrive while you work.
- **Engineer answers are sources.** They enter verbatim in `stages/harden/sources/` and are cited with `src:`. Never write an engineer's answer yourself; an unanswered question stays "not yet known" and goes in the open-questions register.
- **No invented components or tokens.** With a design system, use only its components and tokens and list every gap. Without one, every token comes from Design v1 and is recorded in the tokens file. Never invent a value without saying so.
- **Looks like the real product.** Hardened screens use the tokens and the design system, never stripped-back wireframes.
- **Only rules that change a design decision.** A rulebook rule that would not change any screen is not added.
- **Make only the changes asked for.** List each change, one line per change. Every round is a new version.

## Show where the work is

At the start of every reply, show:

```
Part: [1 Intake / 2 Harden / 3 Build / 4 Rulebook / 5 Handoff]
Step: [step number from the map below]
Next: [what happens next, and whether it is a person's turn or Claude's]
```

End every reply that reaches a checkpoint with a clear question, and stop.

## Starting Harden

1. Follow core's session start and resume protocol. If the engagement exists but Harden has not started, run `koru-core/scripts/init_stage.py --engagement <project> --stage-dir <this skill>`. It creates `stages/harden/`, the final folders `03-rulebook/`, `04-design-library/` and `08-harden/`, the templates and the step tracker.
2. **Core additions.** If `koru-core/references/governance.md` still says "Harden: to be defined", tell the user that the Harden rows in `references/core-additions.md` need adding to core (sign-off rows, defaults, stage map) and offer to apply them. Until they are added, use them as written there and log that you did.
3. **The roles gate.** Harden requires: Designer, Design lead, Rulebook owner, Engineer, Second-person checker pool, plus the client's decision makers and the review rhythm. `koru-core/scripts/check_roles.py` must pass before H1. While it fails, stop and ask. If one person holds two roles, check `references/harden-review.md` ("Who does what") for which pairs are not allowed.
4. **First step: ask for the Explore handoff.** Ask: "Please share the Explore handoff card, or tell me where the final Design v1 is, so I can start." Do nothing else until you have it. Then read **all** of what `references/steps.md` lists under H1. Confirm back in three lines: what the flow is, which design system path you are on (from the read-me), and how many screens and roles you see.

## The step map

| # | Who | Step | Mode |
|---|---|---|---|
| H1 | Designer | Share the Explore handoff and Design v1; Claude reads everything | Human-led |
| H2 | Claude | Build the scope inventory: screens, roles, data, AI touchpoints | AI-led |
| H3 | Claude, then Designer | Draft the feasibility questions; the designer sends them to the engineer | AI-led |
| H4 | Designer | **Checkpoint 1:** confirm the scope and that the engineer is booked | Checkpoint |
| H5 | Claude | States for every screen, including AI states | AI-led |
| H6 | Claude | Roles and permissions | AI-led |
| H7 | Claude | Edge cases | AI-led |
| H8 | Claude + Design lead | Accessibility pass | AI-assisted |
| H9 | Engineer + Claude | Feasibility: the engineer answers; Claude records | Human-led |
| H10 | Designer + Design lead | **Checkpoint 2:** fix here, Ship note or send back | Checkpoint |
| H11 | Claude + Rulebook owner | Tokens file and design library | AI-assisted |
| H12 | Claude | Hardened screens (every screen, every state) | AI-led |
| H13 | Designer + Claude | Changes | AI-assisted |
| H14 | Claude + Rulebook owner | Rulebook chapters for this flow | AI-assisted |
| H15 | Claude | Run the rulebook checks | AI-led |
| H16 | Claude | Fill the hardening checklist, including system fit | AI-led |
| H17 | Engineer, Rulebook owner, Design lead | **Checkpoint 3:** the three sign-offs | Checkpoint |
| H18 | Claude | Ship notes and the hardened design | AI-led |
| H19 | Claude, then signers | The Harden handoff card | AI-led |

The playbook for each step is in `references/steps.md`; read the entry for the current step before doing it. After writing an artefact, run `koru-core/scripts/lint_core.py`, `koru-core/scripts/lint_lines.py` (traceable lines), then `scripts/lint_harden.py` (with `--scope` once the scope inventory exists; pass the `states` and `roles` artefacts together so it can check the No permission states), and fix what they report before handing it on.

## With a design system and without one

The read-me records the path. It changes three steps; everything else is the same.

| | With a design system | Without one |
|---|---|---|
| H11 tokens | Copy the design system's tokens into the tokens file, citing its version; resolve each Explore gap to the closest component or a proposed new component for the rulebook owner | Build the tokens file from Design v1 (colour, type, spacing, radius); set up the design library skeleton |
| H12 screens | Only the design system's components and tokens; list every gap | The tokens file and the internal wireframes components, styled to look like the product |
| H14 rulebook | Read the existing chapters first; add a chapter only for what they do not cover | Draft the first chapters for this flow |

Detail in `references/design-library.md`.

## Bundled resources

Read these when you reach the relevant moment. Shared references are in `koru-core`.

| File | Read it when |
|---|---|
| `references/steps.md` | Before running any step (one entry per step) |
| `references/artefacts.md` | Writing any Harden artefact: types, exact structures, naming, `derives_from` |
| `references/harden-review.md` | Checkpoints, who checks what, the fix-or-send-back rule, sign-offs, size |
| `references/rulebook.md` | H14 and H15: the chapter format, keeping the rulebook fresh, running the check |
| `references/design-library.md` | H11 and H12: tokens, the library skeleton, both design system paths |
| `references/handoff.md` | H18 and H19: the handoff card, Ship notes, send-back to Explore |
| `references/existing-skills.md` | When an outside skill might help with a step |
| `references/core-additions.md` | Once, when Harden first runs in an engagement whose core has no Harden rows |
| `stage.json` | Read by core's `init_stage.py` |
| `assets/templates/` | Starting point for every Harden artefact type |
| `scripts/lint_harden.py` | Harden's structure and coverage checks, after core's lints |
| `scripts/contrast_check.py` | H8 and H11: contrast ratios for the token pairs |
| `scripts/export_tokens.py` | H11: write `tokens.css` and `tokens.json` from the tokens artefact |
