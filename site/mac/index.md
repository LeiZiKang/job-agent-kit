# A day in the desktop app — job-agent-kit

Webpage：https://leizikang.github.io/job-agent-kit/mac/

Explore job-agent-kit in an illustrative desktop app on your Mac: conversations, read-only scouts, message approvals, a local board preview and weekly review. Fictional demo data, not screenshots.

> Illustrative desktop app interface, not screenshots. Your app may look different as it updates. Conversations, companies, session names and job records are fictional examples, not live account activity.

Six scenes share a fixed dark, four-column app window: project/session sidebar, board or JSON preview, conversation with a decision card, and task/environment sidebar. Narrow screens hide the information sidebar, then the preview. Phones show only the top bar and conversation; the Track scene shows the board instead. Buttons are static illustrations. Board and funnel figures are labeled DEMO DATA.

## 1. Morning: Start the day.

```text
You › start the day
Read .agent-memory/handoff.md
Bash jt status → python3 bin/jt.py status
```

The agent reads the handoff and tracker, then highlights three priorities: review Fabrikam’s salary reply, clarify Northwind’s contract / direct-hire question before interview prep, and approve the Proseware draft. Pending items must be refreshed in a real session. One manual inbox-preview check follows; opening unread chats needs approval.

## 2. Scout: three channels, one shortlist.

The lead agent sends one read-only job-scout per channel: LinkedIn, Indeed and company ATS. Each returns reports/scout/<date>-<channel>.json. The lead verifies full job descriptions and checks jt seen / jt company before recording decisions. Scouts never apply or send messages.

Abbreviated JSON illustration using a candidate from examples/tracker.json:

```json
{"channel":"linkedin","source":"scout","shortlist":[{"company":"Alpine Ski House","role":"Senior React Engineer","verdict":"recommend"}]}
```

## 3. You approve: target and exact text.

T2 · First reply to an inbound recruiter. To: Example Co. recruiting team, via email.

> Hi Example Co. recruiting team, thanks for reaching out about the Frontend Engineer role. Could you share the company or client, team size and working arrangement? Happy to share my resume if there is a fit.

```text
Decision card › Send this exact text to this recipient?
Primary button › Yes, send it (illustrative, not clicked)
```

This is a template illustration with a placeholder company and no personal claims. Approval is for that target and exact text; verify delivery before reporting it sent. Specific action types can also be pre-approved in outreach.md.

## 4. Track: a local board.

The HTML page shows a scrollable board in a wider preview panel: a statistics card, Up next, a Where it drops off funnel, recommendations, the maybe pool and all application records. All records come from examples/tracker.json.

| Metric | Demo count |
| --- | ---: |
| Records (includes a draft) | 8 |
| Recorded replies | 3 |
| Recorded interviews | 1 |
| Waiting | 2 |
| Interviewing status | 1 |
| Recommended | 2 |
| Maybe | 2 |
| Active / total records | 6 / 8 |

| Company | Role | Status |
| --- | --- | --- |
| Northwind | Senior Frontend Engineer | interviewing |
| Proseware | Senior Software Engineer | preparing |
| Litware | UI Engineer | submitted |
| Adatum | Staff Engineer | submitted |
| Fabrikam | Full-stack Engineer | submitted |
| Contoso Mobile | iOS Engineer | submitted |
| Tailspin Toys | Web Platform Engineer | rejected |
| Wingtip | Frontend Engineer | ghosted |

Recommended: Alpine Ski House (Senior React Engineer) and Coho Winery (Frontend Lead). Maybe: Woodgrove and Lucerne. Tracker commands only record actions; they do not apply or send.

## 5. Friday review: learn and adjust.

```text
python3 bin/jt.py funnel --by source
Source            Applied  Replied  Reply rate  Interviews  Rejected
scout                   4        0          0%           0         1
recruiter               2        2        100%           1         0
referral                1        1        100%           0         0
self                    1        0          0%           0         0
Total                   8        3         38%           1         1
```

Demo data, not an outcome claim; very small sample. 8 records include 1 draft, with 3 replies and 1 interview. Reply rate: 37.5% (CLI rounds to 38%); interviews / records: 12.5%; reply → interview: 33.3%. Source and platform are different.

1. Continue recruiter follow-ups.Both submitted recruiter records have replies, with 1 interview; the sample is only 2.
2. Review scout fit and the draft.4 scout records include 1 unsent draft and have 0 recorded replies; review the draft and job fit first.
3. Compare like-aged cohorts.Check --since and --by platform; referral has 1 reply from 1 record, self has 0 from 1. Reassess next Friday.

## 6. Stays up to date.

```text
Bash update-check.sh → bin/update-check.sh
Illustrative notice: new version available. Nothing installed.
Decision card › Install v0.x? (placeholder, not a live release)
```

This is not a live release check. At session start, updates are checked at most weekly. The agent explains the changes and installs only after agreement. Personal rules stay in CLAUDE.local.md.

## Quick start

Install the [Claude desktop app](https://claude.ai/download) and open its Code tab, or use Claude Code. Paste this sentence to the agent:

> Install job-agent-kit for me: download https://github.com/LeiZiKang/job-agent-kit to my computer, read its INSTALL.md, and walk me through setup.

The agent reads INSTALL.md and guides setup, defaulting to `~/job-agent-kit`. It asks before installing Git or Python 3.9+ if needed.

[Developer manual installation](https://github.com/LeiZiKang/job-agent-kit/blob/main/README.md#developer-manual-installation)

The agent interviews you and creates local files. No config files to edit. Requires Python 3.9+ for the tracker and Claude Code or an agent following AGENTS.md. Codex follows the same rules.

[GitHub](https://github.com/LeiZiKang/job-agent-kit) · [Home](https://leizikang.github.io/job-agent-kit/) · [中文](https://leizikang.github.io/job-agent-kit/zh/mac/)
