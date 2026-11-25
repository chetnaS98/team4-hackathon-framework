# team4-hackathon-framework

Koru 3.0 Design Ops hackathon: an AI-DLC-style delivery framework (Frame → Explore → Harden → Ship),
built as Claude Code skills plus small deterministic scripts. People review before anything becomes context.

## What's here

| Path | What it is |
|---|---|
| `.claude/skills/markdown-research-formatter/` | Skill: any research file → Claude-readable Markdown, word for word. Project-agnostic via `research-profile.json`. |
| `.claude/skills/frame-clean-synthesise/` | Skill: Frame step 1. Cleans a project's transcripts, then builds the checked `synthesis.json`. |
| `framework/` | Pipeline scripts and docs. Start with [framework/README.md](framework/README.md). |
| `examples/deskly/` | Made-up test project (no real people or clients). |

## Set up (once per teammate)

1. Clone the repo and open the folder in Claude Code (desktop app or `claude` in a terminal).
   Skills in `.claude/skills/` load automatically for anyone working in this folder; nothing to install.
2. Install the one Python dependency (Python 3.9+):
   ```bash
   pip3 install -r requirements.txt
   ```
3. Try it on the example: ask Claude *"run frame step 1 on examples/deskly"*, or run the script directly:
   ```bash
   python3 framework/scripts/frame_build_synthesis.py build examples/deskly/frame
   ```

## Use it on a real project

1. Make `projects/<project>/research-profile.json` (Claude will draft one with you on first run).
2. Put transcripts in `projects/<project>/frame/00-raw/` with a `manifest.json` (fields in [framework/README.md](framework/README.md)).
3. Ask Claude to run Frame step 1 on `projects/<project>`.

Client transcripts are confidential: keep real projects out of shared branches unless the team has agreed where they live.
