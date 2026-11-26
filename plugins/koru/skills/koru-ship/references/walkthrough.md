# The deliverable's guided walkthrough (Intro.js)

The HTML deliverable carries a guided tour, so a person who has never seen the flow (a new engineer, a client stakeholder, a coding agent's reviewer) learns what each screen is for and how each interaction works before they read the tickets. It is built at S3 and tested at checkpoint 2.

## How it is wired

The template (`assets/templates/deliverable.html`) already holds the wiring. Keep it as it is:

- Intro.js **7.2.0** from cdnjs, the only external files allowed in the deliverable:
  `https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/introjs.min.css` and `.../intro.min.js`.
  Don't change the version without the design lead's say-so; `lint_ship.py` accepts only this one.
- A button `id="start-tour"` labelled "Take the tour". It is hidden if Intro.js did not load, so the deliverable still works offline.
- The tour steps as JSON in `<script type="application/json" id="tour-steps">`. Content lives here, not in the script, so `lint_ship.py` can check it and a person can edit it without touching code.
- The small inline script reads the JSON, starts the tour on the button, and starts it once by itself on a first visit (remembered in the browser; if storage is blocked it simply doesn't auto-start).

## What a tour step looks like

```json
{ "element": "#step-2-state-success", "title": "Suggested amount", "intro": "The amount is suggested from your unit's past requests. Nothing is filled in until you choose 'Use 20'. 'Undo' puts it back." }
```

- `element`: an id that exists in the deliverable (`#step-N`, `#step-N-state-<state>`, `#state-switcher`, or an id you add to a control inside a state, such as `#step-2-accept`). Omit `element` only for the first, welcome step.
- `title`: a few words, the feature's name as the screen shows it.
- `intro`: one to three short sentences: what it is, what to do, what happens next, how to undo. Plain words; the labels on screen in quotes.

## Which steps to include

In journey order:

1. **Welcome** (no element): what the flow is for and who uses it, in one sentence, and that all data is sample data.
2. **The state switcher**: how to jump to any step and state.
3. **One step per screen** (`#step-N`): what the user does here.
4. **One step per feature or interaction a new user must learn**, on the state that shows it:
   - each AI moment: what the suggestion or flag is, why it appears (its reason), the confidence label, accept, change and undo, and that accepting is logged with who accepted it;
   - each flag or warning (for example a possible duplicate): what it means and that it never blocks, if Harden says so;
   - each main action (send, approve, cancel) and what happens after it, including the round or status it leads to;
   - how to read status, and where to see the history;
   - one important non-happy state per screen where it changes what the user does (for example Partial: "no suggestion right now, enter the amount yourself").
5. **Finish**: where the tickets and the handoff note are.

Keep it to what the deliverable does. No add-ons, no behaviour Harden did not define, no promises about speed or accuracy the feasibility answers don't support.

## What `lint_ship.py` checks

- Intro.js loaded only from the pinned cdnjs URLs; no other external file.
- A `#start-tour` button and a `#tour-steps` JSON block that parses.
- Every step has an `intro`; every `element` is an id that exists in the page.
- At least one tour step inside each `Step N` screen, and one on the state switcher.
- No tour step mentions add-ons.

## Checkpoint 2: the walkthrough test

1. Pick someone who has **not** seen the flow and did not build the deliverable (checker pool, or an organiser). Record their name.
2. They open the file, take the tour from the start, then click through every step and state with the switcher.
3. Ask: "After the tour, what could you do, and where did you get stuck?" Save their words verbatim as a source: `stages/ship/sources/<project>_walkthrough-test_v<n>.md`. Never write their answer yourself.
4. Each sticking point is fixed in a new version of the deliverable (tour included) or logged as an open question with an owner.
5. The design lead confirms the deliverable. Log the confirmation (stage `ship`, who, date). S4 does not start before it.
