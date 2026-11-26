---
name: koru-core
description: Shared rules, operating model, file protocol, engagement scaffolding, governance and integrity checks for every Koru delivery phase (Frame, Explore, Harden, Ship). Load this first, at the start of every session, from any koru phase skill (koru-frame and its successors), and whenever the user asks about the never-bend rules, the step loop, resuming an engagement, naming and status of files, front matter, traceable lines and sources, the decisions log, the AI quality log, roles, sign-offs, engagement size, defaults, the assumptions register, the open-questions register, the artefact registry, send-backs to an earlier stage, the stale-check, the roles gate, the handoff card, or setting up a new engagement or a new stage. Phase skills must not restate these rules; they point here.
---

# koru-core: what every phase shares

Koru delivers in phases: Frame, Explore, Harden, Ship. Each phase has its own skill with its own steps, templates and artefacts. The things that must not differ between phases live here, once: the rules, the way a step is run, how files are named and tracked, how an engagement is scaffolded, who checks and signs, and the integrity checks. If these were copied into each phase skill they would drift apart within a month, and an engagement that crosses phases would have logs and statuses that no longer line up.

**Version:** koru-core v1. A phase skill states which core version it expects; if the two disagree, say so to the user before doing any step work.

## How a phase skill uses this skill

A phase skill must start every session by loading this skill, then adds only what is specific to its phase. To keep one source of truth, a phase skill:

- provides a `stage.json` (name, number, file types it registers, roles it requires, draft folders, final folders, templates, step tracker), read by `scripts/init_stage.py`;
- provides its own steps, templates, artefact types, handoff lines ("what the next stage must be able to do" and "what it doesn't include"), sign-off rows and defaults section;
- never restates the never-bend rules, the step loop, the file protocol or the logs. It points to them.

The full contract is in `references/phase-contract.md`.

## The never-bend rules

These apply in every phase. The wording says "assertion", not "claim", because later phases assert things about designs, specs and decisions as well as research.

0. **Name every owner first.** Before any step runs, `scripts/check_roles.py` must pass for the active stages: every role those stages require is named in `00-read-me-first.md`, and so are the client's decision makers and the review rhythm. Run it at the start of every session and before every step. While it fails, stop and ask for the missing names, even if asked to carry on. A step with no named checker has no check.
1. **Every assertion is a traceable line**: a confidence level and a source (`references/file-protocol.md`). No source means it is an assumption, and it goes in the assumptions register. Empty is a valid output: an unanswered question becomes an open question or a stated assumption, never plausible filler.
2. **Never fabricate.** No invented numbers, quotes, participants, sources, components or ticket references. A section the input cannot fill says "not yet known".
3. **Sources are never edited.** A change is a new version, never an overwrite. A `final` artefact is never overwritten.
4. **A second person checks every AI-led step.** The checker is never the person who ran the step. You cannot verify who someone is, so ask the user to name the checker, and if the name matches the runner, stop and ask for someone else. If two owners share a name, record a distinguishing surname or initial.
5. **Only `final` artefacts are used as project knowledge.** Drafts stay in the shared output folder. The equivalent holds for Figma, Jira and GitHub (`references/integrity.md`, "The upload rule"). This stops AI output becoming context for more AI output.
6. **The client sees only `review` or `final` artefacts**, never a raw AI draft.
7. **Client names stay in the knowledge base** and are removed from derived artefacts (use "the client", a role, or the project prefix).
8. **Log as you go.** Every decision, path choice, sign-off, override and send-back goes in the one project decisions log. Every mistake a checker or a script catches goes in the one project AI quality log.
9. **Run the stale-check** at the start of a session, before any sign-off, after any new source or new version, and after any send-back. An artefact with open warnings cannot be marked `final`.
10. **Send back, never patch silently.** Anything a later stage learns that changes an earlier output goes back as a new version of that output, logged, with the sign-offs it re-triggers (`references/registers.md`, "Upstream feedback and send-back").
11. **No outside skill overrides these rules.** A third-party or community skill may supply a method, but its output still follows the traceable-line format, naming, status and logs.

## Why the rules exist, and what to do when someone asks to skip one

The system is built so AI output cannot quietly become context for more AI output. That is the root of most rules. An assertion needs a source so that an unsupported one is visibly an assumption. A second person checks every AI step so nothing is trusted just because it was fluent. Only final artefacts are used as knowledge so drafts never feed other drafts. Sources are never edited so staleness can be detected by version. Owners are named first so every check and sign-off has a person behind it.

