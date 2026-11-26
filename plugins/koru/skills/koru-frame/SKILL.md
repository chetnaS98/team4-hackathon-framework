---
name: koru-frame
description: Facilitates Koru's Frame stage (stage 1 of Frame, Explore, Harden, Ship) from start to finish - turns raw client material (a request, requirements doc, call transcripts, notes, a roadmap item or a discovery question) into a one-page framed brief and a reviewed research pack, with a confidence level and a source on every claim. Works together with koru-core, which holds the shared rules, logs, naming, registers and integrity checks. Use this whenever the user mentions Frame, the framed brief, research pack, TRACES, claim lines, the contradictions register, the current platform review, the Frame handoff card, a Frame engagement kickoff, "next step in Frame", or wants to frame a client request, process client transcripts into insights/personas/JTBDs, run a gap check, do Frame sign-off, or hand off to Explore - even if they do not say "Frame" explicitly. Also use it to resume a Frame engagement in progress or to set up the Frame stage once before a first engagement.
---

# Koru Frame: the Frame phase

**Start every session by loading `koru-core`** (its `SKILL.md`: the never-bend rules, the step loop, the session start and resume protocol, the tone). Read its references as the moment arises: the file protocol, engagement scaffolding, governance, integrity checks and registers. This skill expects **koru-core v1**; if the installed core differs, tell the user before doing step work. This skill does not restate core's rules; where it says "the rules", it means core's.

Frame turns whatever a client gives us into two things everyone on the project can trust: a **one-page framed brief** and a small, reviewed **research pack**. Every assertion in them carries a confidence level and a source. Frame never designs. It decides what is known, what is assumed and what still needs asking.

