---
name: update
description: Check for and install a newer job-agent-kit release. Use when the session-start check reports an update, or when the user asks to update / upgrade the kit or "is there a new version".
---

1. Run `bin/update-check.sh --force`. Exit 0 means up to date or offline: say so and stop.
2. Explain the changelog it printed in the user's language: what changes in daily use, and
   anything that changes how the agent behaves (rules, red lines, tracker semantics). Ask before
   installing; an update changes the agent's own instructions, so never install silently.
3. If it lists local edits to kit files, show them. Move personal rules into `CLAUDE.local.md`
   and personal facts into `profile.md` (both git-ignored) with the user's OK, then restore the
   kit file with `git checkout -- <file>`. Never `git stash`, `reset --hard` or discard work
   without asking; never touch git-ignored personal data (profile, tracker, resumes, reports, memory).
4. Install with `git pull --ff-only`. If it is not a fast-forward, stop and explain; do not merge
   or rebase on your own.
5. Verify: `python3 bin/test_jt.py`, `python3 bin/jt.py check` (the user's tracker still
   validates), and re-read `CLAUDE.md`, since your instructions may have changed. If a release
   note asks for a data migration, describe it and run it only after the user agrees.
6. Report the new version, what changed for them, and anything they need to do.
