---
name: weekly-review
description: Weekly funnel review. Reads tracker.json and recent reports, measures applied → reply → screen → interview by channel, and proposes at most 3 strategy changes. Use on the user's review day or when asked "how is it going".
---

1. `python3 bin/jt.py status --full`, then compute from `tracker.json` for the last 7 days and
   all time: applications by platform, reply rate, screens, interviews, median days to reply.
2. Read `.agent-memory/handoff.md` and this week's `reports/` for context (channels tried, blockers).
3. Question the strategy, not just the numbers: which channel produced replies? Which preference
   in `profile.md` is filtering out most jobs? Is the resume version the bottleneck?
4. Output: a 5-line funnel table, then **at most 3** concrete changes with the evidence for each,
   then what the user must decide. Record accepted changes in `.agent-memory/decisions/`.
