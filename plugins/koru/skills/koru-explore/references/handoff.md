# Explore handoff to Harden

The handoff card shell (fields, where it is stored, the registers that travel with it) is core's: `koru-core/references/engagement.md` ("The handoff card shell") and `koru-core/assets/templates/handoff-card.md`. Explore fills the lines below. Save the card as `handoff-cards/<project>-explore-handoff-card.md`.

## Explore's handoff card entries

| Field | Explore's entry |
|---|---|
| What we hand on | Design v1 (the `design` artefact, the combined wireframe it links, the insight decisions and the combined add-ons), the final direction, the two journeys, Ideas A and B with their rationale and add-ons, the design system gap list, and the open assumptions and questions that block Harden. All `final`, in `06-explore/` |
| Format and template | Markdown with core front matter; wireframes as self-contained HTML with the front matter in a leading comment. Templates in `koru-explore/assets/templates/` |
| Where it lives and what it's called | `06-explore/` and Claude project knowledge, for example `<project>-explore-design-v1-final`, `<project>-explore-wireframe-combined-v1-final.html`, `<project>-explore-insight-decisions-v1-final`; the Figma frames (section status `Final`) by their registry pointers |
| What the next stage must be able to do with it | Harden the design without going back to the designer for the reasons behind it: every design decision traces to an insight or a named assumption, and every component used is in the design system or listed as a gap |
| What it doesn't include | Production-ready design, a finished visual theme (without a design system, theme exploration comes after Design v1), engineering specifications, and any testing not yet done |
| Who signs it off | The team lead, with an organiser playing the client; the design lead has checked it |
| Checked by the next stage (name) | To fill (Harden's designer or design lead) |
| Stale-check result | No open warnings on any artefact in the handoff, with the date |
| Assertion confidence | The count of high, medium and low lines across the handed-on artefacts |
| Open assumptions and open questions handed on | Counts, and the ids that block Harden (including every design system gap) |

## How to fill it, after B4

1. Make sure Design v1 and everything it links are `final` in `06-explore/` (`references/files.md`, "From draft to final").
2. Run `koru-core/scripts/build_registry.py`, then `stale_check.py`. Any warning: stop and fix it first.
3. Count the high, medium and low lines across the handed-on files.
4. Read the sign-off names and dates from the decisions log.
5. List the exact final file names and the Figma pointers.
6. Count the open rows in the assumptions and open-questions registers with stage `explore`; list the ids that block Harden, and every design system gap id.
7. Leave "Checked by the next stage" blank: that is Harden's.
8. Self-test the "must be able to do" line: for each row of the insight decisions and each screen of the combined wireframe, can you point to an insight, the final direction or an assumption id? Is every component in the design system or on the gap list? If not, say what is missing and add it to the open-questions register.
9. Set Explore to "handed off" in the read-me stage table and link the card there.

## What Harden reads (its step H1)

Harden refuses to start if Design v1 is not `final` or the stale-check has open warnings on it. It reads, in full:

- Explore's `final` artefacts in `06-explore/`: the `design` artefact (Design v1), the combined wireframe it links, `insight-decisions`, `add-ons`, the final direction and the two journeys.
- This handoff card in `handoff-cards/`.
- The read-me's design system path and the design system's registry row.
- The assumptions and open-questions registers: every row that blocks Harden, and every design system gap Explore listed.

So all of these must exist, be `final` and be named as above before the card is signed.

## Send-back from Harden

If Harden finds that the direction will not hold, it comes back as a send-back (core's `registers.md`). The affected Explore artefact gets a new version, the stale-check flags what is built on it, and the team lead signs the new Design v1 version again (with the organiser as client if the re-confirmation trigger is met).