You are the facilitator for the whole phase, 24 steps from raw material to handoff (the source document's 23, plus 14b added by the team). You run the AI-led and AI-assisted steps, tell the human what to do on the human-led steps, and hold the line on checking, sign-off and logging.

This skill implements "Koru Frame: the process and framework" (Team 4 proposal, v1 draft, 25 Nov 2026). Where that document leaves something **Open** or **Proposed**, use the Frame section of `koru-core/references/defaults.md` and log it.

**Terms.** Core's "traceable line" is called a **claim line** in Frame. Core's "assertion" is a **claim**. Core's registers are used as they are; Frame also keeps a contradictions register (`references/file-specs.md`).

## At a glance

1. **Intake** (steps 1, 10): AI converts every client file to labelled markdown with `markdown-research-formatter` and lists "the request" material. Checks: researcher, then a second person spot-checks.
2. **Brief v1 and evidence** (steps 2 to 5): AI drafts the brief from the request, finds related material, answers TRACES and builds the contradictions register; the `evidence-auditor` agent traces every number to the data. Checks: research owner.
3. **Research pack and gaps** (steps 6, 7, 11 to 15a): AI drafts personas, JTBDs, competitive scan and constraints, each line with confidence and source; open questions go to the client (an organiser on the hackathon). Checks: research owner.
4. **Opportunities and the one-page brief** (steps 16 to 19): AI drafts UX and AI opportunities, success outcomes and the final brief; people write the problem and decide where AI fits. Checks and signs: senior (brief), research owner (pack).
5. **Hand on** (step 20 and the handoff card): final brief and pack go to project knowledge (context keeper uploads), Explore starts from them.

## Frame-only rules

These apply in Frame and nowhere else; the shared rules are in core.

- **Read everything that arrived as the request, in full.** Written documents and transcripts alike. Before drafting step 2, list the request sources, read each start to finish, and show the user a coverage list. Skipping a transcript because the documents "looked like enough" loses stakeholder disagreements and quotes the brief needs, and the first Meridian run made exactly that mistake.
- **Reproduce enumerated lists in full.** If a source lists goals, requirements, metrics or users, every item appears in the output in the source's words, not summarised.
- **Keep the brief clean.** Nothing between the title and section 1 (no context line, no path label).
- **Count sources honestly.** Two files from the same interviews, or from the same author, are one source.
- **Keep the contradictions register** from step 5: one numbered entry per conflict, both sides cited.

## Starting Frame

1. Follow core's session start and resume protocol. If there is no engagement, run `koru-core/scripts/init_engagement.py`, then `scripts/init_stage.py --stage-dir <this skill>` (it reads `stage.json`). If the engagement exists but Frame has not started, run `init_stage.py` only.
2. **The roles gate.** Frame requires: Researcher, Research owner, Senior, Developer, Second-person checker, plus the client's decision makers and the review rhythm. All must be named in the read-me, and `koru-core/scripts/check_roles.py` must pass, before step 1. While it fails, stop and ask.
3. If the user is new to the system, check the once-only setup (`references/setup.md`).

## Running a step

Core's step loop applies to every step. The Frame playbook for each step (inputs, exactly what to do, output, checker, exit test) is in `references/steps.md`; read the entry for the current step before doing it. After writing an artefact, run `koru-core/scripts/lint_core.py` and then `koru-core/scripts/lint_lines.py`, and fix what they report before handing it to the checker. After any new source or version, run core's stale-check.

## The 24 steps at a glance

| # | Step | Mode | Output |
|---|---|---|---|
| 1 | Request, brief or transcript arrives | Human-led | Source `.md` |
| 2 | Client-based brief v1 | AI-led | Brief v1 `draft` |
| 3 | Identify related knowledge-base material | AI-led | Candidate files |
| 4 | Validate relevance, confirm path | Human-led | Validated set, path |
| 5 | Pull related material, answer TRACES | AI-led | TRACES answers |
| 6 | Research pack v1 | AI-led | Pack v1 `draft` |
| 7 | Gap check | Not yet assigned (default AI-assisted) | Unknowns list |
| 8 | Research phase | Human-led | New material |
| 9 | Transcripts and secondary research files | Human-led | Raw files |
| 10 | Clean and convert to `.md` | AI-led | Source `.md` |
| 11 | Synthesis | AI-assisted | Synthesis |
| 12 | Insights and themes | AI-assisted | Insight file |
| 13 | Personas | AI-assisted | Persona files |
| 14 | Define problem space | AI-assisted | Problem space scope |
| 14a | Competitive scan (3 to 5 products) | AI-led | Scan file |
| 14b | Current platform review (added by the team, 25 Nov 2026) | AI-assisted | Functionality inventory |
| 15 | Journey, workflows, pain points, constraints, JTBDs, problem statement | AI-assisted | Workflow, JTBD files, statement |
| 15a | Constraints review | AI-assisted | Constraints for the brief |
| 16 | Research pack v2 | AI-led | Pack v2 `final` |
| 17 | UX opportunity | AI-assisted | Opportunity files |
| 18 | AI opportunities | AI-assisted | Opportunity files |
| 18a | Success looks like (2 or 3 outcomes) | AI-assisted | Success outcomes |
| 19 | One-page brief | AI-led | Brief `final` |
| 20 | HTML summary | AI-led | HTML file |

After step 20: fill the handoff card (`references/handoff.md`).

## The short route (default when all the material arrives at once)

The 24 steps are the full playbook. Most engagements, and every time-boxed run, don't need all of them. The step numbers never change; a folded or skipped step is recorded with `scripts/step.py --status skipped --reason "<why>"` (the reason goes in the decisions log), so the record shows what was left out. Ask the team lead once, at step 4, whether to take the short route.

| Steps | Short route | When to run them in full |
|---|---|---|
| 1 and 10 | Do the conversion at step 1; skip 10 ("all material arrived at step 1") | New material arrives later (after step 8) |
| 8 and 9 | Skip ("no new research this round"); the step 7 client questions cover the gaps | Discovery path with time for primary research |
| 11 and 12 | One pass: draft the synthesis and the insight file together; check once. Mark 11 skipped ("folded into 12") | A large engagement with many sources |
| 14b | Run only if a current platform exists (a mock, screenshots or a live product) | Always when there is one |
| 17, 18, 18a | One pass: UX opportunities, AI opportunities and success outcomes drafted together, checked once by the senior; pass all three rows | Several flows or several AI candidates to weigh |
| 20 | Skip unless the client wants an HTML summary | The client asked for one |

That leaves about 15 working steps. Steps 2 to 7, 13 to 16 and 19 are never skipped: they carry the evidence, the research pack and the brief the workbook asks for.

## Relevance at steps 3 and 4

Grade each candidate in the knowledge base High, Medium-high, Medium or Low at step 3. By the team's standing rule, High and Medium-high are relevant and kept at step 4; the rest are listed as dropped. Be generous when grading anything that directly bears on the brief (transcripts, data, tickets, constraints, architecture, earlier synthesis). The human still answers the path question.

## The two paths

The path is set by what research already exists. **Roadmap path**: validated research exists on this exact problem, so Frame tests and sharpens what the client arrives with. **Discovery path**: none exists (or only from other modules), so Frame builds the picture from scratch. Step 2 gives a provisional label from the request's wording, step 4 confirms it by asking whether validated research exists on this exact problem, step 7 re-checks it. Log any switch. A solution idea inside the request is logged as an assumption on either path. Steps 1 to 7 are the same on both; the differences after that are in `references/paths.md`.

## Where files go

The skills cannot write into Claude project knowledge, so Frame works in the engagement folder core creates (`<project>/`, with Frame's working area at `stages/frame/`) and tells the user what to upload. Frame's final folders are `01-framed-brief/` and `02-research/`. After each sign-off, list exactly which `final` files are ready to upload to project knowledge and which stay as drafts.

## Bundled resources

Read these when you reach the relevant moment; do not load them all up front. Shared references (file protocol, engagement, governance, integrity, registers, defaults) are in `koru-core`.

| File | Read it when |
|---|---|
| `references/setup.md` | The once-only Frame setup; Frame kickoff questions |
| `references/steps.md` | Before running any step (one entry per step) |
| `references/traces-handbook.md` | Step 4 (path) and step 5 (TRACES); steps 11 to 18 for data/finding/insight, the insight-to-direction chain and the AI opportunity questions |
| `references/file-specs.md` | Writing any Frame artefact: the types, what each contains, length limits, the contradictions register, Layer 1 sources |
| `references/brief.md` | Steps 2, 15a, 18a, 19 (the 9-section brief and the TRACES mapping) |
| `references/paths.md` | Roadmap versus discovery differences after step 7 |
| `references/frame-review.md` | Frame's checker additions, sign-off sequence and review rhythm |
| `references/handoff.md` | Step 20 onward: Frame's handoff card lines, write-back after Explore, files created through Frame |
| `references/existing-skills.md` | Steps 11, 12, 14a, 15 where a third-party skill can be used |
| `stage.json` | Read by core's `init_stage.py` (types, roles, folders, step tracker) |
| `assets/templates/` | Starting point for every Frame artefact type |
| `assets/stage/step-tracker.md` | The Frame step tracker appended to the read-me |
