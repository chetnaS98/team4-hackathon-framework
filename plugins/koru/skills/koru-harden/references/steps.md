# Harden step playbook

Read the entry for the current step before running it. Each gives: mode, inputs, what to do, output, checker, exit test. Core's step loop (announce, do, write, hand to checker, record, move on) applies, and Harden shows its Part/Step/Next header at the start of every reply. Every AI output starts as `draft`. Every assertion is a claim line with a source. Each new assumption gets a row in core's assumptions register (stage `harden`); each question for the client or an engineer gets a row in the open-questions register.

Exact artefact structures are in `artefacts.md`. Names follow `[project]-harden-[artefact]-v[n]-[status]`.

## Contents
- Part 1 Intake: H1 to H4
- Part 2 Harden: H5 to H10
- Part 3 Build: H11 to H13
- Part 4 Rulebook: H14 to H17
- Part 5 Handoff: H18, H19

---

## H1. Share the Explore handoff (human-led)

- **Designer does:** shares the Explore handoff card or says where the final Design v1 is.
- **You read, in full:**
  - Explore's `final` artefacts in `06-explore/`: the `design` artefact (Design v1), the combined wireframe it links, `insight-decisions`, `add-ons`, the final direction, the two journeys.
  - The Explore handoff card in `handoff-cards/`.
  - From Frame's finals: the brief's "Who it's for", "Constraints", "Success looks like" and "Where AI fits"; the personas; the current-platform workflow if there is one.
  - The read-me: the design system path, and the design system's registry row.
  - The assumptions register and open-questions register: every row that blocks Harden, and every design system gap Explore listed.
  - `03-rulebook/` and `04-design-library/`, if anything is in them.
  - Any product architecture or UI library the client gave (sources in the knowledge base).
- **Refuse to start** if Design v1 is not `final`, or if the stale-check shows open warnings on it. Say which, and stop.
- **Exit:** everything above read; confirm back in three lines (the flow, the design system path, how many screens and roles).

## H2. Scope inventory (AI-led)

- **You do:** list exactly what Harden will harden.
  - **Screens:** every screen in the combined wireframe, in journey order, with what the user does, the data shown or changed, which other system any of that data comes from (the system of record, so there is one source of truth), and whether AI is involved.
  - **Roles:** every role that touches the flow (from the brief and the personas, including admins, approvers and people who only see results). A role nobody named in the sources is an assumption.
  - **Data objects:** the things the flow creates, reads, changes or deletes.
  - **AI touchpoints:** where AI suggests, decides or acts, and on whose behalf.
  - **Target viewports:** every screen size and device the flow must work on (for example shared desktop workstations, tablets, large screens), with the size in pixels and whether the device is shared. From the brief's constraints or the tech material; a size nobody named is an assumption.
  - **Inherited:** the design system gap ids and the assumption ids that block Harden.
  - **Out of scope:** add-ons and anything outside Design v1's flow.
- **Output:** `scope` (`part-1-intake/`). `derives_from` Design v1, the combined wireframe, the brief and the design system row.
- **Checker:** the design lead. **Exit:** every screen in the combined wireframe is a row; every role, AI touchpoint and target viewport has a source or an assumption id.

## H3. Feasibility questions (AI-led, then the designer sends)

- **You do:** list every question an engineer must answer for the design to be buildable as drawn, so the engineer can start now and not at the end. Look for: where the data comes from and how fresh it is; what an action does in the back end and whether it can be undone; sync, latency and offline; permissions the system can actually enforce; integrations; volumes (how many items a list might hold); what the AI model can and cannot return (confidence, explanations, timing); anything the brief's constraints or the tech-constraints source flags.
- Each question names the screen and the design decision it affects, so the answer can change something. Write them into the `feasibility` artefact's table with the answer column empty, and add each to the open-questions register (asked of the engineer, blocking Harden H9).
- **Pre-check first.** Launch the `koru:feasibility-engineer` agent on the engagement folder before finalising the list. It writes a separate pre-check (green, amber, red per screen element, and up to 8 questions). Merge its questions into the list. The pre-check is never cited as an answer: only the engineer's verbatim answers at H9 are.
- **Designer does:** sends the list to the engineer and books a time before H9. Record who and when in the decisions log.
- **Output:** `feasibility` v1 (`part-2-harden/`, questions only). **Checker:** the design lead. **Exit:** sent, and the engineer's name and date are logged.

## H4. Checkpoint 1 (checkpoint)

- **Ask exactly:** "Shall I start hardening these [N] screens for these [N] roles?" Do not start H5 until the designer confirms, the design lead has passed the scope, and the engineer is booked. Log all three.

## H5. States (AI-led)

- **You do:** for **every** screen in the scope, define each state: Empty, Loading, Error, Success, and where they apply Partial (some data missing), Stale (data may be out of date) and No permission (a role that cannot open or act). Two are always required:
  - **Partial** on every screen whose scope row names data from another system (that system can be slow, down or incomplete).
  - **No permission** on every screen where any role has a `No` in the `roles` table (write `roles` first if you need to, or revisit states after H6).
