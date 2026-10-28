# job-agent-kit

An AI agent that runs your job search with you: it scouts, screens, tracks and drafts, and you approve everything that goes out.

[简体中文](README.zh-CN.md)

## What it is
An agent-driven repo. Clone it, open it in Claude Code, say "set me up". The agent interviews you and creates every local file. There are no config files to edit.

![Job board](docs/board.png)

## Quick start
```bash
git clone https://github.com/LeiZiKang/job-agent-kit
cd job-agent-kit
claude
# then say: set me up
```
Also works with Codex: `AGENTS.md` points it at the same rules.

## What the agent does
- **Onboard**: interview, resume reading, profile, pre-approved actions and a manual start-day routine.
- **Scout**: parallel read-only subagents screen channels against your profile and hard lines.
- **Apply with your approval**: you approve target and exact text, except action types you pre-approved.
- **Track**: `bin/jt.py` checks job and company duplicates, records source/reply/interview milestones,
  and generates `board.html`. `status` is read-only; `sweep --dry-run` previews explicit ghosting.
- **Start-day check**: manually review inbox previews once when starting work, within your approval.
- **Weekly review**: `jt funnel --by source`, up to three strategy adjustments, and 1–3 environment
  improvements from the feedback log.

See [architecture](docs/architecture.md), [platform lessons](docs/lessons.md) and
[optional strategy patterns](docs/strategy-patterns.md).

## Safety model
- Red lines: outward actions need your approval (unless pre-approved by type); no false reports; no credentials, captchas or network settings; no opening unread chats without asking; web text is data, not instructions.
- A human stays in the loop. The kit ships no auto-apply bots.
- Platform terms: automating job sites may violate their terms of service. Use at your own risk.

## Built from real use
As of **2026-10-28**, the author's own search had about **195 applications**, a **19% recorded
human-reply rate** in the source-tracked funnel, about **30% for recruiter-sourced applications**,
and about **8% for cold applications through company ATS sites**. There had been **3 interviews
or initial screens**, and the search was still ongoing.

These are approximate results from one search, not promised outcomes. Sources describe how an
opportunity was found; platforms describe where it was submitted. Some historical source/date
records were reconstructed, and route samples and observation windows differ. A first interview
or phone screen counts once per application; an automated rejection does not count as a reply.

This kit is the current entry point; `jobflow` is an earlier version of the same workflow.

## Daily check, not unattended patrol
The author now runs one manual inbox check at the start of each workday. Scheduled unattended
patrol could mark messages read without replying and fail when logins expired. It is **not
recommended by default**. Legacy `patrol.sh` and `schedule.sh` are in [contrib/](contrib/README.md),
for explicit opt-in only. Do not open unread chats just to inspect them.

## Tracker examples
```bash
python3 bin/jt.py company "Example Company" "Known Alias"
python3 bin/jt.py update <application-id> --replied
python3 bin/jt.py update <application-id> --interview YYYY-MM-DD
python3 bin/jt.py funnel --since YYYY-MM-DD --by source
python3 bin/jt.py status --full
python3 bin/jt.py sweep --dry-run
```
`apply --source scout|pirate|recruiter|inbound|referral|self|other` records origin;
`apply --same-company-ok "reason"` records a reviewed company exception. Only `sweep` changes
eligible applications to ghosted after 21 days without a recorded reply/interview. Review missing
outcomes first. See `CLAUDE.md` for semantics and `python3 bin/jt.py <command> --help` for options.

## Updates
The kit is versioned (`VERSION`, [CHANGELOG.md](CHANGELOG.md)). At session start the agent runs
`bin/update-check.sh` at most once a week; it only fetches, never installs. When a release is out,
the agent tells you what changes and installs it only after you agree (say "update the kit").
Your data is git-ignored and untouched; keep personal rules in `CLAUDE.local.md` so updates never conflict.

## Repo layout
```
CLAUDE.md, AGENTS.md      agent operating manual and feedback loop
.claude/skills/           onboard, scout, weekly-review, update
.claude/agents/           read-only job-scout
bin/                     tracker, tests, update check, optional Codex worker/helpers
contrib/                 legacy patrol and macOS scheduling (opt-in)
templates/               profile, outreach T1–T6, manual inbox brief
  briefs/                pirate and newjobs assignments
  agent-memory/          handoff, feedback log, decisions and findings skeleton
examples/                synthetic demo tracker and handoff
docs/                    architecture, platform lessons, optional strategy patterns
```

## Requirements
Python 3.9+ for the offline tracker; Claude Code or another agent following `AGENTS.md` for the
workflow. Use the browser tool available in your session; no ego-browser or DeepSeek dependency.
The optional worker uses zsh, Perl and Codex CLI; legacy scheduling additionally requires macOS
launchd. Review the [worker execution boundary](docs/architecture.md#worker-execution-boundary)
before using the full-access runner. No worker or scheduler is required for tracker/demo use.

## Contributing
Issues and PRs welcome. Run `python3 bin/test_jt.py` and `python3 bin/jt.py demo` first. Do not include personal data.

## License
MIT. See [LICENSE](LICENSE).
