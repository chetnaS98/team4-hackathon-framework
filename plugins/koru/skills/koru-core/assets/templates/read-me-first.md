# 00 Read me first: {{project}}

**What the project is:** TODO
**Client alias used in derived artefacts:** {{client_alias}}
**Started:** {{date}}
**Engagement size:** {{size}} (set at kickoff; see the decisions log)
**Knowledge base:** TODO (location, connectors)
**Design system:** not decided (with DS: link to the existing design system; without DS: link to the internal wireframes Figma DS)

## Stages
| Stage | Skill | Status | Lead | Handoff card |
|---|---|---|---|---|
| Frame | koru-frame | not started | | |
| Explore | koru-explore | not started | | |
| Harden | koru-harden | not started | | |
| Ship | koru-ship | not started | | |

Status values: not started, active, handed off. Each active stage appends its own step tracker below.

## Roles
*(Every role the active stages require must be named before any step: `scripts/check_roles.py` must pass. Roles a stage does not require may stay blank until that stage starts. If two people share a name, add a surname or initial.)*

| Role | Name |
|---|---|
{{role_rows}}

## Client
- Decision makers:
- Review rhythm:

## Where everything lives
- Finals for project knowledge: the numbered folders at this folder's root (`01-framed-brief/`, `02-research/`; `03-rulebook/` and `04-design-library/` are reserved for Harden)
- Drafts: `stages/<stage>/drafts/`
- One decisions log (`05-decisions-log.md`) and one AI quality log (`ai-quality-log.md`) for the whole project
- One break log (`break-log.md`) and one playbook changes log (`playbook-changes.md`)
- Registers: `assumptions-register.md`, `open-questions-register.md`, `artefact-registry.md`
- Handoff cards: `handoff-cards/`

## Project context
- Who writes to it: each stage's signer adds that stage's `final` files (senior and research owner in Frame, team lead in Explore, rulebook owner and design lead in Harden, engineer in Ship).
- Who maintains it: the **context keeper** (Roles). Uploads only `final` files, removes replaced versions, runs the stale-check rhythm.
- How we know it's out of date: the stale-check reports a newer version of anything an artefact derives from, or a `final` file has a newer `final` version that is not yet uploaded.

## Stale-check
Owner: the context keeper · Last run: never
