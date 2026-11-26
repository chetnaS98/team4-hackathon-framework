# One-time setup for a new client

Do this once per client, not once per engagement. The design engineer owns the list; the engineer and the client's technical contact answer it. Ask at Harden's feasibility step if you can, so the answers are in by Ship. Each answer is a source (save it in `stages/ship/sources/`, verbatim); each item still unknown at S1 is an open question with an owner, and the `pr-readiness` note lists what is missing.

Status per item: `done` (with the source), `not needed` (with a reason), or the open-question id.

## Codebase access

- [ ] Which repository (or repositories) the flow lives in, and the default branch.
- [ ] Read access for the design engineer and for a coding agent; who grants it.
- [ ] Branch and review rules: protected branches, required reviewers, code owners.
- [ ] Where a project instruction file for coding agents lives (for example `CLAUDE.md`), and who may change it.
- [ ] Whether hooks may block edits to `final` design files and raw inputs.

## API calls

- [ ] Every endpoint the flow reads or writes, with its contract (OpenAPI or similar) or "not yet known".
- [ ] Authentication and the roles the API knows; how they map to Harden's roles.
- [ ] A sandbox or staging environment and test accounts (made by the client, never by Koru).
- [ ] Rate limits, timeouts and error shapes, so error and retry criteria are exact.
- [ ] Data freshness: how old the data can be, and how the UI can tell.
- [ ] Any AI service the flow calls: where it runs, what it logs, and who sees its output.

## Data structures

- [ ] The objects in Harden's scope (created, read, changed, deleted), with field names and types.
- [ ] Sample or seed data the team may use; what must never leave the client (personal data rules).
- [ ] Limits that change the design: maximum lengths, list sizes, time zones, locales.
- [ ] Where audit logs are written, and what a log line holds (who, what, when).

## Components, tokens and Storybook

- [ ] Whether the client has a component library and Storybook (or similar); its URL and version.
- [ ] A map from the design library's components to the client's components; gaps become new components.
- [ ] What the client builds in (React and its version, Angular, other). Ship's optional React starter (S3b) runs only for React; for anything else, the HTML deliverable and tickets are the handoff.
- [ ] How tokens reach code (a token pipeline, CSS variables, a theme file) and whether `tokens.json` can feed it.
- [ ] Whether Figma Code Connect or a similar link between Figma and code is in use.

## Tickets and delivery

- [ ] Where tickets go (Jira project key and issue type, or GitHub repository); whether CSV import is allowed and who runs it.
- [ ] Whether the label `koru-final` is allowed (and created) in that tool.
- [ ] Where the HTML deliverable may be hosted or attached so its anchors work for engineers.

## The walkthrough (Intro.js)

- [ ] The licence position for Intro.js is confirmed before a deliverable with the walkthrough goes to the client. Intro.js is AGPL-3.0 or a paid commercial licence; a client deliverable is usually commercial use. Owner: design lead. If it is not confirmed, ship the deliverable with the tour removed (the deliverable works without it) and log the decision.
- [ ] The client's network allows cdnjs.cloudflare.com, or the tour is accepted as online-only.

## Tests and CI

- [ ] The test runner and where end-to-end and accessibility tests run (for journey tests in CI).
- [ ] Whether a review action may comment on pull requests (it never approves; a person merges).
- [ ] Browsers, devices and screen widths that must be supported.

## People

- [ ] Who answers engineering questions during the build, and how fast.
- [ ] Who merges (code owner), and who on the client side accepts the build.
