---
name: frame-clean-synthesise
description: Frame stage, step 1 of the intent pipeline. Cleans a project's call transcripts with markdown-research-formatter, then builds the checked synthesis.json index that the classify step needs. Use when someone wants to start or re-run Frame on a folder of transcripts, "prepare sessions for the ledger", "run step 1", "build synthesis.json", or check whether a project's sessions are ready for classification. Writes drafts only; never promotes anything to final or into project knowledge.
---

# Frame step 1: clean and synthesise

Turns `<project>/frame/00-raw/` (transcripts + `manifest.json`) into
`<project>/frame/02-synthesis/<project>-frame-synthesis-vN-draft.json`, checked and ready for
`frame-classify-evidence`. Pipeline overview, folder layout and manifest fields: `framework/README.md`.

**What AI does here:** marks topic sections and fills front matter in the cleaned files (via the formatter).
**What scripts do:** every check and the synthesis.json itself (no AI, same input → same output).
**Who checks:** the research owner, at the human gate after step 3. Everything here stays `draft`.

Run all commands from the repo root (`git rev-parse --show-toplevel`).

## 0. Setup check

`python3 -c "import yaml"`. If it fails, tell the user to run `pip3 install -r requirements.txt` and stop.

## 1. Find the project

- Ask for the project folder if not given (e.g. `projects/deskly`, or `examples/deskly` to try it out).
- Profile: `python3 .claude/skills/markdown-research-formatter/scripts/research_profile.py find <project>/frame`.
  None → follow the formatter skill's "Project profile" section (draft it, show it, save only on a yes).
- Manifest: `<project>/frame/00-raw/manifest.json`. Missing → offer to draft one from the transcripts in
  `00-raw/` using the fields in `framework/README.md`. Fields a transcript cannot tell you (moderator,
  note-taker, screener, whether the call was sorted beforehand, proxy status) are left `null` and listed
  for the user to fill. Show the draft; save only after the user confirms. The manifest is a human record.
- **Client data check:** if the folder is under `examples/` or a test run, it must hold made-up data only.

## 2. Clean every session that needs it

For each manifest session, it needs cleaning if no `.md` in `<project>/frame/01-clean/` has front matter
`source_file` equal to the transcript's file name (or the manifest's `clean_path` is missing).

Clean it with the **markdown-research-formatter** skill, following that skill fully, with:
- output folder for this run = `<project>/frame/01-clean/` (scratch in `01-clean/_work/`);
- `qualifier` = the session ID in lowercase (`s01`), `source_file` = the transcript's file name;
- `personas` includes the manifest's `participant_role`; `date` = the manifest date;
- skip the Jira/Confluence step unless the user asks for it.

Never edit anything in `00-raw/`. Already-cleaned sessions are not re-cleaned unless the user asks
(then bump the version: `_v2`).

## 3. Build synthesis.json

```bash
python3 framework/scripts/frame_build_synthesis.py build <project>/frame
```

- **Exit 0:** note the file path and any `warn:` lines.
- **Exit 1 (STOPPED):** the cause is in the output and in `<project>/frame/break-log.md`. Do not work around it.
  - A cleaned file fails (e.g. not word for word): re-clean that session in step 2, then re-run.
  - Manifest or transcript problem (missing role, duplicate ID, missing file, wrong project): show the
    user the exact problem and ask them to fix it, or propose the exact edit and apply it only on a yes.
  - Never hand-edit synthesis.json or skip a check to make it pass.

## 4. Contract check for step 2

```bash
python3 framework/scripts/frame_build_synthesis.py check <project>/frame/02-synthesis/<file>.json
```

Must print `OK`. If not, treat it like a STOPPED build.

## 5. Reply (5–8 lines)

- The synthesis file path, number of sessions, by role and by call type, proxies.
- Sessions cleaned in this run (paths) and that section titles were AI-chosen and worth a skim.
- Every warning, in plain words.
- "All outputs are drafts; nothing was added to project knowledge."
- Next: `frame-classify-evidence` on this synthesis file.
