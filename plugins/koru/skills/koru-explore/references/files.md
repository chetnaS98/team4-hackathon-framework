# Explore files: names, folders, what each derives from

Naming, status, front matter and traceable lines are core's (`koru-core/references/file-protocol.md`). This page only maps the source skill's files onto them. `<p>` is the project code name.

## Contents
- The file map
- Sources Explore keeps
- From draft to final
- Mapping from the source skill's names

## The file map

All drafts live under `stages/explore/drafts/`. Every file starts at `-v1-draft`; a change is the next version, never an overwrite.

| Step | Type | File | Folder | `derives_from` |
|---|---|---|---|---|
| A4 | direction | `<p>-explore-direction-options-v1-draft.md` | `part-1-directions/` | the Frame export |
| A7 | direction | `<p>-explore-direction-final-v1-draft.md` | `part-1-directions/` | the Frame export |
| A9 | journey | `<p>-explore-journey-idea-a-v1-draft.md`, `-idea-b-` | `part-2-journeys/` | the final direction |
| A11 | wireframe | `<p>-explore-wireframe-idea-a-v1-draft.html` | `part-3-idea-a/` | journey A, the final direction, the design system pointer |
| A11 | wireframe | `<p>-explore-wireframe-idea-b-v1-draft.html` | `part-3-idea-b/` | journey B, the final direction, the design system pointer |
| A12 | rationale | `<p>-explore-rationale-idea-a-v1-draft.md`, `-idea-b-` | each idea's folder | the final direction, that idea's journey and wireframe |
| A13 | add-ons | `<p>-explore-add-ons-idea-a-v1-draft.md`, `-idea-b-` | each idea's folder | that idea's wireframe |
| B2 | insight-decisions | `<p>-explore-insight-decisions-v1-draft.md` | `part-4-design-v1/` | the insights source, both idea wireframes |
| B2 | wireframe | `<p>-explore-wireframe-combined-v1-draft.html` | `part-4-design-v1/` | insight decisions, both idea wireframes, the design system pointer |
| B3 | add-ons | `<p>-explore-add-ons-combined-v1-draft.md` | `part-4-design-v1/` | the combined wireframe |
| B4 | design | `<p>-explore-design-v1-draft.md` | `part-4-design-v1/` | combined wireframe, insight decisions, combined add-ons, final direction |

Names in `derives_from` carry the version and no status (`<p>-explore-journey-idea-a-v2`). The design system is listed by its registry pointer (`figma:<fileKey>/<nodeId>@vN`). HTML files carry their front matter in a leading comment (template: `assets/templates/wireframe.html`).

After writing any of these, run `koru-core/scripts/lint_core.py <file> --engagement <p>` and fix what it reports before the checker sees it.

## Sources Explore keeps

In `stages/explore/sources/`. Sources are never edited; a change is a new version.

| Source | Name | Written by |
|---|---|---|
| The Frame export (the source skill's frame.md) | `<p>-frame-export-v<n>.md` | `scripts/export_frame.py` only |
| Concept-testing insights (B1) | `<p>-explore-insights-concept-test-v<n>.md` | The designer's words, verbatim; only a header and `## Insight <n>` headings added |
| Feedback on Idea A and Idea B, if the designer shares it as text | `<p>-explore-feedback-idea-a-v<n>.md` | Verbatim |

## From draft to final

1. Draft (`-draft`): written by Claude, linted.
2. Review (`-review`): after the design lead's check. Ideas A and B must be `review` before they are shared for feedback (A16).
3. Final (`-final`): after the sign-off in core's governance (design lead checks; the team lead signs Design v1 and the handoff). Run the stale-check first: no open warnings. Then put the final copy in `06-explore/`, rename the draft's status, and log the sign-off. Superseded versions go to `superseded/` next to the draft.

What goes to `06-explore/` at the end: the final direction, both journeys, Idea A and Idea B (wireframe, rationale, add-ons), the insight decisions, the combined wireframe and add-ons, and Design v1. The A4 options file stays in drafts. Tell the user which finals to upload to project knowledge; Figma frames get the `Final` section status.

## Mapping from the source skill's names

| Source skill | koru-explore |
|---|---|
| `explore/direction-final.md` | `part-1-directions/<p>-explore-direction-final-v1-draft.md` |
| `explore/idea-a/journey.md` | `part-2-journeys/<p>-explore-journey-idea-a-v1-draft.md` |
| `explore/idea-a/wireframes-v[n].html` | `part-3-idea-a/<p>-explore-wireframe-idea-a-v[n]-draft.html` |
| `explore/idea-a/rationale.md` | `part-3-idea-a/<p>-explore-rationale-idea-a-v1-draft.md` |
| `explore/idea-a/add-ons.md` | `part-3-idea-a/<p>-explore-add-ons-idea-a-v1-draft.md` |
| (Idea B the same) | (`idea-b`, `part-3-idea-b/`) |
| `explore/design-v1/wireframes.html` | `part-4-design-v1/<p>-explore-wireframe-combined-v1-draft.html` |
| `explore/design-v1/insight-decisions.md` | `part-4-design-v1/<p>-explore-insight-decisions-v1-draft.md` |
| `explore/design-v1/add-ons.md` | `part-4-design-v1/<p>-explore-add-ons-combined-v1-draft.md` |
| (none: Design v1 was the folder) | `part-4-design-v1/<p>-explore-design-v1-draft.md`, which links the three above |
