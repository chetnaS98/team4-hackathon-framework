---
description: Log something that broke or needed a workaround (the break log)
argument-hint: "<what broke> [what we did instead] [blocked|slowed|minor]"
---

Add one line to the engagement's break log. From `$ARGUMENTS` (and the conversation) work out: what broke or needed a workaround, what we did instead, and how bad (blocked, slowed or minor). Ask only for what's missing, in one question. Then run:

```bash
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/log.py" break --engagement <engagement folder> --what "<what broke>" --instead "<what we did instead>" --severity <blocked|slowed|minor>
```

The stage defaults to the active one; pass `--stage` if the break belongs to another. Confirm the logged line in one sentence and carry on with what you were doing.
