# File protocol: naming, status, front matter, traceable lines, where things live

## Contents
- Naming
- Status lifecycle
- Front matter schema
- Registering types per phase
- Traceable lines and pointers
- Confidence levels
- Where things live

## Naming

`[project]-[stage]-[artefact]-v[number]-[status]`, lowercase, hyphens inside segments. Examples: `deskly-frame-brief-v1-draft`, `deskly-frame-insight-clashes-v1-final`, `deskly-explore-direction-card-1-v2-review`.

- `project`: a code name with letters and digits only, never the client's real name.
- `stage`: `frame`, `explore`, `harden` or `ship`.
- `artefact`: the type, then an optional topic (`insight-clashes`).
- `number`: the version. A new version bumps it; a status change does not.
- `status`: `draft`, `review` or `final`.

Source files in the knowledge base (Layer 1, raw material) use the formatter skill's own naming and are outside this protocol.

## Status lifecycle

| Status | Meaning |
|---|---|
| `draft` | AI output nobody has reviewed |
| `review` | Being discussed or checked |
| `final` | Signed off by the named person (see the sign-off matrix). Only now may it enter project knowledge |

Never overwrite a `final` artefact. Make the next version and mark the old one as replaced in the decisions log. When status changes, the file name suffix and the front matter `status` both change, and they must agree (`lint_core.py` checks this). Superseded drafts move to a `superseded/` folder next to the draft.

## Front matter schema

Every derived artefact starts with this front matter:

```yaml
---
title: "Deskly | Frame | Persona Member | v1"
description: "One or two sentences saying exactly what the artefact is and what it covers."
type: persona          # one of the types registered for the stage
stage: frame           # frame | explore | harden | ship
status: draft          # draft | review | final
version: 1
last_checked: 2026-11-25
owner: name
derives_from: [deskly-frame-insight-clashes-v1, deskly-frame-workflow-booking-v1]   # optional; artefact or source names ending in the version, no status
external_url: https://...   # optional; where the artefact lives if it is not a file (Figma, Jira, GitHub, HTML)
---
```

- `title`: `Project | Stage | Type Topic | vN`.
- `derives_from`: the artefacts this one is built from, named with their version and no status suffix. This is what the stale-check follows across stages: a new brief version flags the direction cards built on it, a changed direction flags hardening, a changed design flags tickets. List it even when every assertion also carries a `src:` pointer.
- `external_url`: for an artefact whose real home is not a file (a Figma frame, a Jira ticket, an HTML page). The file then holds the description and registry data, and the registry row carries the link.
- The `stage` field is new in core. Older files without it are treated as the stage in their file name, with a warning.
- Do not add other fields without registering them here.

### HTML artefacts

Some artefacts are HTML files (wireframes, mocks, a page). They follow the same naming and carry the same front matter, placed inside a leading HTML comment so the page still renders:

```html
<!--
---
title: "Deskly | Explore | Wireframe Idea A | v1"
description: "..."
type: wireframe
stage: explore
status: draft
version: 1
last_checked: 2026-11-25
owner: name
derives_from: [deskly-explore-direction-final-v1, figma:aB3dEf/12:34@v2]
---
-->
<!doctype html>
```

`lint_core.py`, `build_registry.py` and `stale_check.py` read this form. HTML that lives in a `sources/` folder is a source, not an artefact, and needs no front matter.

## Registering types per phase

The type enum is not global. Each phase skill declares the types it creates in its `stage.json`, and `scripts/init_stage.py` merges them into the engagement's `.koru/types.json`. `lint_core.py` accepts a type only if it is registered for the file's stage. Frame registers: insight, persona, workflow, jtbd, opportunity, competitive-scan, research-pack, brief. Explore's proposed types are in `stages.md` (direction, journey, wireframe, rationale, add-ons, insight-decisions, design). Another phase registers its own (for example a hardening checklist, a rulebook entry, a ticket, a handoff note) when its skill is built, in the same change that adds the template. A phase may also supply a sample `stage.json` (see `registry/stage-examples/`).

## Traceable lines and pointers

Every assertion in a derived artefact is one line:

```
- Monday room clashes are frequent. [medium] src: deskly_booking_transcript-ops-lead_v1 §Call notes
- Members would accept a suggested room. [low] (inferred) src: none
```

Shape: `- <assertion>. [high|medium|low] (observed|data)? (inferred)? src: <pointer>[; <pointer>]`, or `src: none`.

One assertion per line. Several sources are separated by `; `. An assertion with no source is not a finding: it moves to the assumptions register (`src: none`).

**Pointer forms**

| Source | Form | Example |
|---|---|---|
| A file | `<artefact-or-source-name> §<section heading>` | `deskly-frame-insight-clashes-v1 §Insight` |
| A Figma frame | `figma:<fileKey>/<nodeId>` | `figma:aB3dEf/12:34` |
| A Jira ticket | `jira:<KEY-123>` | `jira:DSK-482` |
| A GitHub item | `github:<owner>/<repo>#<number>` | `github:koru/deskly#57` |
| A web page or other URL | `url:<https://...>` | `url:https://example.com/spec` |

For a non-file pointer, add `@v<N>` to pin a version when the source has one (`jira:DSK-482@v2`). The stale-check resolves non-file pointers through the artefact registry (its `Pointer` column). A pointer to a source that is not in the registry is reported as unregistered, because it cannot be stale-checked.

## Confidence levels

| Level | Meaning |
|---|---|
| **High** | Two or more independent sources, or direct observation or data (tag `(observed)` or `(data)` when one source is enough) |
| **Medium** | One reliable source, such as a single call, or a single review |
| **Low** | An anecdote, a passing mention, or an AI inference (marked `(inferred)`) |

Two files from the same interview or the same author count as one source. A phase skill may refine what counts as independent for its own evidence (for example test sessions in Explore) but may not loosen this rubric.

## Where things live

| Artefact | Home | Notes |
|---|---|---|
| Source material (transcripts, reports, decks) | Knowledge base (cloud storage) | Names kept; restricted to the team |
| Drafts and artefacts in review | Shared output folder | One folder per stage |
| Final research, briefs and other final text artefacts | Claude project knowledge | Only `final` |
| Logs, registers, read-me | Claude project knowledge | One of each per project |
| Designs (frames, prototypes) | Figma | Registry row carries the link; file in project holds the description |
| Code and rulebook content | GitHub | As the phase skill defines |
| Tickets | Jira | As the phase skill defines |

Each phase skill adds its own artefact rows to this map in its `stage.json`/references. Frame's rows are in its own skill. The Figma, Jira and GitHub homes are proposed defaults (`defaults.md`) until the team confirms them; the final-status markers for those homes are confirmed (`integrity.md`).
