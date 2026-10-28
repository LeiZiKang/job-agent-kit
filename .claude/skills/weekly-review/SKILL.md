---
name: weekly-review
description: Weekly funnel review. Reads tracker.json and recent reports, measures applied → reply → screen → interview by channel, and proposes at most 3 strategy changes. Use on the user's review day or when asked "how is it going".
---

1. Run `python3 bin/jt.py status --full`, `python3 bin/jt.py funnel --by source` and
   `python3 bin/jt.py funnel --by platform`, then repeat the funnels with `--since YYYY-MM-DD`
   for the chosen cohort (for example applications in the last seven days). Compare like-aged
   cohorts; note missing sources and reply/interview dates. Screens count with first interviews.
   Status is read-only; review missing replies before any explicit `sweep`.
2. Read `.agent-memory/handoff.md` and this week's `reports/` for context (channels tried, blockers).
3. Question the strategy, not just the numbers: which channel produced replies? Which preference
   in `profile.md` is filtering out most jobs? Is the resume version the bottleneck?
4. Output: a 5-line funnel table, then **at most 3** concrete changes with the evidence for each,
   then what the user must decide. Record accepted changes in `.agent-memory/decisions/`.

5. Read `.agent-memory/claude-feedback.md`; choose 1–3 actionable items when available and improve
   instructions, tools or work allocation within existing authorization. Record the change and
   validation beside each item; check last week's changes too. Do not invent work if the log is
   empty. Keep these environment improvements distinct from the at-most-three strategy changes.
