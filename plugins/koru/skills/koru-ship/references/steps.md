# Step playbook: S1 to S9

Read the entry for the current step before running it. Each entry gives: who, mode, what AI does, output, checker, exit test. The loop itself (announce, do, write, hand to checker, record, move on) is core's. Every AI output starts as `draft`. Names follow core's file protocol (`<project>-ship-<artefact>-v<n>-<status>`). Templates are in `assets/templates/`.

## Contents
- S1 Share the Harden handoff
- S2 User stories (and S2 early)
- S3 HTML deliverable
- S3b React starter (optional)
- S4 Tickets
- S5 Handoff note and PR readiness note
- S6 Agent pre-check
- S7 Engineer review (checkpoint)
- S8 Deliver tickets
- S9 Close
- What the design engineer does

---

## S1. Share the Harden handoff (human-led)

- **Who:** the design lead shares the Harden handoff card, or says where the final hardened design is.
- **Ask:** "Please share the Harden handoff card, or tell me where the final hardened design is, so I can start." Do nothing else until you have it.
- **AI does:** run `scripts/lint_ship.py --intake <engagement>`. It refuses when there is no `final` hardened design, when a newer draft of it exists, when `tokens.css` is missing, or when core's stale-check has warnings. If it refuses, say Harden has not handed on, name what is missing, and stop.
- Then read **all** of it, in full: the `hardened-design` artefact and every file it links (screens HTML, tokens with `tokens.css` and `tokens.json`, scope, states with its AI touchpoints block, roles, edge cases, accessibility, feasibility, rulebook chapters used, rulebook check, checklist, Ship notes), the Harden handoff card, the final framed brief, the read-me (design system path, roles), the decisions log, and the open rows in the registers that block Ship. Also read any early draft stories in `stages/ship/drafts/stories/`.
- **Confirm back in three lines:** the core flow and its screen count; the states, roles and AI touchpoints you see; the Ship notes, open questions and assumptions handed on (counts and ids).
- **Output:** the intake check result and the tracker row. **Checker:** the person who shared it confirms the three lines. **Exit:** intake check passes and the three lines are confirmed.

## S2. User stories (AI-assisted)

