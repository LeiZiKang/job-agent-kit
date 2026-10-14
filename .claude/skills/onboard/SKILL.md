---
name: onboard
description: First-run setup for job-agent-kit. Interviews the user and creates profile.md, outreach.md, config.json, tracker.json and .agent-memory/. Use when profile.md is missing or the user asks to set up / reconfigure.
---

# Onboard the user

Goal: in one short conversation, leave the repo fully configured. The user never edits a file
or runs a command. You do everything and show a summary at the end.

## 1. Check the machine (silently, fix what you can)
- `python3 --version` (3.9+). `python3 bin/jt.py init` creates `tracker.json`.
- `command -v codex` and whether `/Applications/ChatGPT.app` contains codex-cli. Codex is optional.
- Which browser tool this session has (built-in browser, Chrome extension, or other). Note it.
- If the user has a resume file, ask for its path and read it. It is the best source of facts.

## 2. Interview (ask in batches of 3-4, offer sensible defaults)
1. Target roles and stack; years of experience per stack; things they have NOT done.
2. Locations / remote; salary floor and target; company types to prefer or avoid; hard no's.
3. Deadline (optional) and how many applications per week feels right.
4. Channels they use and are logged into (LinkedIn, Indeed, company ATS, BOSS, Liepin, email…).
5. Which outward actions you may "do, then report" without asking each time (offer the T1-T6
   menu from `templates/outreach.md`; default: none).
6. Optional: scheduled patrol? At what local times? (needs Codex + Mac awake)

Push back on vague answers ("any frontend role") with a concrete question. Facts you can read
from the resume, do not ask.

## 3. Write files (from templates/, fill every placeholder)
- `profile.md` from `templates/profile.md`: facts (never inflated), preferences, hard lines.
- `outreach.md` from `templates/outreach.md`: only the pre-approved action types they picked.
- `config.json`: `{"deadline": "YYYY-MM-DD" | null, "patrol_times": [...], "channels": [...]}`
- `.agent-memory/` from `templates/agent-memory/` (INDEX.md, handoff.md, decisions/, findings/).
- If patrol was requested: copy `templates/patrol-brief.md` to `briefs/patrol/<channel>.md` per
  channel, then run `bin/schedule.sh install`.
- If the user wants a private git history for their data, this repo's `.gitignore` already
  excludes it; suggest a separate private repo instead of un-ignoring.

## 4. Finish
- `python3 bin/jt.py check && python3 bin/jt.py board`
- Show: what was created, what is optional and skipped, and the first suggested move (usually:
  "run a scout on <best channel>").
