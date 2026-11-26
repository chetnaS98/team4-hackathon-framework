---
title: "{{project}} | Ship | PR readiness | v1"
description: "TODO: one sentence: what a pull request for this flow would take (a pull request itself is out of scope)."
type: pr-readiness
stage: ship
status: draft
version: 1
last_checked: {{date}}
owner: TODO
derives_from: []
---

# {{project}} | Ship | PR readiness | v1

A pull request is out of scope for Ship. This note says what one would take, so the build team can start without a planning meeting.

## Spec per unit
- <how the journey splits into units; here each ticket is a unit with its own spec>

## Plan per ticket
- <a coding agent in plan mode writes plan.md per ticket; the engineer approves before any code>

## Questions file
- <questions.md with an [Answer]: slot per question; who answers; how answers become new ticket versions>

## Component build
- <components to build first (design system gaps), from the ticket, the deliverable and tokens.json>

## Journey tests in CI
- <end-to-end and accessibility tests for every journey path and state; where they run>

## Review action
- <a review action comments on each pull request and never approves; the code owner merges>

## Setup still missing
- <open items from the client setup list, with Q ids, or None>
