# Frame review: checker additions, sign-off sequence, rhythm

The general checking rules, the roles registry, the sign-off matrix and the size thresholds are in `koru-core/references/governance.md`. This file adds only what is specific to Frame.

## Frame-specific checks (added to core's hand-over checklist)

1. Were all the request sources read and cited (the brief, the requirements document and any kickoff or client call transcripts)? Ask for the coverage list.
2. Is every list in the sources (goals, requirements, metrics, users) reproduced in full where the brief says so?
3. Is anything between the title and section 1 of the brief that should not be there?
4. In the brief, are the riskiest three assumptions listed first, with what breaks if each is wrong?
5. For TRACES, is every letter answered twice (request and workflow), and is each answer something that could be written as the handbook's "you have X when you can write" sentence, or an open question?
6. Are source counts honest (same interviews or same author counted once)?

## Frame sign-off sequence

Core's matrix has the rows. In order:

1. The research pack is reviewed, then the **research owner** signs it.
2. The framed brief is reviewed, then a **senior** signs it.
3. The **client confirms the framed brief**: the problem, who it is for, success looks like and the answers to open questions. Record who confirmed, the date and the channel in the decisions log.
4. Both are marked `final` and go into Claude project knowledge. The brief is not final until the client has confirmed.

A client change to the brief becomes a new version, and the stale-check flags everything built on it. The client re-confirms only if the problem statement or the success outcomes change in meaning.

## Review scales with size

Core's thresholds apply (async comments within a day for small, a live 45 to 60 minute meeting for large). Frame's size questions: how many workflows, how many source files, how many stakeholder groups. Whether a senior reviews every new brief version: yes (core default).

## The Frame AI quality log

Use core's log and categories. Frame's typical entries: a claim without a source, a dropped speaker label in conversion, a skipped request source, a list summarised instead of reproduced, two claims on one line, an overstated citation.
