---
name: "markdown-research-formatter"
description: Converts any UX research artifact (interview transcripts, synthesis docs, findings decks, workflow diagrams, FigJam boards, Excel/CSV sheets, survey exports, discussion guides, raw notes) into Claude-optimized Markdown with standard YAML front matter and a standardized filename. Source content stays verbatim (sectioned and tagged, never deleted, reworded or anonymised). Images and diagrams are embedded in the .md and transcribed. Use whenever the user wants to prepare, format, clean up, tag, name, or "make Claude-readable" a research artifact, add research to a project or knowledge base, fix front matter, or rename research files, even without the word "markdown", and whenever a research file contains images or diagrams. Project-agnostic: product names, lifecycle stages, personas and workflows come from the project's research-profile.json. Outputs go to the folder named for the run or the user's configured output folder; writes to a shared (SharePoint/OneDrive/Drive) folder need asking first. Optionally suggests related Jira/Confluence links (read-only, user-confirmed).
---

# Research Markdown Formatter

Output: `.md` files with lean front matter (for filtering) and a self-contained body (chunkers may hand Claude one section alone).

**Verbatim rule (all content types).** Source content is never deleted, reworded, summarised in place of the original, reordered, relabelled, cleaned, or anonymised (names, labels, typos, filler, timestamps and numbers stay exactly as in the source). Allowed additions only: front matter, H1, context line, overview, headings with one-line italic summaries, and clearly marked extras (notes, figure blocks). Images and diagrams are never replaced by text alone: each is **embedded** (original image file shown to the viewer) **and transcribed** (every element captured, for chunkers/Claude that only receive text).

## Project profile (what makes this skill project-agnostic)

The skill hard-codes no product, stage, persona or workflow names. They come from the project's `research-profile.json` (fields and example: `references/profile.md`).

1. `python scripts/research_profile.py find <output-folder-or-input-folder>` walks up and finds the nearest profile. `--profile <path>` on any script, or a path the user gives, overrides it.
2. Found → `python scripts/research_profile.py check <path>`; read `products`, `lifecycle`, `personas`, `workflows`, `glossary`, `search_keywords` from it (call this **`<PROFILE>`**). Invalid → show the errors and stop.
3. Not found → ask whether to create one at the project root. Offer a draft built from what the source names (products, roles, stages), show it, and save only after the user confirms. Never classify against values you made up.

## Output locations