- **Who:** Claude drafts, the design lead judges.
- **AI does:** write 3 to 5 user stories for the one core flow, in `assets/templates/user-story.md`. One story per thing a user does that is worth building on its own (usually one or two journey steps of the flow). Each story: `As a <role>, I want <thing>, so that <outcome>.`, the screens (`Step N`) it covers, the roles it touches (names from Harden's `roles`), and a Basis line citing the hardened design. Roles and outcomes come from Harden and the framed brief, never invented. Anything in the flow no story covers goes under "Not covered by a story" with a reason.
- If early stories exist, re-base them on the hardened design as a new version: keep what still holds, change what Harden changed, and say what changed, one line per change.
- **Checkpoint 1 (stories agreed).** Show the design lead and the engineer the stories and the "Not covered by a story" list. Ask exactly: "Are these the stories we will build, and is anything here you would not build or would split?" Each answer is theirs, recorded in their words. Do not start S3 until both confirm. Log the confirmation (stage `ship`, who, date). A change they ask for is a new version of the stories, checked again.
- **Output:** `<project>-ship-user-story-v<n>-draft.md` in `drafts/stories/`. **Checker:** design lead; **confirms:** design lead and engineer. **Exit:** 3 to 5 stories, every screen of the flow covered by a story or listed as not covered, lints clean, checkpoint 1 logged.

### S2 early (draft stories while Explore and Harden work)

- Allowed when Explore's Design v1 (and the framed brief) are `final`. Ship need not be started: write to `stages/ship/drafts/stories/` (create it) and do not run `init_stage.py`, so the stage table does not change.
- Read only `final` artefacts: Explore's `design` and the combined wireframe, the framed brief. Never Harden drafts.
- `derives_from` lists the Explore and Frame artefacts. Status stays `draft`; the description says "Early draft from Explore Design v1; to be re-based on the hardened design at S2".
- `lint_core.py` will warn that Ship has no registered types until Ship starts. That warning is expected here.
- Log one decisions-log line (stage `ship`): early stories drafted, by whom.

## S3. HTML deliverable (AI-led)

- **Who:** the design engineer runs the session with Claude; the design lead checks.
- **AI does:** build one self-contained, clickable HTML file of the core flow from `assets/templates/deliverable.html`:
  - **Reuse Harden's screens.** Copy each screen section's markup from the final `screens` HTML; do not redraw it. Paste `tokens.css` verbatim into the `:root` block. Below it, use only `var(--token)` values for colour; never write a raw colour.
  - Every screen in journey order, labelled `Step N: <screen name from scope>`, inside `<main>`, with `id="step-N"`, shown at the smallest target viewport with Harden's `Viewport: <name> <width>×<height>` label kept.
  - Every state Harden defined for that screen, labelled `State: <name>`, with `id="step-N-state-<state>"`. Role differences shown where `roles` says a role sees something different (label them, for example `State: No permission`).
  - A state switcher (`id="state-switcher"`) listing every step and state as anchor links; it must work offline and without the script.
  - Clickable: the main action in each step's Success state links to the next step.
  - AI moments show their reason, their confidence, and accept, change and undo controls, as Harden's states and the rulebook define.
  - Realistic made-up data, including the edge data from `edge-cases` (long names, no data, a lot of data). Mark it as sample data.
  - A "Design system gaps" section (or "None"), and an "Anchors" appendix listing every step and state anchor and the ticket that uses it (filled after S4).
  - **The Intro.js walkthrough** (`references/walkthrough.md`): a "Take the tour" button (`id="start-tour"`), and the tour steps as JSON in `<script type="application/json" id="tour-steps">`. At least one tour step per screen (`#step-N`), one for the state switcher, and one for each feature and interaction a new user must learn: each AI moment (what the suggestion is, how to accept, change and undo it), each flag or warning, each main action and what happens after it, and how to read status. Plain words, the labels on screen, no add-ons. The tour starts on the button; it may start by itself on a first visit.
- **Checkpoint 2 (walkthrough test).** Someone who has not seen the flow (from the checker pool, or an organiser; never the person who built the deliverable) opens the file, takes the tour, then clicks through every state. Ask them: "After the tour, what could you do, and where did you get stuck?" Save their words verbatim as a source (`stages/ship/sources/<project>_walkthrough-test_v<n>.md`). Fix what they got stuck on (new version of the deliverable, tour included) or log it as an open question. The design lead then confirms the deliverable. Do not start S4 before that confirmation is logged (stage `ship`, who, date).
  - Front matter in the leading comment; `derives_from` the screens, tokens, states, roles, edge cases and hardened design.
- **Run:** `lint_ship.py <file> --tokens <04-design-library>/tokens.css --screens <08-harden>/<screens>.html`. The `--screens` check fails if any step or state in Harden's screens is missing from the deliverable.
- **Output:** `<project>-ship-deliverable-v<n>-draft.html` in `drafts/deliverable/`, and the walkthrough test source. **Checker:** the design lead opens the file in a browser, takes the tour and clicks every step and state; **confirms:** the design lead, after the new user's test. **Exit:** lints clean (the walkthrough check included); the new user's words recorded and each sticking point fixed or logged; checkpoint 2 logged.

## S3b. React starter (optional, AI-led)

- **When:** only if, at checkpoint 1, the engineer asks for a React starter and the client setup list says the client builds in React. Otherwise the team lead skips it (`step.py --skip-optional --by <name>`); the HTML deliverable is always the reference. Run it after checkpoint 2, so it copies a deliverable a new user has already tested.
- **Who:** the design engineer runs the session with Claude and checks it.
- **AI does:** copy `assets/templates/react-starter/` to `drafts/react/<project>-ship-react-starter-v<n>-draft/` and rename `manifest.md` to `<project>-ship-react-starter-v<n>-draft.md` (the manifest shares the folder's name; it is the artefact, the code is its content). Then:
  - Paste Harden's `tokens.css` verbatim into `src/tokens.css`. Style only with `var(--token)`; never a raw colour.
  - One component per screen in `src/screens/Step<N><Name>.tsx`, in journey order, registered in `src/screens/index.ts`. Each starts with `// koru-anchor: #step-N` and lists every state Harden defined in `states`, with the same ids as the deliverable's anchors (`ai-low-confidence`). Copy the structure, labels and copy text from the deliverable; do not redesign.
  - The app shell (`App.tsx`) already gives the state switcher and the `#step-N-state-<id>` links, so tickets can link the deliverable and the starter with one anchor.
  - Sample data only, in `src/data/`, with Harden's edge data. No API calls, no URLs, no packages beyond the template's pinned ones unless the engineer names one.
  - Fill the manifest: how to run, one row per screen (`| Step | Screen | Component | Anchor |`), what this is not (and what the build team will change).
- **Claude does not install packages.** The design engineer runs `npm install` and `npm run build` (Node 18 or later), records the result in "How to run", and clicks every step and state.
- **Run:** `lint_ship.py <starter folder> --tokens <04-design-library>/tokens.css --screens <08-harden>/<screens>.html`.
- **Output:** the starter folder. **Checker:** design engineer. **Exit:** lints clean; the build passes on the design engineer's machine; every state reachable. Sign-off promotes the whole folder to `07-ship/<...>-final/` (without `node_modules/` and `dist/`).

## S4. Tickets (AI-led)

- **Who:** the design engineer runs the session with Claude; the design lead checks. The engineer reads them again at S7.
- **AI does:** one ticket per user story, in `assets/templates/ticket.md`, following `references/tickets.md`. For each ticket:
  - Title (verb plus object), the story, context links (framed brief, Figma frame, the deliverable anchor), and the data and API it relies on as claim lines citing `feasibility` or `ship-notes`.
  - Acceptance criteria, one Given/When/Then per line, covering: the happy path; every state of every screen in the ticket (from `states`, including Partial for data from another system and No permission); every role permission (from `roles`: who can and cannot see, change, undo, approve, and what happens when the person who must act is away); AI behaviour (from the AI touchpoints block in `states`: what triggers it, what happens when the AI is wrong, who sees and fixes it, how it is undone, and the audit log line for accepted suggestions); edge cases (from `edge-cases`, including double submit, approver away with no delegate, session timeout and the target viewports); the system that owns each piece of data, its freshness and API failure (from `scope` and `feasibility`).
  - If S3b ran, a Context line naming the starter component for each screen in the ticket (`src/screens/Step<N><Name>.tsx`).
  - States covered with their anchors; screenshots as anchors; tokens used (from `tokens.css`); out of scope; open questions as Q ids from the register.
  - Close the Ship notes: each Harden Ship note SN<n> is either closed in a ticket (an acceptance criterion or an out-of-scope line that names "Ship note SN<n>") or carried in the handoff note (S5).
- A behaviour Harden did not define is not decided here: add an open question (asked of the design lead or engineer) and leave the criterion out until it is answered. If it changes what a user sees, send it back to Harden (`references/handoff.md`).
- **Run:** `lint_ship.py <tickets folder> --tokens <tokens.css> --ship-notes <harden ship-notes>` (the Ship-note check passes only once the handoff note exists, after S5). Then update the deliverable's Anchors appendix with the ticket numbers (a new version only if the deliverable is already `final`).
- **Output:** `<project>-ship-ticket-<nn>-<slug>-v1-draft.md` x 3 to 5 in `drafts/tickets/`. **Checker:** design lead. **Exit:** every ticket passes the lints; every state in the ticket's screens has a criterion.

## S5. Handoff note and PR readiness note (AI-led)

- **Who:** the design lead runs it with Claude; the design engineer checks.
- **AI does:** write the handoff note (`assets/templates/handoff-note.md`, half a page): what's in the deliverable, what's not, the decisions engineers should know about (linked to decisions-log lines), who to ask (names and roles from the read-me). List each Harden Ship note not closed in a ticket under "Harden Ship notes", with why. Then write the `pr-readiness` note (`assets/templates/pr-readiness.md`): what a pull request would take, using the team's approach (spec per unit, plan per ticket in plan mode, a questions file with `[Answer]:` slots, component build, journey tests in CI, a review action that never approves) and what is still missing from the client setup list.
- **Run:** `lint_ship.py <handoff folder> <tickets folder> --ship-notes <harden ship-notes>`.
- In iteration 2 or later, set `iteration: <n>` in the note's front matter and add `## What changed since iteration <n-1>`: the build team's feedback (cite its source), what changed, and the new version of each artefact.
- **Output:** `<project>-ship-handoff-note-v<n>-draft.md`, `<project>-ship-pr-readiness-v<n>-draft.md` in `drafts/handoff/` (the next version number; in iteration 1 that is v1). **Checker:** design engineer. **Exit:** lints clean; every Ship note closed or carried; the note fits on half a page.

## S6. Agent pre-check (AI-led)

- **Who:** Claude launches the agent; the design engineer fixes; the design lead checks the resolutions.
- **AI does:** launch the plugin agent `handoff-reviewer` (`plugins/koru/agents/handoff-reviewer.md`). Give it only the Ship drafts (tickets, deliverable, handoff note, PR readiness note, and the React starter's manifest and `src/` if S3b ran) and the design library (`04-design-library/`). It reads them cold and lists every question an engineer would ask, ending with "Buildable without questions: n of N". If the agent is not installed, launch a general subagent with the brief in `references/handoff.md` ("The cold read brief"), and say so.
- Record the result verbatim in `assets/templates/review.md` (reviewer: `handoff-reviewer agent`). Then, with the design engineer, resolve every row: **fixed** (a new version of the ticket, note or deliverable; say which) or **logged** (an open question with an owner). Never mark a row resolved without one of these. Log what the agent caught that the AI drafts missed in the AI quality log (category `missed` usually).
- **Output:** `<project>-ship-review-agent-v1-draft.md` in `drafts/review/`, plus new versions. **Checker:** design lead. **Exit:** every row has a resolution; re-run the agent if more than a third of tickets were not buildable, and log the second score.

## S7. Engineer review (checkpoint, human-led)

- **Who:** a named engineer (not the person who ran S3 or S4).
- **AI does:** prepare a one-page review pack: the file list with versions, the agent score and what was fixed, the open questions, and the question to answer: "Could you or your coding agent build this without coming back to us? List anything you'd still need to ask." Then wait.
- When the engineer replies, save their words verbatim as a source in `stages/ship/sources/` (for example `<project>_engineer-review_v1.md`). Record it in `review.md` (reviewer: the engineer's name and role), citing the source. Turn each answer the team gives into a new version of the affected ticket, note or deliverable; anything unanswered becomes an open question with an owner.
- **Checkpoint:** stop until the engineer confirms the new versions cover their list. Log the confirmation (stage `ship`, who, date). Then the engineer signs the tickets, the handoff note and the PR readiness note, and the design lead signs the deliverable (core sign-off matrix, `references/core-additions.md`). Log each sign-off with "sign-off" in the decision text. Before any `final`, run core's stale-check.
- Promote signed artefacts to `final` (new file name and front matter status) and move them to `07-ship/`. Superseded drafts move to `superseded/`.
- **Output:** the source, `<project>-ship-review-engineer-v1-draft.md`, the `final` set. **Checker:** the engineer. **Exit:** the engineer's list is recorded and each item answered or owned; sign-offs logged; stale-check clean.

## S8. Deliver tickets (AI-led, then a person)

- **Who:** Claude runs the export; the engineer (or whoever has Jira) imports; the design engineer checks the count.
- **AI does:** run `scripts/export_tickets.py --engagement <project>` (finals only). It writes `07-ship/export/iteration-<n>/tickets.csv` (Jira's CSV import format) and `tickets.md` (one combined file to paste). If the deliverable will be hosted, pass `--link-base <url>` so ticket links work outside the folder. Follow `references/tickets.md` ("Delivering tickets").
- **GitHub (optional):** `--github owner/repo` prints what it would create. Show the user that list and ask in chat whether to create those issues. Only after a clear yes, run again with `--yes`. If `gh auth status` fails, tell the user to run `gh auth login` themselves, and deliver the CSV meanwhile.
- After delivery, add a registry row per delivered ticket (`jira:<KEY>` or `github:<owner>/<repo>#<n>` pointer, status `final`), once the person gives you the keys. Never invent a key.
- **Output:** `07-ship/export/iteration-<n>/` (earlier iterations stay as they were). **Checker:** the engineer confirms the tickets arrived with the `koru-final` label (or that the CSV is in their hands). **Exit:** delivery confirmed and logged.

## S9. Close (AI-led, then the signers)

- **AI does:** fill the Ship handoff card (`references/handoff.md`) for this iteration at `handoff-cards/<project>-ship-handoff-card-v<iteration>.md` (route.py prints the iteration; never edit an earlier iteration's card); run `koru-core/scripts/build_registry.py` and `stale_check.py`; confirm `07-ship/` holds only `final` artefacts and the generated export; list exactly which files go to Claude project knowledge. Self-test the "must be able to do" line on one ticket.
- **Signers:** the engineer and the design lead. **Checked by:** the build team's engineer (named). Then tell the orchestrator Ship is ready to hand off: it runs `advance_stage.py --engagement <project> --confirmed-by "<name>"`. Ship is the last stage, so this closes the engagement.
- **Exit:** every step passed or skipped, card signed, stale-check clean, a named person confirmed.

---

## What the design engineer does

The design engineer bridges design and code. In Ship they: run the S3 and S4 sessions with Claude (deliverable and tickets); map the design library to code (tokens to the client's token pipeline, components to the client's components or Storybook entries, gaps to new components); fix what the agent pre-check finds (S6); check the handoff note (S5) and the delivered ticket count (S8); own the one-time client setup list (`client-setup.md`); and later answer a coding agent's `questions.md` during the build.
