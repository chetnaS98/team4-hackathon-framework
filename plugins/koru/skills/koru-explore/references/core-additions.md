# Additions to koru-core for Explore

The phase contract (`koru-core/references/phase-contract.md`) says a phase adds its sign-off rows, re-confirmation trigger, defaults section and stage-map entry to core when it is built. Core v1 has Explore's rows as "Proposed", inferred from the source document before `koru-explore` existed. Paste the blocks below into the named core files (or let Claude apply them, then log it in the decisions log, stage `core`). Until they are applied, Explore uses them as written here and logs that it did.

## 1. `koru-core/references/governance.md`, sign-off matrix

Replace the three Explore rows and the Explore handoff row with:

```markdown
| Explore | Direction options, final direction, journeys | Design lead | Designer (confirms at Checkpoints 1 and 2) | No |
| Explore | Wireframes, rationale and add-ons for Idea A and Idea B | Design lead (must be `review` before they are shared for feedback) | Designer (confirms at Checkpoint 3) | No |
| Explore | Insight decisions, combined wireframe, combined add-ons | Design lead | Designer (agrees the decisions table at B2) | No |
| Explore | Design v1 (the `design` artefact) | Design lead | Team lead | Yes (an organiser plays the client on the hackathon): the combined flow and key job. A change to the brief's problem or success outcomes is a send-back to Frame |
| Explore | Handoff card | Next stage's team | Team lead | No |
```

In "Re-confirmation triggers", replace the Explore row with:

```markdown
| Explore | Design v1 | The flow (its screens or journey steps), the key job it solves, or a keep-from-A / keep-from-B / change decision changes in meaning. Copy, layout and add-on changes do not count; when unsure, ask the team lead. A change touching the brief's problem or success outcomes is a send-back to Frame, and Frame's trigger applies |
```

## 2. `koru-core/references/defaults.md`, replace the "Explore" section

```markdown
## Explore

The `koru-explore` skill keeps the team's Explore skill ("explore-idea-generation") as written: its step map A1 to A17, B1 to B4 and "After", the direction structure, the three checkpoints and its rules. These are the defaults it uses to fit core; the team can confirm or change them.

| Item | Status | Default used |
|---|---|---|
| Explore's input file `frame.md` | Proposed | In an engagement, `koru-explore/scripts/export_frame.py` builds `stages/explore/sources/<project>-frame-export-v<n>.md` from the final Frame artefacts in `01-framed-brief/` and `02-research/`, lists each in `derives_from`, and is never hand-edited; it refuses if there is no final brief. With no engagement, the designer shares frame.md |
| Design system path | Proposed | Read from the read-me's `**Design system:**` line (set at intake); the designer is asked only if it says "not decided" |
| Required roles | Proposed | Designer, Design lead, Team lead, second-person checker pool |
| Who checks Explore artefacts | Proposed | The design lead checks every AI-led step (directions, journeys, wireframes, rationale, add-ons, insight decisions, Design v1); the designer's checkpoint confirmation is not the check |
| Who signs Design v1 and the handoff | Proposed | The team lead, with an organiser playing the client (hackathon workbook) |
| Sharing Idea A and Idea B for feedback | Proposed | Only at `review` or `final` (core rule 6), after the design lead's check |
| Concept-testing insights | Proposed | Saved verbatim as a source, `stages/explore/sources/<project>-explore-insights-concept-test-v<n>.md`, with only a header and `## Insight <n>` headings added |
| A4 direction options | Proposed | Saved as `<project>-explore-direction-options-v1-draft.md` so the assumptions have a home; later A7 rounds stay in the conversation until the final direction is saved |
| Size thresholds | Open | Not defined; Explore has a fixed shape. Until defined, use core's and log it |
| Number of directions | Proposed | 2 to 3 unless the designer asks otherwise |
| Draft folders | Proposed | `part-1-directions/`, `part-2-journeys/`, `part-3-idea-a/`, `part-3-idea-b/`, `part-4-design-v1/` |
| Final folder number | Proposed | `06-explore/` |
| Artefact types | Proposed | direction, journey, wireframe, rationale, add-ons, insight-decisions, design |
| Design system gap list | Proposed | Recorded in the open-questions register (stage `explore`, blocking Harden) and listed in Design v1 |
| Who owns theme exploration and creating the design system when there is none (after Design v1) | Open | Not started unless the designer asks |
| Wireframe form | Proposed | Self-contained HTML with core front matter in a leading HTML comment |
| Internal "Stage 1 to 4" naming | Confirmed in `koru-explore` | "Part 1 to 4"; the reply header is `Part / Step / Next` |
```

## 3. `koru-core/references/stages.md`, update the "Explore" section

Replace the first paragraph and the "Inputs" bullet about `frame.md` with:

```markdown
Described in `koru-explore`, which keeps the team's source skill ("explore-idea-generation") as written and adds only what core needs: the Frame export, file names, a design lead check per AI step, and the team lead's sign-off of Design v1. It takes a designer from the framed brief to two ideas (Idea A, Idea B) and then to one combined design (Design v1) after concept testing. The designer decides at every checkpoint; Claude drafts.

- **The framed brief and research pack, `final`.** `koru-explore/scripts/export_frame.py` builds `stages/explore/sources/<project>-frame-export-v<n>.md` (the source skill's `frame.md`) from the final artefacts in `01-framed-brief/` and `02-research/`, lists each in `derives_from`, and refuses if no final brief exists. It is never hand-edited; when a Frame final changes, re-running it writes the next version and the stale-check flags everything in Explore built on the old one.
```

In "Parts and steps", the folder sentence at the end of "Artefacts" becomes:

```markdown
The folder layout is `stages/explore/drafts/` with `part-1-directions/`, `part-2-journeys/`, `part-3-idea-a/`, `part-3-idea-b/` and `part-4-design-v1/`, plus `stages/explore/sources/` for the Frame export and the concept-testing insights. Finals go to `06-explore/`.
```

Replace "Roles and sign-off (Proposed)" with:

```markdown
### Roles and sign-off

- Required roles: **Designer** (runs the session and confirms the checkpoints), **Design lead** (checks every AI-led step as the second person), **Team lead** (signs Design v1 and the handoff card), and the **second-person checker pool**.
- Client confirmation: Design v1 only, with an organiser playing the client on the hackathon. Re-confirmation trigger in `governance.md`.
```

In "Gaps and mismatches to resolve", mark items 2, 3 and 6 as resolved by `koru-explore`.

## 4. `koru-core/references/engagement.md`, folder layout

The Explore line under `stages/` becomes:

```
    explore/  drafts/ sources/ templates/
```

## 5. `koru-core/scripts/init_stage.py`

It copies only `*.md` templates. Explore's wireframe template is `assets/templates/wireframe.html`. Change the glob to copy `*.md` and `*.html`. Until then, read the wireframe template from the skill's `assets/templates/`.

## 6. `koru-core/registry/roles.json`

No change: `Designer`, `Design lead`, `Team lead` and `Second-person checker pool` already exist.
