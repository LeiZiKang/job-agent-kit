# .agent-memory

Shared memory for every agent working in this repo (Claude Code, Codex, ...). It is the only
project memory; do not keep project facts in a tool's private memory.

- `INDEX.md`: entry point: one-line project description, current state, next steps, record list.
- `handoff.md`: latest handoff. `bin/jt.py board` shows sections whose heading contains
  "Needs you" or "In progress".
- `claude-feedback.md`: one-line friction/helpfulness observations; choose 1–3 environment
  improvements at weekly review and record their results.
- `decisions/` and `findings/`: one decision or finding per file, named `YYYY-MM-DD-title.md`.

Frontmatter for each record:

```yaml
---
type: decision | finding
date: YYYY-MM-DD
author: claude-code | codex | ...
status: active | superseded
superseded_by: <file name, only when superseded>
---
```

Rules: never delete a record, mark it `superseded` and link the replacement. Re-read a file before
editing (another agent may have changed it). Always set `author`. No secrets. Find live records
with `grep -rl "status: active" .agent-memory/`.
