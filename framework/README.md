# Frame intent pipeline

Automates part of Koru's **Frame** stage (AI-DLC *Inception*): turn raw call transcripts into a
checked, well-framed brief with proof it is ready for Explore.

```
00-raw/  transcripts + manifest.json          (people)
   │
   ▼  [1a] markdown-research-formatter skill  (AI: sections + tags; script: word-for-word check)
01-clean/  one .md per session
   │
   ▼  [1b] frame_build_synthesis.py build     (script only, no AI)
02-synthesis/  <project>-frame-synthesis-vN-draft.json   ── contract check ──┐
   │                                                                          │ fail → break-log.md, stop
   ▼  [2] frame-classify-evidence            (next to build)                  │
03-ledger/                                                ── contract check ──┘
   │
   ▼  [3] frame-audit-traces                 (to build)
04-audit/  audit.json, gap-report.md, open-questions.md
   │
   ▼  Human gate: research owner, 30 min → promote to final → decisions-log.md
```

## Rules every step follows

- All outputs are `draft`. Only a named person promotes a file to `final`; only `final` files go into project knowledge.
- Steps hand over through files, never conversation. A failed contract writes `break-log.md` and stops; the next step never guesses.
- Artefact names: `[project]-[stage]-[artefact]-v[n]-[status]`. A draft is overwritten on re-run; if the latest version is in `review` or `final`, a new version starts. A `final` file is never touched.
- Made-up data only in tests and examples.

## Project folder

```
<project>/
  research-profile.json       products, stages, personas, workflows (see the formatter skill's references/profile.md)
  frame/
    00-raw/manifest.json      one entry per session (schema below)
    00-raw/<transcripts>
    01-clean/                 formatter output (+ _work/ plans)
    02-synthesis/  03-ledger/  04-audit/
    break-log.md  decisions-log.md
```

## Step 1: clean, then build synthesis.json

1. **Clean** each transcript with the `markdown-research-formatter` skill, output folder `frame/01-clean/`.
   It keeps every source line word for word and adds front matter and topic sections.
2. **Index** the cleaned sessions:

   ```bash
   python3 framework/scripts/frame_build_synthesis.py build <project>/frame
   ```

   It checks, and stops with a break-log entry if any fail:
   - the manifest: unique session IDs, a role per session, valid date, `call_type` and `path`, files that exist;
   - the profile: same project as the manifest;
   - every session has a cleaned file (matched by `source_file`, or `clean_path` in the manifest);
   - every cleaned file passes the formatter's validator, including the word-for-word check against the raw transcript.

   It writes `02-synthesis/<project>-frame-synthesis-vN-draft.json`: per session, the manifest facts,
   the cleaned file, the sections the formatter marked (line ranges in the cleaned file), speakers, and
   whether to cite by `timestamp` or `line`; plus the fixed category lists (TRACES letters, layers,
   cohorts, roles) the classify step must use. It holds no findings: interpretation starts at step 2.
3. **Contract check before step 2** (the orchestrator runs this; you can too):

   ```bash
   python3 framework/scripts/frame_build_synthesis.py check <project>/frame/02-synthesis/<file>.json
   ```

### manifest.json

| Field | Required | Values |
|---|---|---|
| `project` | yes | kebab-case, same as the profile |
| `sessions[].session_id` | yes | unique, letters/digits/hyphens (`S01`) |
| `sessions[].date` | yes | `YYYY-MM-DD` |
| `sessions[].call_type` | yes | `fresh_start`, `informed`, `ad_hoc` |
| `sessions[].participant_role` | yes | a profile persona |
| `sessions[].transcript_path` | yes | relative to `frame/` |
| `sessions[].path` | no | `roadmap_hypothesis`, `discovery_question`, null |
| `sessions[].cohort`, `moderator`, `note_taker`, `guide_reviewed_by` | no | text or null |
| `sessions[].sorted_before_call`, `is_proxy`, `screener_used` | no | true, false or null |
| `sessions[].discussion_guide`, `clean_path` | no | path relative to `frame/`, or null |
| `artefacts.heuristic_evaluation`, `accessibility_check`, `competitive_scan`, `secondary_research` | no | path or null |

## Example

`examples/deskly/` is a complete made-up project with three sessions, one per call scenario, with
gaps planted for later steps to find: no one mentions decision rights or dates (TRACES **S** is empty),
and S03 is a proxy making a single-source claim about the mobile app.

```bash
pip3 install -r requirements.txt
python3 framework/scripts/frame_build_synthesis.py build examples/deskly/frame
```