**Per-run folder first.** If the user or a calling pipeline names an output folder for this run (e.g. a project's `00-raw/` or `01-clean/`), that folder is **`<LOCAL_OUT>`** for this run. Otherwise use the user's configured folder below.

### First-use setup (configured folder)

This skill is shared, so it has no built-in paths. Each user stores their own locations once in `~/.config/markdown-research-formatter/config.json` (managed by `scripts/config.py`; the file lives outside the skill, so skill updates never overwrite it).

At the start of every run, before anything else:

1. `python scripts/config.py check`. Exit 0 means a writable local folder is configured: read `local_output_dir` (**`<LOCAL_OUT>`**) and, if present, `sharepoint_output_dir` (**`<SP_OUT>`**) from the JSON it prints, and continue.
2. Otherwise this is first use (or the folder is gone/unwritable). Ask the user one short message, then wait:
   - **Local output folder** (required): the absolute path where converted `.md` files and `assets/` should be saved, e.g. `~/Documents/research-md`.
   - **Shared folder** (optional): the absolute path of a SharePoint/OneDrive/Drive-synced folder on their computer where they sometimes want copies placed (stored as `sharepoint_output_dir`). They can skip it and add it later.
3. Save with `python scripts/config.py set --local <path> [--sharepoint <path>]` (creates the local folder if missing; the shared folder must already exist because it is a synced library, and is never created). Confirm the saved paths in one line.
4. If `set` fails (not writable, path missing), tell the user why and ask for another path. Never substitute a location of your own.

Users can change either location any time ("change my output folder", "set my shared folder", `config.py set ...`) and see them with `config.py show`.

### Hard rules

- Write **every** file this skill produces (final `.md`, `assets/` image files, hand-written image/diagram files, plan JSON, `src.txt`, extracted-image work dir, batch tables saved to disk) **only** under `<LOCAL_OUT>/`. Never write to `/mnt/user-data/outputs/`, the working directory, `/tmp`, or any other path. The reason: the user chose one place to find their research files, and stray copies elsewhere are invisible to them.
- **The shared folder (`<SP_OUT>`) is ask-first.** Never write, copy, move, or save anything under `<SP_OUT>` (including subfolders) unless the user has explicitly approved that specific write in the current conversation. Before writing, ask one short question naming the exact destination folder and file(s) and wait for a yes. Approval covers only that request; ask again next time. A repo/knowledge-base/SharePoint mention in the request is not approval. If the answer is no or unclear, keep the files in `<LOCAL_OUT>/`. If no `sharepoint_output_dir` is configured, do not guess one: offer to save one with `config.py set --sharepoint <path>` first.
- Images live in `<LOCAL_OUT>/assets/`, named `<md-filename-stem>_figNN.<ext>` (stem prefix keeps files from different studies from colliding). Copying a `.md` to SharePoint means copying its `assets/<stem>_fig*` files too, into `<SP_OUT>/assets/` (same ask-first rule), so relative links keep working.
- Reading inputs from SharePoint or anywhere else is fine; only writes are restricted.
- If `<LOCAL_OUT>` is not writable in the current environment, stop and tell the user. Do not fall back to another location.

## Workflow

0. Resolve `<LOCAL_OUT>` / `<SP_OUT>` (Output locations) and `<PROFILE>` (Project profile). Then `mkdir -p <LOCAL_OUT>/_work` for scratch files.
1. Read the input (see `file-reading` skill if only a path is given). Pick a `content_type` below.
2. Infer metadata from the content, choosing `product`, `lifecycle`, `personas` and `workflow` from `<PROFILE>`. Ask (one compact message) only if 2+ required fields are unknowable. Uncertain-but-plausible values: fill in, list under "Needs confirmation" in the reply.
2b. **Jira/Confluence links (optional; see section below).** Search, show candidates, wait for the user's answer, and only then continue. Skip silently if the connector is unavailable.
3. Read **only** the matching `references/<type>.md`.
4. **Never retype source text.** Extract it by script: `python scripts/to_text.py <input> src.txt` (xlsx/csv/pptx/docx/pdf/html/text; nothing dropped). Read it with `cat -n`, write a plan JSON (below; scratch `src.txt`/`plan.json` also live under `<LOCAL_OUT>`, in `_work/`), then `python scripts/build_verbatim.py plan.json src.txt <LOCAL_OUT>/ [--profile <path>]`. It copies the source byte for byte and adds only front matter and headings. Only image/diagram transcriptions are written by hand.
4b. **Images (whenever the input has any, or is one).** Run `python scripts/extract_images.py <input> <LOCAL_OUT>/_work/` (add `--render-pages` for charts, SmartArt, native shapes or vector diagrams in pptx/pdf, which are not embedded pictures). It keeps meaningful images and skips icons <48px and exact duplicates, listing both. `view` each kept image, then add one entry per image to the plan's `figures` (format below). A diagram repeated on another slide that carries meaning (not a logo): add another figure reusing the same image path. build_verbatim.py copies each image to `assets/` and embeds it with its transcription.
5. Run `python scripts/validate_md.py <file.md> --source src.txt [--profile <path>]` and fix all errors (the profile is found automatically when the .md sits under the project folder). `--source` proves nothing was altered or deleted; always use it when a source text exists. It also fails on image links that do not resolve, empty alt text, and images with no transcription after them.
6. Present the files and reply in 3-6 lines: full output paths (md + assets/), final names, figures embedded (count) and skipped (count, why), "Needs confirmation" (including any persona/workflow/lifecycle value not yet in the profile, with an offer to add it), anything unconvertible. Always say image content was read visually and needs a spot-check. If SharePoint is the intended final home and `<SP_OUT>` is configured, offer to copy there (ask-first rule above).

Mixed or large input: one file per content type or participant (split at source line boundaries), linked via `related`.

| content_type | reference | inputs |
|---|---|---|
| `transcript` | transcript.md | Zoom/Teams/Fathom/Otter text, VTT/SRT |
| `synthesis` | synthesis.md | findings, readouts, insight docs |
| `workflow-map` | workflow-map.md | flows, journey maps, FigJam/Miro, whiteboard photos |
| `spreadsheet` | spreadsheet.md | Excel/CSV, survey exports, coded data |
| `guide`, `deck`, `notes`, `persona` | other.md | guides/scripts, slides, call notes, personas |

Closest fit only; never invent new values.

## Plan JSON (input to build_verbatim.py)

```json
{"product":"deskly","workflow":["booking-desk"],"content_type":"transcript","qualifier":"s01","version":1,
 "personas":["member"],"lifecycle":["book"],"research_type":"discovery","date":"2026-11-20",
 "description":"≤300 chars","context":"One sentence: product, workflow, stage, research type, what this file is.",
 "overview":"Optional. Speaker key / scope / what is covered.","source_file":"P03.vtt",
 "sections":[{"line":1,"title":"Role and background","summary":"One sentence naming participant/topic."},
             {"line":48,"title":"Late-ETA handling","summary":"…","level":2}]}
```
Optional keys: `customer`, `participants`, `status` (default `raw`), `tags`, `related`, `jira_confluence` (only user-confirmed URLs), `confidentiality`, `notes`, `figures`. `line` = 1-based source line where a section starts (start at a turn/paragraph/slide/row-group boundary). `sections` may be `[]` when the source already has good headings. `level` defaults to 2 (use 3 under `## Discovery`/`## Design feedback` for `both`). The script derives title, filename, H1 and `schema_version`.

`figures` (one per image):
```json
"figures":[{"id":"fig01","image":"_work/images/fig01.png","alt":"One-line description of what the figure shows",
  "title":"Booking flow (slide 3)","after_line":42,"transcription":"Every visible element, in reading order."}]
```
`image` = path from `images.json`. `after_line` = source line after which it appears (a paragraph/slide boundary; `0` = before the source text, for image-only files; for docx, the line holding the `<img>` reference; for pptx, the last line of that slide). `level` optional (defaults to one below the enclosing heading). `title` is a plain label: the script prepends "Figure N:".

## Front matter

Line 1 is `---`. Required: `title, description, product, personas, lifecycle, workflow, research_type, content_type, date`. Optional: `customer`(string, or list if several), `participants`(int), `status`(raw|cleaned|synthesized|final), `source_file`, `related`(filenames), `jira_confluence`(list of Jira/Confluence URLs, user-confirmed only), `tags`(≤6 kebab), `confidentiality`(internal|customer-confidential|public), `schema_version`(1). No other fields; no findings or quotes in front matter.

```yaml
---
title: "Deskly | Booking Desk | Transcript S01 | v1"
description: "Discovery interview with a hybrid-team member on booking desks at peak times, double bookings and workarounds."
product: deskly
personas: [member]
lifecycle: [book]
workflow: [booking-desk]
research_type: discovery
content_type: transcript
date: 2026-11-20
status: raw
schema_version: 1
---
```

- `product`: one key of `<PROFILE>.products` (use the descriptions to classify). None fits: ask; never invent one.
- `lifecycle` (list, primary first; the goal decides): keys of `<PROFILE>.lifecycle`, using the descriptions. None fits: ask; if confirmed, `[multi]`. If the profile has no `lifecycle`, use a short kebab-case stage and flag it.
- `research_type`: `discovery` (current behavior/needs, "walk me through today") | `design-feedback` (reactions to designs/prototypes/usability) | `both`.
- `workflow`: kebab-case `verb-ing + object`, 2-3 words (max 4, ~25 chars), primary first, e.g. `booking-desk`, `approving-request`. Reuse `<PROFILE>.workflows` or the user's list verbatim; new name → flag it and offer to add it to the profile.
- `personas`: kebab-case roles as the organization names them (prefer `<PROFILE>.personas`); the role acted in the study. Inferred or not in the profile → say so.
- `customer`: only when the research is tied to a particular customer (e.g. a session with one customer's users, a customer-specific study, a customer's data). Use the name exactly as it appears in the source or as the user gave it; several customers → inline list `[a, b]`. If the research is general (not tied to a customer), **omit the field entirely**; never write `none`, `n/a`, or a blank. Unclear whether it's customer-specific → omit and list under "Needs confirmation". Goes right after `date` in the front matter (the script does this). Not part of the filename or title.
- `jira_confluence`: inline list of Jira ticket and/or Confluence page URLs related to this research, e.g. `["https://acme.atlassian.net/browse/IT-482", "https://acme.atlassian.net/wiki/spaces/UX/pages/123456/Desk-Booking"]`. Only entries the user confirmed (see "Jira/Confluence links"). No confirmed entries → **omit the field entirely**; never write `[]`, `none`, titles, statuses, or guessed links. Sits right after `related` (the script does this). Not part of the filename or title.
- `date`: ISO session/study date (synthesis: finalized), not today. Only recorded here.
- `description`: ≤300 chars, 1-2 sentences, what it contains and which questions it answers.
- Quote strings containing `: # | [ ]`; inline lists `[a, b]`; spaces only.

## Jira/Confluence links (optional field `jira_confluence`)

Goal: connect the research file to the Jira tickets and Confluence pages it relates to, **never without the user's confirmation**.

1. **Tools.** Use the Atlassian connector (if its tools are deferred, `tool_search` "Atlassian"). All calls are **read-only**: never create, edit, comment on, or transition anything. If the connector is missing, unauthorised, or errors, skip this step, do not block the conversion, and add one line to the final reply ("Jira/Confluence not searched: <reason>"). If the user said to skip Jira/Confluence, skip silently. If the user already gave ticket/page links, treat them as confirmed (no search needed).
2. **Search (lean, after metadata is inferred).** Build keywords from `<PROFILE>.search_keywords`, the product, workflow words, customer (if any), study or source title. Use no participant names, quotes, or other source text in queries. Start with one semantic `search` (`targetApp` ALL, default limit; get `cloudId` from `getAccessibleAtlassianResources`). Only if results are thin, add one JQL `text ~` search and one CQL `text ~` search. Judge from titles/snippets/status; do not fetch full bodies (at most one summary read to disambiguate).
3. **Shortlist** at most 5 items total, best first, dropping weak matches (do not pad). Same-product-and-workflow plus matching customer or time frame ranks highest.
4. **Ask once, then wait** (batch: one table covering all files). Per item: number, Jira/Confluence, key or page title, status or space, full URL, ≤10 words on why it matches. End with: "Add any of these to `jira_confluence`? Reply with numbers, 'all', or 'none'." Nothing is written to the file before the answer. Zero candidates → say so in one line in the final reply and omit the field.
5. **Write only what was confirmed**, as the full URLs returned by the tools (Jira: `https://<site>/browse/KEY-123`), in the plan's `jira_confluence` list. 'none' or no answer → omit the field. Never add a ticket/page from memory or inference.
6. Metadata only: nothing from the tickets/pages goes into the body (verbatim rule). Revisions (`vN+1`) carry over previously confirmed links and do not re-ask unless the user wants a refresh.

## Naming

File: `product_workflow_content-type[-qualifier]_vN.md` (lowercase, 4 underscore segments, ≲50 chars), e.g. `deskly_booking-desk_transcript-s01_v1.md`.
Title: `Product | Workflow | Content Type [QUALIFIER] | vN`. H1 = title minus `| vN`. Qualifier optional (`s01`, `p03`, `round2`, `survey`). Revisions bump `vN`; never overwrite. Multiple studies on one workflow: add a distinguishing qualifier.

## Body rules

1. H1, then an italic context line naming product, workflow, stage, research type, and what the file is (the script writes both).
2. Strict heading order (no skipped levels). Inserted headings name the workflow/participant so each section stands alone ("as above" is banned); aim for ≲700 words per section, splitting at source boundaries.
3. Images/diagrams: always a figure block = heading, `![alt](assets/<stem>_figNN.<ext>)`, then `**Transcription:**` covering every visible element (nodes, labels, arrows with direction, swimlanes, stickies, legends, chart axes/values/titles). Relative paths only; alt text is a real one-line description; never write "see diagram" or link without transcribing. Unreadable parts: `[illegible: <where>]`, never guessed.
4. Participants, speaker labels, names and quotes stay exactly as in the source. No anonymisation.
5. Consistent product names (canonical spellings from `<PROFILE>.glossary`) only in text you add; the source is never normalised.
6. Add nothing absent from the source. Inferences are marked `(inferred)` and flagged in the reply.

## Edge cases

- `both`: `## Discovery` and `## Design feedback` H2s.
- Source front matter: keep it as source text; the schema front matter goes above it.
- Customer-confidential data: `confidentiality: internal` (or stricter), set `customer` if a specific customer is identifiable, and say so; never strip needed information silently.
- Batch: table of old → new names plus confirmation items.
