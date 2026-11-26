# Frame handoff to Explore, write-back, and files created through Frame

The handoff card shell (fields, where it is stored, the registers that travel with it) is core's: `koru-core/references/engagement.md` ("The handoff card shell") and `koru-core/assets/templates/handoff-card.md`. Frame fills the phase-specific lines and the content below.

## Contents
- Frame's handoff card entries
- Write-back after Explore
- Files created and updated through Frame

## Frame's handoff card entries

| Field | Frame's entry |
|---|---|
| What we hand on | The one-page framed brief and the research pack (1 or 2 personas, 5 to 8 JTBDs, a competitive scan of 3 to 5 products), all `final` |
| Format and template | The 9-section brief template. Pack files as `.md` with front matter |
| Where it lives and what it's called | Claude project knowledge, for example `deskly-frame-brief-v1-final` and `deskly-frame-research-pack-v1-final` |
| What the next stage must be able to do with it | Write two direction cards without going back to the client, and see which facts are high and which are low confidence |
| What it doesn't include | A full PRD, any solution direction, and any research not yet done |
| Who signs it off | The senior (brief) and the research owner (pack), by name |
| Checked by the next stage (name) | To fill (leave blank for the next stage) |
| Stale-check result | No open warnings on any artefact in the handoff, with the date the check ran |
| Assertion confidence | The count of high, medium and low claims across the research pack and the brief |
| Open assumptions and questions handed on | From core's registers: counts and the ids that block Explore |

How to fill it: run `koru-core/scripts/build_registry.py` and `stale_check.py`, then the claim count (`koru-core/scripts/lint_lines.py --count` over the final files); read the sign-off names and dates from the decisions log; list the exact final file names; count the open rows in the assumptions and open-questions registers. Do not fill "Checked by the next stage": that is theirs. Run a self-test of the "must be able to do" line: could someone write two direction cards from these files alone, without asking the client? If not, say what is missing and add it to the open-questions register.

## Write-back after Explore

Frame's write-back is now core's general send-back protocol (`koru-core/references/registers.md`, "Upstream feedback and send-back"). The brief is one page and is never expanded into a full PRD. In Frame terms:

1. What Explore learns enters as new sources (user test findings, client feedback), then flows into insights through claim lines.
2. Explore (or Frame's owner) updates the brief as the next version (v+1, `draft`, then `review`). The stale-check flags every file the new evidence touches, including everything in Explore that derives from the old version.
3. The client re-confirms only if the problem statement or the success outcomes change in meaning. Any other change is logged and shown in the new version.
4. A senior reviews every new brief version before it is final.

When asked to run a write-back: convert the new material as sources (step 10 rules), re-tag affected insights as confirmed, challenged, new or outdated, update the assumptions register, run the stale-check, revise in dependency order, draft brief v+1, and say plainly whether client re-confirmation is triggered and why.

## Files created and updated through Frame

| File | Created at | Updated at | Status path | Signed by | Lives in |
|---|---|---|---|---|---|
| Source files | Step 1, step 10, after Explore | Never edited; a change is a new version | `raw`, `cleaned` | None; a second person confirms front matter | Knowledge base |
| Brief | Step 2 (v1) | 15a, 18, 18a, 19, and write-back (v+1) | draft, review, final | Senior, then client confirms | Drafts in `stages/frame/drafts/`; final in `01-framed-brief` |
| Research pack | Step 6 (v1) | Step 16 (v2) | draft, review, final | Research owner | Drafts in output; final in `02-research` |
| Insight, persona, workflow (including the current-platform inventory), JTBD, scan files | Steps 12, 13, 14b, 15, 15, 14a | After new sources, when flagged | draft, review, final | Checked by the research owner | `02-research` when final |
| Opportunity files | Steps 17 and 18 | As above | As above | Checked by the senior | `02-research` when final |
| Contradictions register | Step 5 | Every step that reads new material | draft, review, final | Checked by the research owner | `02-research` when final |
| HTML summary | Step 20 | When the brief changes | n/a | A second person checks it | Output folder |

The read-me, both logs, the three registers and the handoff card are core's and are updated as core describes. Notes: constraints (15a) and success outcomes (18a) are not separate files; they go straight into the brief. TRACES answers live in research pack v1 (or the TRACES insight file it links). The stale-check produces a list, not a file.
