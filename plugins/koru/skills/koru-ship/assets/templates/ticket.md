---
title: "{{project}} | Ship | Ticket 01 | v1"
description: "TODO: one sentence saying what this ticket builds and which story it serves."
type: ticket
stage: ship
status: draft
version: 1
last_checked: {{date}}
owner: TODO
derives_from: []
---

# {{project}} | Ship | Ticket 01 | v1

## Title
<Verb plus object>
Priority: Medium

## User story
As a <role>, I want <thing>, so that <outcome>. (Story U1)

## Context
- Framed brief: {{project}}-frame-brief-v<n>
- Figma frame: figma:<fileKey>/<nodeId> (or "not pasted: <reason>")
- HTML deliverable: {{project}}-ship-deliverable-v<n>.html#step-<n>
- Relies on (data and API):
  - <assumption the build relies on>. [medium] src: {{project}}-harden-feasibility-v<n> §<section>

## Acceptance criteria
**Happy path**
- Given <context>, when <action>, then <result>.

**Empty**
- Given <context>, when <action>, then <result>.

**Loading**
- Given <context>, when <action>, then <result>.

**Error**
- Given <context>, when <action>, then <result>.

**Success**
- Given <context>, when <action>, then <result>.

**Partial** (only if the screen shows data from another system)
- Given <the other system> returns only part of the data, when <action>, then <result>.

**Roles and permissions**
- Given I am a <role> without <permission>, when I open <screen>, then I see the No permission state.
- Given the approver is away with no delegate, when <action>, then <result from Harden's roles>.

**AI behaviour** (only if the screen has an AI touchpoint)
- Given the AI suggestion is wrong, when the <role> overrides it, then <result> and an audit log line records who changed what, when.
- Given the <role> accepts an AI suggestion, when it is saved, then the audit log records who accepted what, when.

**Edge cases**
- Given <edge data from Harden's edge cases>, when <action>, then <result>.
- Given the user presses submit twice, when the first request is still running, then only one <item> is created.
- Given the session times out mid-task, when the user signs in again, then <result from Harden's edge cases>.

**Data and API**
- Given the <API> fails, when <action>, then <result>.

## States covered
- Empty: {{project}}-ship-deliverable-v<n>.html#step-<n>-state-empty
- Loading: {{project}}-ship-deliverable-v<n>.html#step-<n>-state-loading
- Error: {{project}}-ship-deliverable-v<n>.html#step-<n>-state-error
- Success: {{project}}-ship-deliverable-v<n>.html#step-<n>-state-success

## Screenshots
Capture from these anchors in the HTML deliverable (no image files are made up):
- {{project}}-ship-deliverable-v<n>.html#step-<n>-state-success

## Tokens used
- <token names from tokens.css, for example color-text, space-2>

## Out of scope
- None

## Open questions
- None
