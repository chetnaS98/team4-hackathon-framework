---
title: "{{project}} | Harden | Scope | v1"
description: "TODO: one or two sentences saying exactly what this artefact is and what it covers."
type: scope
stage: harden
status: draft
version: 1
last_checked: {{date}}
owner: TODO
derives_from: []
---

# {{project}} | Harden | Scope | v1

What Harden will harden: every screen in Design v1's flow, every role, the data, the AI touchpoints and the screen sizes it must work on. The Screen names here are the names every later Harden artefact uses.

## Screens
`Data from another system`: None, or the system of record the data comes from (makes a Partial state required).

| Step | Screen | What the user does | Data shown or changed | Data from another system | AI touchpoint | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | <screen name> | | | None | None | <pointer or A id> |

## Roles
| Role | Who they are | Source |
| --- | --- | --- |
| <role> | | <pointer or A id> |

## Data objects
- <object>: created, read, changed or deleted on <screen>. [medium] src: <pointer> §<section>

## Target viewports
Every screen size the flow must work on. Size is width×height in CSS pixels. Say if the device is shared. The hardened screens show the smallest one.

| Viewport | Size | Devices and context | Source |
| --- | --- | --- | --- |
| <name> | <width>×<height> | <devices; shared or personal> | <pointer or A id> |

## Inherited from Explore
- Design system gaps: <Q ids, or None>
- Assumptions blocking Harden: <A ids, or None>

## Out of scope
- <add-ons and anything outside Design v1's flow>
