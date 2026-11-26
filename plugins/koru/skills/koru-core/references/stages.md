# The stages: what each hands on and expects

Core is phase-agnostic, but it must know enough about each phase to scaffold, check and hand off between them. This file holds that context, one section per stage. A phase skill owns its steps and templates; this file owns only what other stages and core depend on. Where a section says Proposed, it is an inference from the source document and needs the team's confirmation (it is also listed in `defaults.md`).

## Contents
- The four stages in one table
- Terminology: stage, part, checkpoint
- Frame
- Explore
- Harden
- Ship

## The four stages in one table

| Stage | Takes in | Hands on | Final folders at the root |
|---|---|---|---|
| Frame | Raw client material | The framed brief and research pack | `01-framed-brief/`, `02-research/` |
| Explore | The final framed brief and research pack, and the design system path | A combined design (Design v1) with its insight decisions and add-ons | `06-explore/` (Proposed) |
| Harden | Design v1 (and the design system gaps) | To be defined by the Harden skill; owns the rulebook and design library | `03-rulebook/`, `04-design-library/` (reserved) |
| Ship | To be defined by the Ship skill | To be defined by the Ship skill | To be defined |

## Terminology: stage, part, checkpoint

- **Stage** always means one of Frame, Explore, Harden, Ship. The Explore source document calls its four internal blocks "Stage 1 to 4" (directions, journeys, wireframes, concept testing); in koru-core and in a rebuilt Explore skill these are **parts** (Part 1 to Part 4), so "stage" is never ambiguous.
- **Checkpoint**: a hard stop in a phase where a named person confirms before the next step begins. Explore has three (confirm to start ideation, confirm to start wireframing, review both ideas). A checkpoint confirmation is logged in the decisions log (stage, who, date). A checkpoint is not a substitute for the second-person check: if the person confirming is also the person running the session, a different person still checks the artefact (see Explore, below).

## Frame

Described in `koru-frame`. For hand-off purposes: it hands on a `final` framed brief and research pack (1 or 2 personas, 5 to 8 JTBDs, a scan of 3 to 5 products), the confidence counts, the open questions and assumptions that block Explore, and a stale-check with no open warnings. Its handoff test is "write two direction cards without going back to the client". Explore takes the brief as its input.

## Explore

Source: the Explore skill document ("explore-idea-generation"). It takes a designer from the framed brief to two ideas (Idea A, Idea B) and then to one combined design (Design v1) after concept testing. The designer decides at every checkpoint; Claude drafts.

### Inputs

- **The framed brief and research pack, `final`.** The source document reads a single file called `frame.md`. In a koru-core engagement `frame.md` is an export of the final Frame artefacts, not a separately written file: it is generated from the final brief and the research pack index, names the versions it was built from, lists them in `derives_from`, and is never hand-edited. If a final Frame artefact changes, `frame.md` is regenerated as a new version and the stale-check flags everything in Explore built on the old one. (Proposed.) If `frame.md` is not available, Explore reads the final brief and pack directly; it never starts from a draft.
- **The design system path**, recorded once in the read-me ("Design system"): **with DS** (the existing design system is linked; use only its components and tokens) or **without DS** (the internal wireframes Figma design system is linked). The design system is a source: it is registered in the artefact registry (a Figma row with its pointer and version), and every wireframe lists it in `derives_from`, so a change to the design system flags the wireframes built on it.

### Parts and steps

| Part | Steps | What happens | Who decides |
|---|---|---|---|
| 1 Directions | A4 to A8 | Claude proposes 2 to 3 design directions in a fixed structure (persona, problem it solves, direction, assumptions); the designer approves, edits or overwrites; Claude asks up to five questions at a time; the designer says when a direction is final; Claude saves the final direction. **Checkpoint 1**: confirm to start ideation | Designer |
| 2 Journeys | A9, A10 | Claude creates 2 user journeys, one per idea, both serving the final direction and differing in a meaningful way. **Checkpoint 2**: confirm to start wireframing | Designer |
| 3 Wireframes | A11 to A17 | Claude builds one self-contained HTML wireframe per idea, in journey order, using only the design system (listing any gap), plus a rationale and key job per idea and a separate UX/UI add-ons list (Immediate, Short term, 1 year). **Checkpoint 3**: the designer reviews both ideas. Changes are made only as asked, one line per change. The designer downloads the HTML, shares it for feedback and pastes it on Figma (a human step). Claude saves Idea A and Idea B, with numbered wireframe versions | Designer |
| 4 Concept testing | B1 to B4 | The designer brings insights on both ideas (Claude never invents them). Claude shows how each insight shapes the combined design (keep from A, keep from B, change); the designer agrees; Claude builds one combined wireframe and a separate add-ons list; saves Design v1 | Designer |
| After | | Without a design system only: theme exploration, creating the design system in Figma from the finalised wireframe. Not started unless the designer asks | Designer |

### Artefacts (types the Explore skill registers)

Proposed types and typical names, following `file-protocol.md` (`[project]-explore-[artefact]-v[n]-[status]`):

