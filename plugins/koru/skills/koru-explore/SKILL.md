---
name: koru-explore
description: Guides a Koru designer through the whole Explore stage (stage 2 of Frame, Explore, Harden, Ship), from the final framed brief (the Frame export, or frame.md) to design directions, 2 user journeys, wireframes for Idea A and Idea B with rationale and UX/UI add-ons, and a combined Design v1 after concept testing. Works together with koru-core, which holds the shared rules, logs, naming, registers and integrity checks. Use this whenever the designer refers to frame.md or the Frame export, says they are starting Explore or ideation, or asks for design directions, user journeys, wireframes for two ideas, UX/UI add-ons, combining ideas after concept testing, Design v1, or the Explore handoff card, even if they don't name the skill. Also use it to resume an Explore stage in progress.
---

# Koru Explore: idea generation

**Start every session by loading `koru-core`** (its `SKILL.md`: the never-bend rules, the step loop, checkpoints, the session start and resume protocol, the tone). Read its references as the moment arises: the file protocol, engagement scaffolding, governance, integrity checks, registers, and the Explore section of `koru-core/references/stages.md`. This skill expects **koru-core v1**; if the installed core differs, say so before doing step work. This skill does not restate core's rules; where it says "the rules", it means core's.

## What this skill is for

This skill takes the Explore stage from the framed brief to two ideas (Idea A and Idea B), and then to one combined design (Design v1) after concept testing. It does every AI step in the Explore workflow and tells the designer when it is their turn.

The designer stays in charge. Claude drafts, the designer decides. Claude never moves to the next part until the designer confirms.

**Terms.** Explore has four **parts** (1 Directions, 2 Journeys, 3 Wireframes, 4 Concept testing). "Stage" always means Frame, Explore, Harden or Ship. **Design v1** is the `design` artefact and the combined wireframe, insight decisions and add-ons it links.

## At a glance

1. **Directions** (A1 to A8): AI reads the Frame export and proposes 2 to 3 directions (persona, problem, direction, assumptions); the designer edits until one is final. Checks: design lead checks the final direction; the designer confirms Checkpoint 1.
2. **Journeys** (A9, A10): AI drafts 2 user journeys, one per idea, that differ in a meaningful way. Checks: design lead; the designer confirms Checkpoint 2.
3. **Wireframes** (A11 to A17): AI builds one self-contained HTML wireframe per idea from the design system, with rationale and separate UX/UI add-ons; the designer reviews, asks for changes, shares and pastes on Figma by hand. Checks: design lead, before anything is shared.
4. **Concept testing and Design v1** (B1 to B4): the designer brings real insights (AI never invents them); AI shows how each shapes the combined design, then builds Design v1. Checks: design lead; signs: team lead, with an organiser playing the client.

## How to run it

At the start of every reply, show where the work is:

```
Part: [1 Directions / 2 Journeys / 3 Wireframes / 4 Concept testing]
Step: [step number from the map below]
Next: [what happens next, and whether it is the designer's turn or Claude's]
```

End every reply that reaches a checkpoint with a clear question to the designer, and stop.

Every step runs core's step loop. When the orchestrator calls this skill with `engagement=<path> step=<step id>`, go straight to that step after core's session start.

## Step map

| # | Who | Step | Checker (core's second person) |
| --- | --- | --- | --- |
| A1 | Designer | Start Claude Code | |
| A2a | Designer | With DS: link the existing design system | |
| A2b | Designer | Without DS: link the internal wireframes Figma DS | |
| A3 | Designer | Attach this skill and share frame.md when Claude asks (in an engagement: Claude builds the Frame export) | |
| A4 | Claude | Give design directions in a fixed structure | Design lead (with the final direction) |
| A5 | Designer | Approve and overwrite the directions | |
| A6 | Claude | Ask for missing inputs | |
| A7 | Designer | Talk with Claude until the direction is final | Design lead checks the final direction |
| A8 | Designer | **Checkpoint 1:** confirm to start ideation | |
| A9 | Claude | Create 2 user journeys | Design lead |
| A10 | Designer | **Checkpoint 2:** confirm to start wireframing | |
| A11 | Claude | Create wireframes for both ideas | Design lead |
| A12 | Claude | Share the rationale and key job for each idea | Design lead |
| A13 | Claude | Share UX/UI add-ons, separately | Design lead |
| A14 | Designer | **Checkpoint 3:** review both ideas | |
| A15 | Designer | Ask for changes (Claude makes them) | Design lead, before A16 |
| A16 | Designer | Download as HTML, share for feedback, paste on Figma | |
| A17 | Claude | Save as Idea A and Idea B | |
| B1 | Designer | Get insights on both ideas | |
| B2 | Designer + Claude | Combine both ideas into one wireframe | Design lead |
| B3 | Claude | Share UX/UI add-ons, separately | Design lead |
| B4 | Claude | Save as Design v1 | Design lead checks; team lead signs |
| After | Designer + Claude | Without DS only: theme exploration | |

