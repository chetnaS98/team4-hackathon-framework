---
title: "{{project}} | Harden | States | v1"
description: "TODO: one or two sentences saying exactly what this artefact is and what it covers."
type: states
stage: harden
status: draft
version: 1
last_checked: {{date}}
owner: TODO
derives_from: []
---

# {{project}} | Harden | States | v1

Every state of every screen in the scope. Every screen has Empty, Loading, Error and Success (Not applicable with a reason if one cannot happen). A screen that shows data from another system also has Partial. A screen where any role has a No in the roles table also has No permission. Screens with an AI touchpoint also have AI thinking, AI low confidence, AI wrong and AI override.

| Screen | State | What the user sees | Copy (draft) | How they recover or move on | Source |
| --- | --- | --- | --- | --- | --- |
| <screen> | Empty | | | | design decision |
| <screen> | Loading | | | | design decision |
| <screen> | Error | | | | <feasibility pointer or A id> |
| <screen> | Success | | | | design decision |
| <screen> | Partial | <what shows when the other system is slow, down or incomplete> | | | <feasibility pointer or A id> |
| <screen> | No permission | <what a role without access sees> | | | <roles pointer> |

## AI touchpoints
### <touchpoint name> (<screen>)
- Trigger: <what makes the AI act>
- Who sees a wrong answer: <role, and where they see it>
- Who fixes it: <role, and how>
- How the user overrides or undoes it: <action>
- How it is logged: <where a wrong output and its fix are recorded, and who reviews them>
- Accepted suggestions audit-logged: <Yes: who accepted, what, when, where stored; or not yet known with a Q id>
