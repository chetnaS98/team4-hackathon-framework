# Engagement scaffolding

## Contents
- Folder layout and reserved numbers
- The read-me (engagement-wide)
- The decisions log
- The AI quality log
- The handoff card shell
- The init scripts

## Folder layout and reserved numbers

One folder per project, not per stage. Final artefacts that belong in Claude project knowledge sit under numbered folders at the root; each stage keeps its own working area.

```
<project>/
  00-read-me-first.md        engagement-wide: project, roles, stage table, each active stage's step tracker
  01-framed-brief/           Frame finals: the brief
  02-research/               Frame finals: pack, insights, personas, workflows, JTBD, scan, opportunities
  03-rulebook/               RESERVED for Harden (the rulebook)
  04-design-library/         RESERVED for Harden (the design library)
  05-decisions-log.md        one log per project
  06-explore/                Explore finals (Proposed assignment; see stages.md)
  07-...                     unassigned: a phase skill claims the next free number for its own finals
  ai-quality-log.md          one log per project
  assumptions-register.md    one register per project
  open-questions-register.md one register per project
  artefact-registry.md       index of every artefact
  handoff-cards/             one card per stage handoff
  stages/
    frame/    drafts/ sources/ templates/
    explore/  drafts/ templates/
    harden/   drafts/ templates/
    ship/     drafts/ templates/
  .koru/                     project.json, stages.json, types.json (written by the init scripts)
```

Frame's numbering skips 03 and 04 because they belong to the rulebook and the design library in Harden. Core reserves them; no other phase may use them. A phase that needs a final-folder number takes the next free one (06 is proposed for Explore) and records it in its `stage.json` and in this list.

`drafts/` below means `stages/<stage>/drafts/`. The older Frame-only layout (`<project>-frame/` with `drafts/` and `sources/` at the root) still works with the scripts; new engagements use the layout above.

## The read-me (engagement-wide)

`00-read-me-first.md` describes the whole engagement, not one stage. It holds: what the project is, the client alias used in derived artefacts, the start date, engagement size (small or large, with the date it was set), the knowledge base location, the **design system** path (with DS and its link, or without DS and the internal wireframes DS link, or not decided; read by Explore and Harden), the **roles table** (every role in the registry, named or blank), the client's decision makers and review rhythm, a **stage table** (stage, skill, status, lead, handoff card), where everything lives, and the stale-check owner and last run.

Each phase skill appends its own **step tracker** under a heading `## <Stage> step tracker` when `init_stage.py` runs. The tracker has one row per step: step, status (not started, drafted, in check, passed, skipped with reason), checker, date. Update it at the end of every step. The tracker is how a later session resumes.

## The decisions log

One log per project (`05-decisions-log.md`). One line per decision:

| Date | Stage | Decision | Artefact affected | Made by | Alternative considered |
|---|---|---|---|---|---|

It records every sign-off, client confirmation, path or scope choice, size setting, new version of a key artefact, replaced `final` artefact, send-back, default accepted, and any time a stale-check warning is overridden (an override needs a named person and a reason). `Artefact affected` is the artefact name (or `-` if none). `Stage` is `core` for project-wide decisions.

## The AI quality log

One log per project (`ai-quality-log.md`). One line per mistake caught, with a category so patterns across stages show instead of anecdotes:

| Date | Stage | Step | Category | What the AI got wrong | How it was caught | Caught by | Fix |
|---|---|---|---|---|---|---|---|

**Categories** (use one): `fabricated` (invented content), `misattributed` (right fact, wrong source or speaker), `overconfident` (stated more strongly than the evidence), `missed` (left out something that was in the input), `ignored-instruction` (did not follow a rule or request), `format` (naming, front matter, structure). If a mistake fits two, pick the one that explains the root cause and note the other in the text.

## The handoff card shell

One card per stage handoff, stored in `handoff-cards/`, checked by the next stage's team. The shell is fixed; each phase fills its own two lines.

| Field | What goes in |
|---|---|
| What we hand on | The artefacts, all `final` |
| Format and template | The template and file format used |
| Where it lives and what it's called | The home and the exact names |
| What the next stage must be able to do with it | **Phase fills this in** |
| What it doesn't include | **Phase fills this in** |
| Who signs it off | Names, per the sign-off matrix |
| Checked by the next stage (name) | To fill by the next stage |
| Stale-check result | No open warnings on any artefact in the handoff, with the date |
| Assertion confidence | The count of high, medium and low lines across the handed-on artefacts |
| Open assumptions and open questions handed on | Counts and the ids that block the next stage |

The last row is core's addition so the registers travel with the handoff.

## The init scripts

- `scripts/init_engagement.py` runs once per project. It creates the root layout, the read-me with the roles and stage tables, the two logs, the three registers, `handoff-cards/` and `.koru/`.
- `scripts/init_stage.py` runs once per phase. It reads the phase skill's `stage.json`, creates `stages/<stage>/`, its draft and final folders, copies the phase templates, appends the step tracker to the read-me, marks the stage active in the stage table, and merges the phase's types and required roles into `.koru/`.

Both refuse to overwrite. Roles must be named (the roles gate passes for the stage) before the first step of a stage runs.
