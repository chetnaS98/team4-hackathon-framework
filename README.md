# team4-hackathon-framework

Koru 3.0 Design Ops hackathon: an AI-DLC-style delivery framework (Frame → Explore → Harden → Ship),
built as Claude Code skills plus small deterministic scripts. People review before anything becomes context.

- `.claude/skills/markdown-research-formatter/`: turns any research file into Claude-readable Markdown, word for word. Project-agnostic via `research-profile.json`.
- `framework/`: the Frame intent pipeline (transcripts → synthesis → ledger → TRACES audit). Start with [framework/README.md](framework/README.md).
- `examples/deskly/`: made-up test project.

Setup: `pip3 install -r requirements.txt` (Python 3.9+).