A checkpoint is the designer's confirmation, not the second-person check (core, "Checkpoints"). Both are needed before the next part starts.

## Starting Explore

1. Follow core's session start and resume protocol. If the engagement exists but Explore has not started, run `koru-core/scripts/init_stage.py --engagement <project> --stage-dir <this skill>`. It creates `stages/explore/` (drafts in `part-1-directions/`, `part-2-journeys/`, `part-3-idea-a/`, `part-3-idea-b/`, `part-4-design-v1/`, plus `sources/`), the final folder `06-explore/`, the templates and the step tracker.
2. **Core additions.** If `koru-core/references/governance.md` still has the old Explore rows (signed by the designer, no team lead), tell the user that the rows in `references/core-additions.md` need adding to core and offer to apply them. Until they are added, use them as written there and log that you did.
3. **The roles gate.** Explore requires: Designer, Design lead, Team lead, Second-person checker pool, plus the client's decision makers and the review rhythm. `koru-core/scripts/check_roles.py` must pass before A4. While it fails, stop and ask. The designer and the design lead must be different people.

## First step: get the framed brief

**In an engagement** (a folder with `00-read-me-first.md`), do not ask the designer to attach frame.md. Build it:

```bash
python3 scripts/export_frame.py --engagement <project>
```

It writes `stages/explore/sources/<project>-frame-export-v<n>.md` from the **final** Frame artefacts in `01-framed-brief/` and `02-research/`, with each one listed in `derives_from`. It is never hand-edited. If it refuses (no final brief), say Frame has not handed on, and stop: Explore never starts from a draft. Read all of the export before moving on. Wherever this skill says "frame.md", it means this export.

**With no engagement**, ask the designer to share frame.md:

"Please share frame.md so I can start. You can attach the file or give me its path in the project."

Do nothing else until you have it. If the file can't be found or opened, say so and ask again. Once you have it, read all of it before moving on.

## Setup check (A1 to A3)

With frame.md read, check the rest of the setup before giving any directions. If one is missing, ask for it and stop.

1. **frame.md** has been shared and read (first step above).
2. **Design system.** Read the `**Design system:**` line in `00-read-me-first.md` (set at intake). Ask the designer only if it says "not decided" (or there is no engagement), then record the answer in that line and in the decisions log. Confirm which path the project is on:
   - **With DS:** the designer has linked the existing design system. Use only its components and tokens.
   - **Without DS:** the designer has linked the internal wireframes Figma DS. Use its components.

   The design system is a source: make sure it has a row in the artefact registry (Figma pointer and version), so every wireframe can list it in `derives_from`.
3. **Output folder.** In an engagement, files go in `stages/explore/drafts/<part folder>/` (`references/files.md`). With no engagement, ask where to save files if it isn't clear. Default to an `explore/` folder in the project.

Then confirm back in two or three lines: what the brief is about, which DS path you're on, and where files will be saved.

## Part 1: Design directions (A4 to A7)

### A4: Give directions

Read frame.md and propose 2 to 3 design directions, unless the designer asks for a different number. Each direction must use this structure:

```
### Direction [letter]: [short name]
- User persona: [who it is for, from frame.md]
- Problem it solves: [one or two sentences]
- Design direction: [the approach, in two to four sentences]
- Assumptions: [anything not stated in frame.md; write "None" if there are none]
```

Base every direction on frame.md. If you assume something the brief doesn't say, put it under Assumptions so the designer can check it.

Save them as `<project>-explore-direction-options-v1-draft.md` (`part-1-directions/`), with a `src:` pointer on the persona and problem lines and each assumption added to the assumptions register (stage `explore`).

