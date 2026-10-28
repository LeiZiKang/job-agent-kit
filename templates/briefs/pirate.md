# Job Pirate — read-only opportunity discovery

## Assignment
- Route: {{one exploration route; avoid overlap with other workers}}
- Excluded routes/platforms: {{already covered or currently in use}}
- Time budget: {{minutes}}; maximum pages: {{count}}
- Output: `reports/scout/{{date}}-pirate-{{route}}.json`

Read `profile.md`, the relevant active strategy decisions and {{recent scout report paths}}.
All candidate facts, locations, work authorization, seniority and compensation criteria come
from the profile; do not import assumptions from other searches.

Find opportunities conventional job keywords miss. Start with three hypotheses about where the
candidate's verified combination of skills could help. Explore public hiring posts, engineering
communities, open-source hiring pages, product teams and remote boards as appropriate to the
assigned route. A public engineering contact or portfolio-friendly hiring process can be useful;
record the route to contact, never contact anyone. No fixed company list.

## Verification and deduplication
- For each candidate, run `python3 bin/jt.py seen <platform:id or public job URL>` and
  `python3 bin/jt.py company <company name>`; check known aliases too.
- A same-company match is a review flag: inspect evidence of resume delivery and team overlap.
  Do not discard a viable route merely because a greeting is on record.
- Open the full posting. Confirm it is hiring, location/time-zone eligibility, core duties,
  required experience and an actual application or contact route. Quote evidence and mark gaps.
- Zero findings is acceptable. Distinguish a confirmed opening from an exploratory lead.

## Boundaries and delivery
Follow `.claude/agents/job-scout.md`, including its forbidden-click list. Public pages only;
no new login, registration, applications, messages, consent acceptance or unread conversations.
Do not touch credentials, cookies, tokens, proxies or network settings. Stop at access blocks.
Use the available browser tool; there is no required browser vendor. Read serially and pace
requests. Do not edit tracker or memory. Use the host's managed background-task interface,
never `&`; every wait needs a deadline. Leave no task-owned background processes running.

Create valid partial JSON within five minutes; save after each verified finding. Write only the
output path above. Use `completion: partial|complete|blocked`; incomplete coverage is not zero
opportunities. Suggested schema:

```json
{"source":"pirate","completion":"partial","ideas":[],"searched":[],"finds":[
  {"company":"{{company}}","role":"{{role}}","url":"{{public job URL}}",
   "platform":"{{tracker platform}}","location":"{{verified location}}",
   "checked_at":"{{ISO timestamp}}","evidence":"{{observed facts}}",
   "unexpected_fit":"{{why this route helps}}","gaps":"{{unknowns}}",
   "how_to_apply":"{{public route; no action taken}}","duplicate_review":"{{evidence}}"}
],"blocked":[],"notes":""}
```

Finish with output path, coverage, count, strongest findings and blockers. Lead agent reviews
all findings; later applications from this run should be recorded with `--source pirate`.