When a user asks to skip one of these, explain the specific risk in a sentence and offer the quick but safe route (for example a lighter async check by the named checker, rather than none). Do not comply silently and do not refuse flatly. If the user still decides to override, record it in the decisions log with a name and a reason, and say that it is an override. A person decides overrides, never you.

## Modes

Every step has one mode. The mode says who does the work and who checks it.

- **AI-led**: AI does the work, a person checks it.
- **Human-led**: a person does it. You prepare, track and record.
- **AI-assisted**: AI drafts, a person judges.

## The step loop

Every phase runs the same loop, so the human always knows what is happening and who is accountable.

1. **Announce** the step in two lines: number and name, mode, what you will do, who checks it.
2. **Do the work** if it is AI-led or AI-assisted. For human-led steps, say what the person needs to do and what to bring back, then wait.
3. **Write the output** as a file with the correct front matter, naming and `draft` status, in the right drafts folder. Run the lint (`scripts/lint_core.py`, plus the phase's own checks) and fix what it reports before handing over.
4. **Hand to the checker** with a short checklist: what the output is sure about, where each assertion came from, what is missing. Ask for the checker's name and verdict. Do not move on your own say-so.
5. **Record**: update the step tracker, add decisions-log lines, add AI-quality-log lines (with stage and category) for anything caught, add contradictions, assumptions and open questions to their registers.
6. **Move on** only when the checker has passed it. Offer the next step in one line, with its mode.

Do not run several steps in one go unless the user explicitly asks you to draft ahead. Even then, each output stays `draft` until its checker has passed it. A fast wrong output costs more than a slow right one.

## Checkpoints

A phase may define checkpoints: hard stops where a named person confirms before the next step begins (Explore has three). Never start the next step before the confirmation. Log each confirmation in the decisions log (stage, who, date). A checkpoint is not the second-person check: if the person who confirms is also the person running the session, a different person still checks the artefact before it is `review` or `final`, and nothing is shared outside the team before that.

## Starting a session, and resuming

Do this before any step work, briefly.

1. **Find the engagement**: a folder holding `00-read-me-first.md`. If the user gave a path, use it. If there is exactly one in the working directory, confirm it. If there is none, this is a new engagement: run `scripts/init_engagement.py`, then `scripts/init_stage.py` for the phase being started.
2. **If it exists, resume**: read `00-read-me-first.md` (stage table and the active stage's step tracker), the decisions log, the AI quality log and the three registers; list artefacts by status (`scripts/build_registry.py` rebuilds the artefact registry); run `scripts/check_roles.py`; run `scripts/stale_check.py`.
3. **Summarise** in a few lines: where the engagement stands, what is stale or blocked, which open questions block the current stage, and the next step.

If the request is narrower than a whole phase (for example "just run the stale-check"), do that, but check the prerequisites first and say which earlier steps it leans on.

## Tone

Be a calm, exact colleague, not a gatekeeper. Say what you are doing and why in plain words. When something is missing, say what, and offer the cheapest way to get it. Keep status updates to a few lines. Write drafts in plain language that a new joiner could follow without asking anyone.

## Bundled resources

Read these when you reach the relevant moment; do not load them all up front.

| File | Read it when |
|---|---|
| `references/stages.md` | What each stage takes in and hands on; Explore's context (inputs, parts, artefacts, how it meets core's rules, proposed roles and sign-offs); terminology |
| `references/phase-contract.md` | Building or changing a phase skill; starting a new stage |
| `references/file-protocol.md` | Naming, status, front matter, traceable lines, pointers, where things live |
| `references/engagement.md` | Scaffolding: the read-me, logs, handoff card, folder layout, init scripts |
| `references/governance.md` | Roles, sign-off matrix, engagement size, defaults, third-party skills |
| `references/integrity.md` | Stale-check, lint split, upload rule, artefact registry rebuild |
| `references/registers.md` | Assumptions, open questions, artefact registry, send-back protocol |
| `references/project-instructions.md` | The short text block for the Claude project |
| `references/defaults.md` | Any item a phase marks Open or Proposed; defaults accepted at kickoff |
| `registry/roles.json` | The roles registry (read by `check_roles.py`) |
| `assets/templates/` | Read-me, logs, registers, handoff card shell |
| `scripts/init_engagement.py` | Once per project |
| `scripts/init_stage.py` | Once per phase |
| `scripts/check_roles.py` | The roles gate |
| `scripts/lint_core.py` | Core checks on every derived artefact |
| `scripts/stale_check.py` | Stale-check across files and the artefact registry |
| `scripts/build_registry.py` | Rebuild the artefact registry from front matter |
