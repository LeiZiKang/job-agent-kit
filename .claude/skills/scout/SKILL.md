---
name: scout
description: Run a job-search sweep. Splits channels across job-scout subagents (and optionally a Codex second pass), then does the final review and records verdicts with jt.py. Use when the user asks to find jobs or the pipeline is empty.
---

1. Read `profile.md` and `config.json`. Pick 1-3 channels and 2-4 keyword sets based on what the
   last weekly review said works.
2. Launch one `job-scout` subagent per channel in parallel. Tell each: channel, keywords, output
   path `reports/scout/<date>-<channel>.json`, JD budget.
3. Optional second pass: write `briefs/scout-<channel>.md` and run `bin/codex-run.sh` in the
   background on a different channel or keyword set.
4. Final review is yours: re-open each shortlisted JD, check against `profile.md` hard lines,
   then `python3 bin/jt.py add-seen` every job (recommend / maybe / reject, with a one-line reason).
5. `python3 bin/jt.py board`. Report: N read, N recommended, top 3 with why, and what to apply to.
