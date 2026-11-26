# The framed brief

## Contents
- Template (9 sections)
- How TRACES lands in the brief
- Brief across versions
- Rules for writing it

One page. The problem is one sentence in the final brief. Success looks like is 2 or 3 outcomes.

## Template

| Section | What goes in |
|---|---|
| 1. Problem | In brief v1, the problem in the client's words. In the final brief, the problem statement: user, obstacle, impact and measure, with no solution in it |
| 2. Who it's for | Specific roles, their context and skill level, and who decides |
| 3. What we know | Facts, each a claim line with a confidence level and a source |
| 4. What we're assuming | Claims with no source, with what breaks if wrong and how we would check. The riskiest three are listed first |
| 5. Where AI fits | Screen, agent, both or neither, and why |
| 6. Constraints | Tech, business, regulatory and time limits, what must not change, edge cases, what has been tried, fixed dates and their reasons |
| 7. Success looks like | 2 or 3 outcomes we could observe, for the user and the business |
| 8. Open questions | What we still need from the client. Required |
| 9. Signed off by | The senior and the client's confirmation, with names and dates |

The ready-to-fill file is `assets/templates/brief.md`.

## How TRACES lands in the brief

TRACES (Trigger, Result, Audience, Confidence, Edges, Say-so) is the checklist the early steps fill, asked about both the request and the workflow underneath it.

| Letter | Lands in |
|---|---|
| **T** Trigger | Problem and What we know |
| **R** Result | Success looks like |
| **A** Audience | Who it's for |
| **C** Confidence | What we know and What we're assuming |
| **E** Edges | Constraints |
| **S** Say-so | Constraints (fixed dates) and Signed off by |

The client's decision makers and the review rhythm go in `00-read-me-first`, not in the brief.

## Brief across versions

- **v1 (step 2, `draft`)**: written from all the request material (the written brief, requirements doc and any kickoff or client call transcripts). Problem in the client's words. Provisional path label. Fill each section only from the source; a section the request cannot fill says "not yet known". Anything without a source goes to What we're assuming. Open questions listed for the client.
- **Constraints (step 15a)** and **Success looks like (step 18a)** are not separate files. They go straight into sections 6 and 7.
- **Where AI fits (step 18)** goes into section 5.
- **Final (step 19)**: one page, drafted from the opportunities and the research pack. Senior signs, client confirms, then `final`.
- **After Explore**: the next version (v+1, `draft`, then `review`). The client re-confirms only if the problem statement or the success outcomes change. Anything else is logged and shown in the new version.

## Rules for writing it

- **Nothing between the title and section 1.** No italic context line, no "built from..." note, no path label. Provenance lives in the decisions log, the progress tracker and the front matter `description`. (Feedback on the Meridian brief v1: the framing line was unwanted.)
- **Reproduce enumerated lists in full.** When a source lists goals, requirements, metrics or users, put every item in the brief as a clear numbered list, in the source's own words and order, under one claim line that carries the source. Never compress a list to "including X and Y". (Feedback: the PRD's seven goals were missing.)
- **Use every source that arrived as the request** (brief, requirements doc, and any kickoff or client call transcripts), not just the written documents. See step 1 and step 2 in `steps.md`.
- Never expand it into a PRD. One page.
- No solution in the problem statement. If the client's request contains a solution idea, move it to What we're assuming and say what breaks if it is wrong.
- Section 3 contains only claim lines with a real source. Section 4 lists the riskiest three assumptions first.
- Section 8 is required, even if the answer is "none outstanding" (and then say why that is believable).
- Strip client names from the text; use the role or "the client".
- If the page overflows, cut detail from What we know (keep the highest-confidence lines) rather than shrinking the problem or success sections, and say what was cut.