- For every screen with an AI touchpoint, add AI thinking, AI low confidence, AI wrong, and AI override (the user overrides or undoes it), plus an AI touchpoints block per touchpoint. The block says exactly what happens when the AI is wrong: the trigger, who sees a wrong output, who fixes it and how, how the user overrides or undoes it, how it is logged, and that every accepted suggestion is audit-logged with who accepted it, what and when. A state that cannot happen is a row with "Not applicable" and the reason.
- For each state say what the user sees, draft copy in plain words, and how they recover or move on. A state the sources do not describe is still written (it is a design decision), but anything it assumes about the system ("the save can be retried") is a claim line citing the feasibility answer or an assumption id.
- **Output:** `states`. **Checker:** the design lead. **Exit:** `lint_harden.py --scope` (run on `states` and `roles` together) reports full coverage, Partial and No permission included.

## H6. Roles and permissions (AI-led)

- **You do:** for each role and each screen or action: can they see it, change it, undo it, approve it, and what must they never see. Use Yes, No, Own only, or "not yet known". Name action rows `<screen>: <action>` so they match the scope. Every permission that rests on the system enforcing it cites the feasibility answer or an assumption id. Note what happens when a role's permission changes mid-flow, and what happens when the person who must act (an approver, an owner) is away: who can act instead, and what happens if nobody is named. These become acceptance criteria for who can do what.
- Every row with a `No` means the matching screen needs a No permission state in `states`.
- **Output:** `roles`. **Checker:** the design lead. **Exit:** every role in the scope has a row for every screen.

## H7. Edge cases (AI-led)

- **You do:** check every screen against the standard set and the domain set.
  - **Standard set (always):** long text (names, labels, translations); no data; a lot of data (paging, search, performance); two people editing at once; a double submit (the same action sent twice); slow or no network; an item renamed, moved or deleted while in use; a permission removed mid-flow; an approver or owner away with no delegate (what stops, who is told, how it is unblocked); a session timeout mid-task (what is kept, what the user sees on return, and the idle time on shared devices); dates, times and time zones where relevant; every target viewport in the scope, smallest first.
  - **Domain set:** from the sources: support tickets, the contradictions register, the current-platform review, interview findings. Each cites its source.
- For each: what happens today in Design v1, and the design response.
- **Try to break it.** With states, roles and edge cases drafted, launch the `koru:hardening-critic` agent on the engagement folder. It walks the flow as each role in awkward situations and writes a list of breaks with the smallest fix and a fix-here, Ship note or send-back suggestion. Add the breaks to the edge cases (new version) and carry them into the H10 decision list; log anything it caught that the drafts missed in the AI quality log.
- **Output:** `edge-cases`. **Checker:** the design lead. **Exit:** the standard set is covered for every screen where it applies (a case that cannot happen says so in the design response); each domain case cites a source.

## H8. Accessibility (AI-assisted)