| Type | Contains | Typical name | Form |
|---|---|---|---|
| `direction` | A design direction in the fixed structure; the final direction is one of them | `meridian-explore-direction-final-v1-draft` | `.md` |
| `journey` | One user journey: persona, goal, starting point, step table, end state | `meridian-explore-journey-idea-a-v1-draft` | `.md` |
| `wireframe` | One idea's self-contained wireframe, or the combined design | `meridian-explore-wireframe-idea-a-v2-draft` | `.html` with the front matter in a leading comment |
| `rationale` | Why this idea (linked to the final direction) and the key job it solves | `meridian-explore-rationale-idea-a-v1-draft` | `.md` |
| `add-ons` | UX/UI enhancements not in the wireframes, by ease of implementation | `meridian-explore-add-ons-idea-a-v1-draft` | `.md` |
| `insight-decisions` | The insight-by-insight table: keep from A, keep from B, change | `meridian-explore-insight-decisions-v1-draft` | `.md` |
| `design` | Design v1: the combined design, tying together its wireframe, decisions and add-ons | `meridian-explore-design-v1-draft` | `.md` (links the HTML) |

The source document's file names (`explore/direction-final.md`, `explore/idea-a/journey.md`, `wireframes-v[n].html`, `explore/design-v1/...`) map onto these. The rule "number wireframe versions and never overwrite an earlier one" is core's versioning rule applied; the folder layout is `stages/explore/drafts/` with sub-folders per idea (`idea-a/`, `idea-b/`, `design-v1/`).

### How Explore meets core's rules

- **Assumptions.** The "Assumptions" line in every direction is not free text: each assumption gets a row in the assumptions register (stage `explore`, artefact named), and anything the brief does not say stays visibly marked. "Stay within the brief" is core's rule 1 and rule 2.
- **Concept-testing insights are sources.** Insights the designer brings (B1) enter as new source files (converted verbatim, kept in the knowledge base) so they flow into `insight-decisions` as traceable lines with `src:` pointers. Claude never writes an insight itself; an insight with no source is an assumption.
- **Share for feedback.** Idea A and Idea B are shared for feedback (A16). Core's rule 6 applies: the client, and anyone outside the team, sees only artefacts at `review` or `final`, so each idea is checked by a second person and marked `review` before it is shared.
- **Send-back to Frame.** If concept testing challenges the brief (a problem, a persona, a success outcome), it goes back as a send-back (`registers.md`): the brief gets a new version, the client re-confirms if Frame's trigger is met, and the stale-check flags everything in Explore built on the old brief.
- **Design system gaps.** The "list the gap" rule produces a gap list. Gaps are recorded in the open-questions register (stage `explore`, blocking Harden) and handed to Harden, which owns the design library.
- **Checkpoints.** Claude never starts the next part before the checkpoint confirmation. Each confirmation is logged.

### Roles and sign-off (Proposed)

- Required roles: **Designer** (runs the session with Claude and decides at the checkpoints), **Design lead** (checks the artefacts, as the second person), and the **second-person checker pool**. The designer confirms checkpoints; the design lead, who did not run the step, checks each artefact before it is `review` or `final`.
- Sign-off rows are in `governance.md`. Client confirmation: the source document defines none. Until the team defines one, the client confirms nothing in Explore, and any change that touches the brief's problem or success outcomes goes back to Frame.
- Size thresholds: the source document has a fixed shape (2 to 3 directions, 2 journeys, 2 ideas, 1 combined design), so size is better set by the number of journeys, screens and flows than by Frame's source-file count. Not defined yet.

### What Explore hands on (Proposed handoff card entries)

| Field | Explore's entry |
|---|---|
| What we hand on | Design v1 (combined wireframe, insight decisions, add-ons), the final direction, the two journeys, Ideas A and B with rationale and add-ons, the design system gap list, and the open assumptions and questions that block Harden |
| What the next stage must be able to do with it | Harden the design without going back to the designer for the reasons behind it: every design decision traces to an insight or to a named assumption, and every component used is in the design system or listed as a gap |
| What it doesn't include | Production-ready design, a finished visual theme (without a design system, theme exploration comes after Design v1), engineering specifications, and any testing not yet done |

### Gaps and mismatches to resolve

1. Frame's handoff test says "two direction cards"; Explore proposes 2 to 3 directions unless the designer asks otherwise. Core reads this as "at least two".
2. Explore's checkpoints are the designer's own confirmations; core requires a second person to check AI-led output. Resolved above by the design lead check (Proposed).
3. Explore's file names and `explore/` folder do not follow core's naming and front matter; resolved by the mapping above when the Explore skill is rebuilt as `koru-explore`.
4. Wireframes are HTML files. Core now reads front matter in a leading HTML comment, so HTML artefacts are linted, registered and stale-checked like Markdown ones.
5. Who owns theme exploration and creating the design system (the tail of Explore, or Harden's design library) is not stated; left open in `defaults.md`.
6. The step status header Explore shows at the start of every reply (Stage, Step, Next) is a phase convention and compatible with core's "announce" step; it does not need to move into core.

## Harden

No source document has been supplied yet. What core already knows: Harden owns the rulebook and the design library (folders `03-rulebook/` and `04-design-library/` are reserved), a direction can be sent back from Harden to Explore, and a changed design flags tickets. Everything else is to be defined by the Harden skill.

## Ship

No source document has been supplied yet. What core already knows: a changed design flags tickets, and tickets and code live in Jira and GitHub (`file-protocol.md`). Everything else is to be defined by the Ship skill.
