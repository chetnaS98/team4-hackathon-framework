# Frame artefact specs

The shared protocol (naming, status, front matter with `stage`, `derives_from` and `external_url`, the traceable-line format and its pointer forms, confidence levels, where things live) is in `koru-core/references/file-protocol.md`. In Frame a traceable line is called a **claim line**. This file is only what is specific to Frame.

## Contents
- Length limits
- Artefact types and what each contains
- The contradictions register
- Source files (Layer 1)

## Length limits (defaults for a small engagement)

| Type | Limit |
|---|---|
| persona | 1 or 2 in the pack |
| jtbd | 5 to 8 in the pack |
| competitive-scan | 3 to 5 products |
| research-pack | readable by a reviewer in one sitting |
| brief | one page |

Proposed: on a large engagement, scale persona, JTBD and scan limits per persona group or workflow.

## Artefact types and what each contains

Frame registers these types in `stage.json`.

| Type | Contains | Derives from |
|---|---|---|
| **insight** | One finding or insight per claim line. An insight explains what happened, why, and so what. Only insights carry design directions | Sources |
| **persona** | Who they are, needs, known pain points and friction, work conditions | Sources, insights |
| **workflow** | Steps today, who does what, pain points and friction per step, constraints | Sources |
| **jtbd** | The jobs people are trying to do, each linked to a persona: "When [situation], I want to [motivation], so I can [outcome]" | Personas, insights |
| **opportunity** | UX and AI opportunities, and where AI fits (screen, agent, both, neither). Derives from insight lines, never from a single quote | Insights, JTBDs, workflows |
| **competitive-scan** | 3 to 5 products: what each does well, what it misses, annotated screenshots | External sources |
| **research-pack** | A thin index, not a copy: TRACES answers, links to the final files pinned by version, open questions, a count of high, medium and low claims | The final persona, JTBD, workflow, insight and scan files |
| **brief** | The 9-section framed brief | All of the above |

Templates for each are in `assets/templates/`. Use the template, keep its headings, and delete guidance text as you fill it. Set `derives_from` in the front matter to the artefacts the file is built from (name with version, no status).

Several sources for one claim line are separated by `; `. A claim that has no source does not go under "What we know"; it moves to "What we're assuming" and gets a row in core's assumptions register.

## The contradictions register

A living `insight` file named `[project]-frame-insight-contradictions-vN-draft` (template `assets/templates/contradictions.md`). Each entry is one claim line: what conflicts, with both sides cited as `src:` pointers, then a sub-line giving Impact (High, Medium or Low on the framed brief), Status (Open or Resolved) and who can resolve it. Group entries as: the requirements document against the evidence; between the evidence sources; the current platform against the other sources. Compare numbers, definitions and scope, not only opinions (for example a measured 18 minutes against a quoted 40). Start it at step 5, update it at every step that reads new material, and let the brief's open questions and the gap check draw on it. A contradiction is resolved only by a person with authority or by new evidence; never mark one Resolved yourself.

## Source files (Layer 1)

Raw items are converted to `.md` with the markdown-research-formatter skill: `product_workflow_content-type[-qualifier]_vN.md`, lowercase, e.g. `deskly_booking_transcript-ops-lead_v1.md`. Required front matter: title, description, product, personas, lifecycle, workflow, research_type, content_type, date. Optional: customer, participants, status (`raw`, `cleaned`, `synthesized`, `final`), source_file, related, jira_confluence, tags, confidentiality, schema_version. Content types: transcript, synthesis, workflow-map, spreadsheet, guide, deck, notes, persona. The conversion adds nothing that is not in the source; inference is marked `(inferred)`. Originals stay untouched; revisions bump `vN`. HTML sources (mocks, pages) are copied into `stages/frame/sources/` so the stale-check can cite them.