- **Standard:** WCAG 2.2 AA (default; the team may change it in core's defaults).
- **You do:** for every screen: keyboard path and focus order; visible focus; accessible names for every control and icon; headings and landmarks; errors identified in text, not colour alone; status changes announced (loading, AI thinking, success); target size at least 24 by 24 CSS pixels; nothing that depends on colour alone; content reflows at the smallest target viewport with no loss of content or function. Run `scripts/contrast_check.py` on the tokens file's contrast pairs (or on the Design v1 colours if the tokens file does not exist yet).
- If the `design:accessibility-review` skill is installed, you may use it for the method (it audits WCAG 2.1 AA; add the 2.2 items above yourself). Its output still goes into the `accessibility` artefact in this format.
- **Design lead does:** judges the Fail and "Not checked" rows: what needs a real screen-reader or keyboard test before Ship.
- **Output:** `accessibility`. **Checker:** the design lead. **Exit:** every screen checked; every Fail has a fix or is a gap for H10.

## H9. Feasibility (human-led, with the engineer)

- **Engineer does:** answers the H3 questions, in writing or in a call.
- **You do:** have the answers converted to a source file, verbatim (`stages/harden/sources/`, in the knowledge base), then fill the `feasibility` artefact's answer column as claim lines citing it, and the design impact of each answer. List the limits the engineer named. Update the open-questions register (Answered, with the source). Questions still unanswered stay "not yet known".
- **Output:** `feasibility` v2. **Checker and signer:** the engineer. **Exit:** every question answered or recorded as open with an owner and a date.

## H10. Checkpoint 2: fix, note or send back (checkpoint)

- **You do:** gather every gap from H5 to H9 into one list and propose, for each, one of: **fix here**, **Ship note**, or **send back to Explore**, using the rule in `harden-review.md`. Give a one-line reason for each.
- **Ask exactly:** "Here is what hardening found. Do you agree with fix here, Ship note or send back for each?" The designer and the design lead decide. Log each send-back and the count of fixes and notes.
- If anything is sent back, follow `handoff.md` ("Send-back to Explore") and pause Harden on the parts it touches.

## H11. Tokens and design library (AI-assisted)

- **You do:** follow `design-library.md` for the design system path in the read-me.
  - With a design system: copy its colour, type, spacing and radius tokens into the `tokens` artefact, citing the design system version. For each Explore gap, propose the closest existing component or a new component entry; the rulebook owner decides.
  - Without one: build the `tokens` artefact from Design v1's colours, type, spacing and radius, each citing where in Design v1 it came from. Set up the library skeleton.
- Add the contrast pairs the screens use and run `scripts/contrast_check.py`. A failing pair is fixed here (a new token value) or logged.
- Run `scripts/export_tokens.py` to write `tokens.css` and `tokens.json` beside the artefact.
- **Output:** `tokens` (`part-3-build/`; `04-design-library/` once final). **Checker and signer:** the rulebook owner. **Exit:** contrast check clean or each failure logged with a decision.

## H12. Hardened screens (AI-led)

- **You do:** build the hardened design as one self-contained HTML file (no external scripts, stylesheets or images), using the tokens and the design system so it looks like the real product.
  - Every screen in the scope, in journey order, each labelled `Step N: <screen>`.
  - Every state from `states` shown for that screen, each labelled `State: <name>`. A small inline state switcher is fine; it must work offline.
  - Every screen shown at the smallest target viewport from the scope, labelled `Viewport: <name> <width>×<height>` (a fixed-width frame is enough). Show a larger viewport too where the layout changes.
  - Role differences shown where `roles` says a role sees something different.
  - Every "fix here" decision from H10 applied. List them at the end of the page under "Fixes applied in this version".
  - A "Design system gaps" section (or "None").
  - Front matter in a leading HTML comment; `derives_from` the combined wireframe, `scope`, `states`, `roles`, `edge-cases`, `accessibility`, `feasibility`, `tokens` and the design system row.
- **Output:** `screens` v1 (`part-3-build/`). **Checker:** the design lead. **Exit:** `lint_harden.py --scope` reports every screen and every state present, and the smallest target viewport shown.

## H13. Changes (AI-assisted)

- **You do:** make only the changes asked for. After each round, list what changed, one line per change. Each round is a new version. If a change touches a state, role or edge case, update that artefact too (new version) so they stay in step. If a change would change the idea itself, stop: that is a send-back.

## H14. Rulebook chapters (AI-assisted)

- **You do:** follow `rulebook.md`. Read the chapters in `03-rulebook/` that apply to this flow. If a chapter is missing, draft it in the chapter format, holding only rules that change a design decision in this flow, each tracing to a decision, an insight or a source. Update an existing chapter only as a new version.
- **Output:** `rulebook-chapter` (one per chapter, `part-4-rulebook/`; `03-rulebook/` once final). **Checker and signer:** the rulebook owner. **Exit:** every rule has an id, a must or must-not, and a check.

## H15. Rulebook checks (AI-led)

- **You do:** check the hardened screens against every rule in every applicable chapter. For each rule and each screen and state it applies to: Pass, Break or Not applicable, with the reason. For each Break propose an action: fixed now (a new `screens` version), a Ship note, a send-back, or a rule conflict (the client wants something a rule forbids: an open question for the rulebook owner and the client's decision maker; never decide it yourself).
- **Output:** `rulebook-check`. **Checker:** the rulebook owner, who passes it. **Exit:** no Break without an action.

## H16. Hardening checklist (AI-led)

- **You do:** fill the ten-item checklist (`artefacts.md`), each item Pass, Gap or Not applicable, with a pointer to the artefact that proves it. For "Checked against the system as a whole", compare the hardened flow with the product's other flows and patterns (the product architecture, the current-platform review, the design system's patterns) and name any place it behaves differently from the rest of the product.
- **Output:** `checklist`. **Checker:** the design lead. **Exit:** every item has evidence.

## H17. Checkpoint 3: sign-offs (checkpoint)

- **Prepare** the three sign-offs and ask each person for their verdict, name and date: the engineer (feasibility), the rulebook owner (rulebook checks and tokens), the design lead (the hardened design: scope, states, roles, edge cases, accessibility, screens, checklist). Run the stale-check first: nothing with open warnings can be signed. Log each sign-off. Do not start H18 until all three are in.

## H18. Ship notes and the hardened design (AI-led)

- **You do:** write `ship-notes`: the fixes travelling to Ship (from H10 and H15), the API and data assumptions engineers must know (claim lines citing the feasibility source), the open questions that block Ship, and what is out of scope. Then write `hardened-design`, which ties everything together and is what Ship reads.
- Run `koru-core/scripts/build_registry.py`, then `stale_check.py`.
- **Output:** `ship-notes`, `hardened-design` (`part-5-handoff/`; `08-harden/` once final). **Checker:** the engineer reads `ship-notes` as Ship would; the design lead signs `hardened-design`. **Exit:** lint and stale-check clean.

## H19. Handoff card (AI-led, then the signers)

- **You do:** fill the Harden handoff card (`handoff.md`), self-test the "must be able to do" line, and list exactly which files move to `03-rulebook/`, `04-design-library/` and `08-harden/`, and which Figma frames get the `Final` section status. Tell the user to do the upload and labelling.
- **Signers:** the design lead and the rulebook owner. **Checked by:** Ship's team. **Exit:** the card is signed and the stage table says Harden is handed off.
