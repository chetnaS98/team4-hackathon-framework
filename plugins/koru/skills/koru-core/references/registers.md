# Shared registers and the send-back protocol

Four things that run through every stage and must not be tracked separately in each phase. All live in the engagement root; templates are in `assets/templates/`.

## Contents
- Assumptions register
- Open-questions register
- Artefact registry
- Upstream feedback and send-back protocol
- The contradictions register (a phase may keep one)

## Assumptions register

`assumptions-register.md`. An assumption starts in the brief (Frame), gets tested in Explore, and is confirmed or challenged in Harden or Ship. One register tracks it through all stages so nobody re-discovers it.

| Id | Assumption | Raised in (stage, artefact) | If wrong, what breaks | How we check | Owner | Status | Evidence | Last updated (stage) |
|---|---|---|---|---|---|---|---|---|

- Ids are `A1`, `A2`, ... and are never reused.
- Status: `Open`, `Testing`, `Confirmed`, `Challenged`, `Retired`. `Confirmed` and `Challenged` need an evidence pointer (the traceable-line pointer form).
- Every assertion with `src: none` in any artefact gets a row (or points to an existing one). The riskiest three are marked as such.
- An assumption that survives three reviews without being tested is flagged: it has quietly become a "fact" and needs a check.
- When an assumption is confirmed or challenged, update the row, log it, and run the stale-check: artefacts that rested on it may now be stale.

## Open-questions register

`open-questions-register.md`. Questions for the client or an engineer, with an owner and a date, so nothing is blocked by a question nobody owns.

| Id | Question | Asked of (person, role) | Owner on our side | Due | Blocks (stage, step) | Status | Answer and source |
|---|---|---|---|---|---|---|---|

- Ids are `Q1`, `Q2`, ... and are never reused.
- Status: `Open`, `Asked`, `Answered`, `Dropped` (with a reason).
- Before a stage's handoff, list every open question that blocks the next stage; the handoff card counts them.
- An answer is a new source: record where it came from, and run the stale-check.

## What a later stage feeds into the registers

Every stage uses these registers; none keeps its own. Explore, for example: each "Assumptions" line in a direction becomes a row in the assumptions register (stage `explore`); design system gaps and anything the designer must ask the client or an engineer become open-questions rows (blocking Harden, where relevant); the wireframes, the combined design and the design system are registry rows with `derives_from`. A later stage that confirms or challenges an earlier assumption updates the same row and logs it.

## Artefact registry

`artefact-registry.md`. An index of every artefact: stage, version, status, home, external link, signer, and what it derives from. It is what the stale-check reads for things that are not files.

| Artefact | Stage | Type | Version | Status | Home | External link | Pointer | Signer | Derives from |
|---|---|---|---|---|---|---|---|---|---|

File artefacts are filled from front matter by `scripts/build_registry.py`. Add rows by hand for non-file artefacts (a Figma frame, a Jira ticket, an HTML page) with their link, `Pointer` (the `figma:` or `jira:` string used in `src:`), version, status and `Derives from`. The signer column is filled from the decisions log when an artefact is signed.

## Upstream feedback and send-back protocol

Frame's write-back after Explore becomes a general rule: anything a later stage learns that changes an earlier output goes back to the earlier output as a new version. Nothing is patched in place, and nothing is quietly worked around.

1. **Raise it.** Record what was learned, where (the later artefact and the evidence pointer), and which earlier artefact it changes. Add a line to the decisions log with stage `core` and the artefact affected.
2. **New source.** What the later stage learned enters as a new source (test findings, an engineer's constraint, client feedback), so it flows through traceable lines.
3. **New version.** The owner of the earlier artefact makes the next version (`v+1`, `draft`, then `review`). The old version is marked replaced in the decisions log. The stale-check then flags everything built on the old version.
4. **Re-sign-off.** The new version needs the checks and sign-offs its type requires in the matrix. The client re-confirms only if the stage's re-confirmation trigger is met (`governance.md`); otherwise the change is logged and shown in the new version.
5. **Harden can send a direction back to Explore.** A direction that fails hardening (it cannot be built, tested or made accessible as stated) goes back with the reason as a send-back; Explore revises it as a new version. The send-back names who decides whether the revised direction needs the client again.
6. **Close it.** When the earlier stage has issued the new version and the stale-check is clean, mark the send-back resolved in the decisions log.

Core does not decide the content of any send-back; it only requires that it is raised, versioned, re-signed as the matrix says, and logged.

## The contradictions register (a phase may keep one)

Frame keeps a living contradictions register (the requirements document against the evidence, and one source against another). Any phase can keep one in the same form: numbered entries, both sides cited, impact, status, and who can resolve. A contradiction is resolved only by a person with authority or by new evidence; never mark one Resolved yourself. The Frame format is in `koru-frame/references/file-specs.md`.