Stop and ask the designer to approve, edit or overwrite the directions (A5).

### A6: Ask for inputs

After the designer responds, ask for anything you still need to refine the directions. Ask only what changes the outcome, for example missing user context, the platform, the main flow to focus on, or constraints. Ask at most five questions at a time.

### A7: Refine until final

Update the directions with the designer's edits and answers. Repeat A6 and A7 as many times as needed. Don't push the designer to finish.

When the designer says a direction is final, restate it in the same structure as **Final direction**, and save it as `<project>-explore-direction-final-v1-draft.md` (`part-1-directions/`).

**Checker:** the design lead checks the final direction (persona and problem traced to the Frame export, every assumption in the register).

### Checkpoint 1 (A8)

Ask: "Shall I start ideation and create the 2 user journeys?" Do not create journeys until the designer confirms and the design lead has passed the final direction.

## Part 2: User journeys (A9)

Create 2 user journeys, one for each idea, both serving the final direction. The two ideas should differ in a meaningful way, not only in layout.

Use this structure for each:

```
## Idea [A/B]: [short name]
- Persona: [from the final direction]
- Goal: [what the user wants to get done]
- Starting point: [where and why the journey starts]

| Step | What the user does | What they see | What could go wrong | Opportunity |
| --- | --- | --- | --- | --- |

- End state: [what has been done when the journey ends]
```

Save as `<project>-explore-journey-idea-a-v1-draft.md` and `<project>-explore-journey-idea-b-v1-draft.md` (`part-2-journeys/`).

**Checker:** the design lead (both serve the final direction, they differ in more than layout, no invented user facts).

### Checkpoint 2 (A10)

Ask: "Shall I start wireframing both ideas?" Do not create wireframes until the designer confirms and the design lead has passed both journeys.

## Part 3: Wireframes, rationale and add-ons (A11 to A17)

### A11: Wireframes

Create wireframes for both ideas, covering the screens in each journey.

- **With DS:** use only the design system's components and tokens. If something you need isn't in it, use the closest component and list the gap. Don't invent new components without saying so.
- **Without DS:** use the internal wireframes Figma DS components.
- Build each idea as one self-contained HTML file, so the designer can download it, share it for feedback and paste it on Figma.
- Show screens in journey order, each labelled with its journey step.

Save as `<project>-explore-wireframe-idea-a-v1-draft.html` (`part-3-idea-a/`) and `-idea-b-` (`part-3-idea-b/`), front matter in a leading HTML comment. Each gap goes in the open-questions register (stage `explore`, blocking Harden).

**Checker:** the design lead (every journey step has a screen, only design system components, every gap listed).

### A12: Rationale

For each idea, share:

```
### Idea [A/B]: [short name]
- Why this idea: [two or three sentences linked to the final direction]
- Key job it solves: [one sentence]
```

Save as `<project>-explore-rationale-idea-a-v1-draft.md` and `-idea-b-`, in each idea's folder. **Checker:** the design lead.

### A13: UX/UI add-ons

Separately from the wireframes, list UX/UI add-ons that are not in the wireframes. These are enhancements to current features. Group them by ease of implementation:

```
| When | Add-on | Feature it improves | Why |
| --- | --- | --- | --- |
| Immediate | | | |
| Short term | | | |
| 1 year | | | |
```

Keep this list out of the wireframes so the designer can decide what to add.

Save as `<project>-explore-add-ons-idea-a-v1-draft.md` and `-idea-b-`, in each idea's folder. **Checker:** the design lead.

### Checkpoint 3 (A14)

Ask the designer to review both ideas, and stop.

### A15: Changes

Make only the changes the designer asks for. After each round, list what changed in one line per change. If a change to one idea affects the other, ask before changing both. Repeat until the designer is happy.

Each round that changes a wireframe is its next version (`-v2-draft.html`, …); the earlier one moves to `superseded/`.

**Checker:** before A16, the design lead checks both ideas. Only then mark them `review` (core rule 6: nothing is shared outside the team before that).

### A16: Designer's step

Remind the designer to download the HTML files, share them for feedback and paste them on Figma. Claude doesn't do this step. Ask for the Figma link to each pasted idea, and record it as `external_url` and as a registry row with its pointer.

### A17: Save

Save each idea in its own folder:

