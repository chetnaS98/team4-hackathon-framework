---
title: "{{project}} | Ship | React starter | v1"
description: "TODO: one sentence: a React starter of the core flow, one component per screen, built on the design library tokens, with sample data only."
type: react-starter
stage: ship
status: draft
version: 1
last_checked: {{date}}
owner: TODO
derives_from: []
---

# {{project}} | Ship | React starter | v1

<!-- Rename this file to match its folder: <project>-ship-react-starter-v<n>-draft.md inside
     <project>-ship-react-starter-v<n>-draft/. This file is the artefact; the code is its content. -->

A reference starter for the build team: the core flow as React components, using the same anchors, states and tokens as the HTML deliverable. It is not production code, it is not a pull request, and nothing here is merged into the client's codebase.

## How to run
- Needs Node 18 or later. From this folder: `npm install`, then `npm run dev` (or `npm run build` and open `dist/index.html`).
- Built and checked by: TODO (name, date, Node version, result of `npm run build`)

## Screens and components
| Step | Screen | Component | Anchor |
| --- | --- | --- | --- |
| 1 | TODO | src/screens/Step1Example.tsx | #step-1 |

## Tokens
`src/tokens.css` is Harden's `tokens.css`, copied verbatim. Components use only `var(--token)` for colour.

## What this is not
- Not production code: sample data only, no API calls, no authentication, no routing library, no state library.
- Not the client's stack: TODO (what the build team will change: their component library, data layer, tests).
- The HTML deliverable stays the reference. If the two disagree, the deliverable wins and this starter gets a new version.
