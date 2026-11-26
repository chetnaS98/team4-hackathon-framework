# The phase skill contract

What a phase skill (Frame, Explore, Harden, Ship) must provide, and what it must leave to core. Use this when building a new phase skill or changing an existing one.

## Contents
- A phase skill starts by loading core
- What a phase skill provides
- stage.json
- What a phase skill must not do
- Starting a stage
- Checklist for a new phase skill

## A phase skill starts by loading core

The first instruction in a phase skill's `SKILL.md` is to load `koru-core` (its `SKILL.md`, which holds the rules, the step loop and the session protocol), then to read the core references the moment they are needed. The phase skill states the core version it expects. A phase skill's description should say it works together with koru-core.

## What a phase skill provides

- **Steps.** Numbered, each with a mode (AI-led, AI-assisted, human-led), what AI does, what people do, who checks, the output, and an exit test. The step loop itself is core's. If the phase has checkpoints, mark them (core's rule: hard stop, logged, not the second-person check). Call internal blocks "parts", never "stages".
- **Artefact types and templates.** Each type has a template with the core front matter, and is registered in `stage.json`.
- **Required roles.** The roles from `registry/roles.json` that the phase needs, so the roles gate can enforce them.
- **Sign-off rows.** Its rows for core's sign-off matrix, and a re-confirmation trigger for anything the client confirms. Added to `koru-core/references/governance.md` when the phase is built.
- **Handoff lines.** The two lines core's handoff card leaves to the phase: "what the next stage must be able to do with it" and "what it doesn't include".
- **A defaults section** in `koru-core/references/defaults.md`, including any size thresholds that differ from core's.
- **Its own list of third-party skills**, with the principle that none overrides core rules.
- **Phase-only checks** (for example Frame's assertion lint) that run after core's lint.
- **Phase-specific rules** that do not apply elsewhere (for example "read every request source in full"). These are added to the phase skill, not to core.

## stage.json

Read by `scripts/init_stage.py`. Fields:

```json
{
  "stage": "frame",
  "title": "Frame",
  "number": 1,
  "skill": "koru-frame",
  "core_version": 1,
  "types": ["insight", "persona", "workflow", "jtbd", "opportunity", "competitive-scan", "research-pack", "brief"],
  "required_roles": ["Researcher", "Research owner", "Senior", "Developer", "Second-person checker"],
  "draft_folders": ["stage-intake", "stage-research", "stage-define", "stage-opportunity", "stage-brief"],
  "final_folders": ["01-framed-brief", "02-research"],
  "source_folder": true,
  "templates_dir": "assets/templates",
  "step_tracker": "assets/stage/step-tracker.md",
  "handoff": {
    "must_be_able_to_do": "...",
    "does_not_include": "..."
  }
}
```

`final_folders` take numbers from core's reserved list (01 and 02 are Frame's; 03 and 04 are reserved for Harden; a new phase takes the next free number from 06 and says so here and in `engagement.md`).

## What a phase skill must not do

- Restate the never-bend rules, the step loop, the session protocol, the naming or status rules, the log formats, the registers or the stale-check. Link to them.
- Keep its own decisions log, AI quality log, defaults file or roles list. There is one of each per project.
- Define a different confidence rubric, naming pattern or status lifecycle.
- Ask the client to confirm an artefact before its sign-off row and re-confirmation trigger exist in core's governance.
- Write into another phase's folders, or change another phase's artefacts. Use the send-back protocol.

## Starting a stage

```bash
python koru-core/scripts/init_stage.py --engagement <project> --stage-dir <path to the phase skill>
```

It reads `stage.json`, creates the stage's folders, copies its templates (with project and date filled in), appends its step tracker to the read-me, marks the stage active in the stage table, and registers its types and roles. Then run the roles gate. The first step of the stage does not begin until the gate passes.

## Checklist for a new phase skill

1. `SKILL.md` loads koru-core first and states the core version.
2. `stage.json` is complete and its types have templates.
3. Required roles are declared; any new role is added to `registry/roles.json`.
4. Sign-off rows and re-confirmation triggers are added to core governance.
5. A defaults section is added to core defaults.
6. Handoff lines are defined.
7. Phase-only checks exist and run after `lint_core.py`.
8. Nothing in the skill duplicates core text.
