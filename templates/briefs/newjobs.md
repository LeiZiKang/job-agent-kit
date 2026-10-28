# New jobs — read-only search since a cutoff

## Assignment
- Channel/route: {{channel and search scope}}
- Posted or updated on/after: {{YYYY-MM-DD}}
- Keywords: {{profile-derived keyword sets}}
- Excluded routes/platforms: {{already covered or assigned elsewhere}}
- Limits: {{JD budget}}, {{minutes}}
- Recent reports to dedupe against: {{paths}}
- Output: `reports/scout/{{date}}-newjobs-{{channel}}.json`

Read `profile.md` and relevant active strategy decisions. Use its facts, red lines and preferences
for locations, level, compensation, technical fit and work authorization. Search the assigned
route only; change keywords when a repeated approach has yielded nothing. No fixed company list.

## Verify every recommendation
1. Run `python3 bin/jt.py seen <platform:id or URL>` and `python3 bin/jt.py company <company>`.
   Check known aliases and recent reports. A company hit requires delivery/team review, not an
   automatic rejection or permission to reapply.
2. Read the full JD: still open, posted/updated date, location/remote eligibility, responsibilities,
   seniority and stack. A search-engine snippet date is not proof of posting date. If freshness
   cannot be established, put it under `uncertain` instead of claiming it is new.
3. Explain fit and gaps. Use `recommend` only when the profile's screening criteria are met;
   otherwise use `maybe` for lead review or list a rejection reason. Pick a resume variant only
   from the profile. Record how to apply without applying.

## Boundaries and delivery
Follow `.claude/agents/job-scout.md` and its explicit forbidden-click list. No applications,
messages, unread chats/invitations, registration, new logins or consent acceptance. BOSS: read
job_detail pages only, no buttons. One page per platform, serial reads with pauses; do not overlap
with another worker's search or application batch. Stop at captcha, login or account warnings.
No credentials, cookies, tokens, proxy or network changes. Use the session's available browser.
Write only the output file, not tracker or memory. Use managed background tasks rather than `&`;
every wait needs a timeout. Create valid partial JSON within five minutes and save incrementally.

```json
{"source":"scout","completion":"partial","searched":[],"read_count":0,"jobs":[
  {"company":"{{company}}","title":"{{role}}","platform":"{{tracker platform}}",
   "location":"{{verified location}}","url":"{{public job URL}}",
   "posted":"{{verified date}}","date_evidence":"{{page evidence}}",
   "verdict":"recommend","reason":"{{fit and gaps}}","resume":"{{profile variant}}",
   "how_to_apply":"{{route only}}","duplicate_review":"{{delivery evidence}}"}
],"uncertain":[],"rejected":[],"blocked":[]}
```

Set completion to `complete` or `blocked` when finished. Report output path, coverage, count,
top candidates and blockers. The lead agent reviews and records results; use `--source scout`
for applications originating from this task. Zero verified new jobs is a valid result.