```
stages/explore/drafts/part-3-idea-a/   <project>-explore-wireframe-idea-a-v[n]-<status>.html, -rationale-idea-a-, -add-ons-idea-a-
stages/explore/drafts/part-3-idea-b/   <project>-explore-wireframe-idea-b-v[n]-<status>.html, -rationale-idea-b-, -add-ons-idea-b-
```

The journeys stay in `part-2-journeys/`. Number wireframe versions (v1, v2…) so feedback always refers to a fixed version. Don't overwrite an earlier version. Then list the set for each idea (exact file names and versions, and the Figma link), rebuild the artefact registry and run the stale-check.

## Part 4: Concept testing (B1 to B4)

### B1: Insights

Wait for the designer to share insights on both ideas. Don't invent or guess insights. If none have been shared, ask for them and stop.

Save what the designer gives, verbatim, as a source: `stages/explore/sources/<project>-explore-insights-concept-test-v1.md`. Add only a short header (who gave them, the date, which wireframe versions were tested) and a heading per insight (`## Insight 1`, …) so lines can point to it. A later round of insights is the next version, never an edit. If an insight challenges the brief (its problem, persona or success outcomes), say so: it is a send-back to Frame (core's send-back protocol), not something to fix in Explore.

### B2: Combine both ideas

Before building, show how each insight shapes the combined design, and wait for the designer to agree:

```
| Insight | Keep from Idea A | Keep from Idea B | Change |
| --- | --- | --- | --- |
```

Save it as `<project>-explore-insight-decisions-v1-draft.md` (`part-4-design-v1/`), with a Source column pointing to the insight (`src: <project>-explore-insights-concept-test-v1 §Insight 1`). Log the designer's agreement in the decisions log.

Then create one combined wireframe as a self-contained HTML file, using the same DS rules as A11: `<project>-explore-wireframe-combined-v1-draft.html` (`part-4-design-v1/`).

**Checker:** the design lead (every row traces to a real insight; the wireframe follows the agreed table and nothing else).

### B3: UX/UI add-ons

Share the add-ons list again for the combined design, in the same format as A13, separately from the wireframe. Save as `<project>-explore-add-ons-combined-v1-draft.md` (`part-4-design-v1/`). **Checker:** the design lead.

### B4: Save

Save as Design v1: `<project>-explore-design-v1-draft.md` (`part-4-design-v1/`), the `design` artefact that links:

```
stages/explore/drafts/part-4-design-v1/   -wireframe-combined-, -insight-decisions-, -add-ons-combined-, -design-
```

**Checker and signer:** the design lead checks Design v1; the team lead signs it off, with an organiser playing the client (the hackathon workbook's rule). When signed, the finals move to `06-explore/` as the next status (see `references/files.md`), then fill the handoff card (`references/handoff.md`).

## After Design v1: theme exploration (without DS only)

If the project has no design system, tell the designer that theme exploration comes next: once one wireframe is finalised, the design system is created using Claude in Figma, based on the wireframes. Don't start it unless the designer asks.

## Rules

These apply in Explore; the shared rules are in core.

- **Checkpoints are hard stops.** Never start journeys, wireframes or the combined design without the designer's confirmation.
- **The designer decides.** Offer options and reasons; don't choose for them.
- **Stay within frame.md.** Mark anything not in the brief as an assumption.
- **Don't invent research.** Personas, insights and findings come from frame.md or the designer.
- **Keep add-ons separate** from wireframes every time.
- **Keep copy plain.** Write labels, screen copy and notes in simple, direct language.

## Bundled resources

Read these when you reach the relevant moment; do not load them all up front.

| File | Read it when |
|---|---|
| `references/files.md` | Writing any Explore file: names, folders, `derives_from`, sources, moving to `06-explore/` |
| `references/handoff.md` | After B4: Explore's handoff card lines and what Harden reads |
| `references/core-additions.md` | Starting Explore, if core's Explore rows are not yet updated |
| `stage.json` | Read by core's `init_stage.py` (types, roles, folders, step tracker) |
| `assets/templates/` | Starting point for every Explore artefact type (the wireframe template is HTML) |
| `assets/stage/step-tracker.md` | The Explore step tracker appended to the read-me |
| `scripts/export_frame.py` | A3: build the Frame export from Frame's finals |
