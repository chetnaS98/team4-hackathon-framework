---
name: explore-idea-generation
description: Guides a Koru designer through the whole Explore stage in Claude Code, from frame.md to design directions, 2 user journeys, wireframes for Idea A and Idea B with rationale and UX/UI add-ons, and a combined Design v1 after concept testing. Use this skill whenever the designer refers to frame.md, says they are starting Explore or ideation, or asks for design directions, user journeys, wireframes for two ideas, UX/UI add-ons, or combining ideas after concept testing, even if they don't name the skill.
---

# Explore: idea generation

## What this skill is for

This skill takes the Explore stage from the framed brief in frame.md to two ideas (Idea A and Idea B), and then to one combined design (Design v1) after concept testing. It does every AI step in the Explore workflow and tells the designer when it is their turn.

The designer stays in charge. Claude drafts, the designer decides. Claude never moves to the next stage until the designer confirms.

## How to run it

At the start of every reply, show where the work is:

```
Stage: [1 Directions / 2 Journeys / 3 Wireframes / 4 Concept testing]
Step: [step number from the map below]
Next: [what happens next, and whether it is the designer's turn or Claude's]
```

End every reply that reaches a checkpoint with a clear question to the designer, and stop.

## Step map

| # | Who | Step |
| --- | --- | --- |
| A1 | Designer | Start Claude Code |
| A2a | Designer | With DS: link the existing design system |
| A2b | Designer | Without DS: link the internal wireframes Figma DS |
| A3 | Designer | Attach this skill and share frame.md when Claude asks |
| A4 | Claude | Give design directions in a fixed structure |
| A5 | Designer | Approve and overwrite the directions |
| A6 | Claude | Ask for missing inputs |
| A7 | Designer | Talk with Claude until the direction is final |
| A8 | Designer | **Checkpoint 1:** confirm to start ideation |
| A9 | Claude | Create 2 user journeys |
| A10 | Designer | **Checkpoint 2:** confirm to start wireframing |
| A11 | Claude | Create wireframes for both ideas |
| A12 | Claude | Share the rationale and key job for each idea |
| A13 | Claude | Share UX/UI add-ons, separately |
| A14 | Designer | **Checkpoint 3:** review both ideas |
| A15 | Designer | Ask for changes (Claude makes them) |
| A16 | Designer | Download as HTML, share for feedback, paste on Figma |
| A17 | Claude | Save as Idea A and Idea B |
| B1 | Designer | Get insights on both ideas |
| B2 | Designer + Claude | Combine both ideas into one wireframe |
| B3 | Claude | Share UX/UI add-ons, separately |
| B4 | Claude | Save as Design v1 |
| After | Designer + Claude | Without DS only: theme exploration |

## First step: ask for frame.md

As soon as this skill is attached, ask the designer to share frame.md:

"Please share frame.md so I can start. You can attach the file or give me its path in the project."

Do nothing else until you have it. If the file can't be found or opened, say so and ask again. Once you have it, read all of it before moving on.

## Setup check (A1 to A3)

With frame.md read, check the rest of the setup before giving any directions. If one is missing, ask for it and stop.

1. **frame.md** has been shared and read (first step above).
2. **Design system.** Confirm which path the project is on:
   - **With DS:** the designer has linked the existing design system. Use only its components and tokens.
   - **Without DS:** the designer has linked the internal wireframes Figma DS. Use its components.
3. **Output folder.** Ask where to save files if it isn't clear. Default to an `explore/` folder in the project.

Then confirm back in two or three lines: what the brief is about, which DS path you're on, and where files will be saved.

## Stage 1: Design directions (A4 to A7)

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

Stop and ask the designer to approve, edit or overwrite the directions (A5).

### A6: Ask for inputs

After the designer responds, ask for anything you still need to refine the directions. Ask only what changes the outcome, for example missing user context, the platform, the main flow to focus on, or constraints. Ask at most five questions at a time.

### A7: Refine until final

Update the directions with the designer's edits and answers. Repeat A6 and A7 as many times as needed. Don't push the designer to finish.

When the designer says a direction is final, restate it in the same structure as **Final direction**, and save it as `explore/direction-final.md`.

### Checkpoint 1 (A8)

Ask: "Shall I start ideation and create the 2 user journeys?" Do not create journeys until the designer confirms.

## Stage 2: User journeys (A9)

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

Save as `explore/idea-a/journey.md` and `explore/idea-b/journey.md`.

### Checkpoint 2 (A10)

Ask: "Shall I start wireframing both ideas?" Do not create wireframes until the designer confirms.

## Stage 3: Wireframes, rationale and add-ons (A11 to A17)

### A11: Wireframes

Create wireframes for both ideas, covering the screens in each journey.

- **With DS:** use only the design system's components and tokens. If something you need isn't in it, use the closest component and list the gap. Don't invent new components without saying so.
- **Without DS:** use the internal wireframes Figma DS components.
- Build each idea as one self-contained HTML file, so the designer can download it, share it for feedback and paste it on Figma.
- Show screens in journey order, each labelled with its journey step.

### A12: Rationale

For each idea, share:

```
### Idea [A/B]: [short name]
- Why this idea: [two or three sentences linked to the final direction]
- Key job it solves: [one sentence]
```

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

### Checkpoint 3 (A14)

Ask the designer to review both ideas, and stop.

### A15: Changes

Make only the changes the designer asks for. After each round, list what changed in one line per change. If a change to one idea affects the other, ask before changing both. Repeat until the designer is happy.

### A16: Designer's step

Remind the designer to download the HTML files, share them for feedback and paste them on Figma. Claude doesn't do this step.

### A17: Save

Save each idea in its own folder:

```
explore/idea-a/   journey.md, wireframes-v[n].html, rationale.md, add-ons.md
explore/idea-b/   journey.md, wireframes-v[n].html, rationale.md, add-ons.md
```

Number wireframe versions (v1, v2…) so feedback always refers to a fixed version. Don't overwrite an earlier version.

## Stage 4: Concept testing (B1 to B4)

### B1: Insights

Wait for the designer to share insights on both ideas. Don't invent or guess insights. If none have been shared, ask for them and stop.

### B2: Combine both ideas

Before building, show how each insight shapes the combined design, and wait for the designer to agree:

```
| Insight | Keep from Idea A | Keep from Idea B | Change |
| --- | --- | --- | --- |
```

Then create one combined wireframe as a self-contained HTML file, using the same DS rules as A11.

### B3: UX/UI add-ons

Share the add-ons list again for the combined design, in the same format as A13, separately from the wireframe.

### B4: Save

Save as Design v1:

```
explore/design-v1/   wireframes.html, insight-decisions.md, add-ons.md
```

## After Design v1: theme exploration (without DS only)

If the project has no design system, tell the designer that theme exploration comes next: once one wireframe is finalised, the design system is created using Claude in Figma, based on the wireframes. Don't start it unless the designer asks.

## Rules

- **Checkpoints are hard stops.** Never start journeys, wireframes or the combined design without the designer's confirmation.
- **The designer decides.** Offer options and reasons; don't choose for them.
- **Stay within frame.md.** Mark anything not in the brief as an assumption.
- **Don't invent research.** Personas, insights and findings come from frame.md or the designer.
- **Keep add-ons separate** from wireframes every time.
- **Keep copy plain.** Write labels, screen copy and notes in simple, direct language.
