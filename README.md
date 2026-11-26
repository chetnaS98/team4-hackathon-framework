# team4-hackathon-framework

Koru 3.0 Design Ops hackathon: an AI-DLC-style delivery framework (Frame → Explore → Harden → Ship),
built as Claude Code skills plus small deterministic scripts. People review before anything becomes context.

## What's here

| Path | What it is |
|---|---|
| `.claude/skills/markdown-research-formatter/` | Skill: any research file → Claude-readable Markdown, word for word. Project-agnostic via `research-profile.json`. |
| `.claude/skills/frame-clean-synthesise/` | Skill: Frame step 1. Cleans a project's transcripts, then builds the checked `synthesis.json`. |
| `plugins/koru/` | The **koru** Claude Code plugin: the whole playbook (Frame, Explore, Harden, Ship) behind one command, `/koru:next`. See [plugins/koru/README.md](plugins/koru/README.md). |
| `.claude-plugin/marketplace.json` | Makes this repo a plugin marketplace (`team4-koru`) so teammates can install koru. |
| `ONBOARDING.md` | Teammate guide to the koru plugin: install, first engagement, who checks what. |
| `framework/` | Pipeline scripts and docs. Start with [framework/README.md](framework/README.md). |
| `examples/deskly/` | Made-up test project (no real people or clients). |

## Site map

```mermaid
flowchart TD
  repo["<b>team4-hackathon-framework</b>"]
  repo --> mkt[".claude-plugin/<br/>marketplace.json<br/><i>marketplace team4-koru</i>"]
  repo --> onb["ONBOARDING.md<br/><i>teammate guide</i>"]
  repo --> rs[".claude/skills/<br/>research formatter<br/>frame-clean-synthesise"]
  repo --> plug["<b>plugins/koru/</b><br/>the koru plugin v0.1.0"]

  plug --> cmd["<b>commands/</b><br/>/koru:next<br/>/koru:status<br/>/koru:break<br/>/koru:change"]
  plug --> ag["<b>agents/</b><br/>evidence-auditor<br/>feasibility-engineer<br/>hardening-critic<br/>handoff-reviewer"]
  plug --> hk["<b>hooks/</b><br/>guard: PreToolUse<br/>session_start: SessionStart<br/>agent_done: Pre/PostToolUse"]
  plug --> sc["<b>scripts/</b><br/>route · intake · step<br/>signoff · advance_stage<br/>iteration · log"]
  plug --> sk["<b>skills/</b>"]

  sk --> core["<b>koru-core</b><br/>rules · naming · logs<br/>registers · roles gate<br/>stale-check · lints"]
  sk --> fr["<b>1 · koru-frame</b><br/>24 steps<br/>framed brief<br/>research pack"]
  sk --> exp["<b>2 · koru-explore</b><br/>18 steps<br/>two ideas<br/>Design v1"]
  sk --> hd["<b>3 · koru-harden</b><br/>H1 to H19<br/>states · roles · a11y<br/>tokens · rulebook"]
  sk --> sh["<b>4 · koru-ship</b><br/>S1 to S9 (+ S3b)<br/>HTML + walkthrough<br/>React starter · tickets"]
```

The numbers are the order the stages hand on. Every stage skill loads `koru-core` first. The file-by-file tree is in [plugins/koru/README.md](plugins/koru/README.md#site-map).

### Technical specifications

| | |
|---|---|
| **Runs in** | Claude Code (CLI, desktop app or IDE), as a plugin installed from this repo's marketplace (`team4-koru`) |
| **Scripts** | Python 3.9+, standard library only: nothing to install for the plugin |
| **Hooks** | `guard.py` on PreToolUse `Write\|Edit\|MultiEdit`; `agent_done.py` on Pre and PostToolUse `Agent\|Task`; `session_start.py` on SessionStart |
| **Agents** | 4 reviewers with their own fresh context; read-only (`Read, Grep, Glob`) plus `Write` for their own report only |
| **Files** | Markdown with YAML front matter; named `[project]-[stage]-[artefact]-v[n]-[draft\|review\|final]`; a final is never overwritten |
| **State** | `00-read-me-first.md` (roles, stage table, step trackers) and `.koru/` (`project.json`, `stages.json`, `types.json`, `progress.json`) |
| **Gates** | Roles gate before any step; a pass needs a named checker who didn't run the step; stale-check before any final; handoff needs every step passed or skipped, finals only, a signed card |
| **Ship outputs** | One self-contained HTML deliverable with an Intro.js 7.2.0 tour (cdnjs, the only external script); optional React starter (Vite 5.4, React 18.3, TypeScript 5.6, pinned); tickets as Jira-import `tickets.csv` and `tickets.md` |
| **Data** | No client data in git: keep engagement folders out of shared branches; only made-up data is committed |

## The koru plugin (the full playbook)

The plugin runs a whole engagement through **Frame → Explore → Harden → Ship**. Claude drafts; a named person checks every AI step; only signed-off files become project knowledge. Install it once in Claude Code, from this repo:

```
/plugin marketplace add ./
/plugin install koru@team4-koru
```

Restart Claude Code, then type `/koru:next`. The first time it asks the intake questions and the names of the people in each role; after that it runs the next step, stops wherever a person has to check or decide, and hands a finished stage on to the next. `/koru:status` shows where things stand without changing anything.

| Stage | Hands on | People decide |
|---|---|---|
| Frame | One-page framed brief, reviewed research pack | Senior signs the brief, research owner the pack |
| Explore | Directions, two ideas with wireframes, concept tests, Design v1 | Designer decides at 3 checkpoints; team lead signs off |
| Harden | Every state, role, edge case, AI state and accessibility check; engineer feasibility; tokens; rulebook checks | Engineer answers feasibility; design lead decides fixes vs Ship notes |
| Ship | Clickable HTML deliverable with an Intro.js walkthrough, an optional React starter, 3 to 5 tickets (Jira CSV and markdown), handoff note | Stories agreed, walkthrough tested by a new user, engineer signs; each round to the build team is a new handoff version |

Skills hold the judgement, scripts enforce the rules the same way every time (named checker, stale-check, handoff gates), hooks block unsafe edits, and four reviewer agents give an independent read. Details in [plugins/koru/README.md](plugins/koru/README.md) and [ONBOARDING.md](ONBOARDING.md).

## Set up the Frame pipeline (once per teammate)

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
