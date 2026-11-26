---
description: Log a change to the playbook itself (steps, skills, templates, roles) with the reason
argument-hint: "<what changed> because <why>"
---

Add one line to the engagement's playbook changes log (what changed in the process, not a project decision; project decisions go in the decisions log). From `$ARGUMENTS` work out what changed, why, and who made the call (ask if the person isn't clear; never assume a name). Then run:

```bash
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/log.py" change --engagement <engagement folder> --what "<what changed>" --why "<why>" --by "<name>"
```

Confirm the line in one sentence. If the change should also be made to a skill file, say which file and offer to make it.
