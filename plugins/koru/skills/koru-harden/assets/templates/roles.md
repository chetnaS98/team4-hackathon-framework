---
title: "{{project}} | Harden | Roles and permissions | v1"
description: "TODO: one or two sentences saying exactly what this artefact is and what it covers."
type: roles
stage: harden
status: draft
version: 1
last_checked: {{date}}
owner: TODO
derives_from: []
---

# {{project}} | Harden | Roles and permissions | v1

For each role and each screen or action. Cells: Yes, No, Own only, or not yet known. Name action rows `<screen>: <action>`. Any No means that screen needs a No permission state.

| Role | Screen or action | See | Change | Undo | Approve | Must not see | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <role> | <screen> | | | | | | <pointer or A id> |

## If a permission changes mid-flow
- <what the user sees>

## If the person who must act is away
- <step that needs an approver or owner>: who can act instead, and what happens if nobody is named (who is told, after how long, how it is unblocked)
