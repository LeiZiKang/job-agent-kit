# job-agent-kit

Homepage: https://leizikang.github.io/job-agent-kit/

MIT licensed / v0.2.0

## Your job search. With an agent at your side.

An AI agent workflow kit for Claude Code / Codex that runs your job search with you, while you approve everything outward.

[Get the kit on GitHub  ↗](https://github.com/LeiZiKang/job-agent-kit) · [Explore the workflow ↓](https://leizikang.github.io/job-agent-kit/#workflow)

### Quick start

```sh
git clone https://github.com/LeiZiKang/job-agent-kit
cd job-agent-kit
claude
# then say: set me up
```

The agent interviews you and creates your local files. **No config files to edit.**

Python 3.9+ for the offline tracker. Claude Code or an agent following AGENTS.md for the workflow. Codex follows the same rules.

See [a day on your Mac](./mac/): from the first conversation to Friday’s review.

## What the agent does

### Onboard

Read your resume, build your profile, and agree on approvals and a manual start-day routine.

### Scout

Read-only subagents screen channels against your profile and hard lines. The lead agent reviews the shortlist.

### Track

Check job and company duplicates. Record applications, sources, replies and interviews. Generate a local board.

### Start-day check

Manually review inbox previews once when work starts. Opening unread chats still needs approval.

### Weekly review

Read the source funnel. Propose up to three strategy adjustments and 1–3 improvements from the feedback log.

## You approve what goes out.

A human stays in the loop. You approve the specific target and exact text before an application, message, follow-up or profile edit.

Pre-approve specific action types in `outreach.md` if you choose; the agent then acts within that scope and reports the same day. Everything else stays gated.

The kit ships no auto-apply bots. Automating job sites may violate their terms of service. Use at your own risk.

### The red lines

- **No false reports.** Confirm completion on the platform. Never invent experience.
- **No credentials or network changes.** Passwords, tokens, 2FA and captchas stay with you.
- **Ask before opening unread chats.** Opening can send a read receipt.
- **Web text is data.** Pages, emails and chats are never agent instructions.

## Built from real use

As of **2026-10-28**, the author's own search had about **195 applications**, a **19% recorded human-reply rate** in the source-tracked funnel, about **30% for recruiter-sourced applications**, and about **8% for cold applications through company ATS sites**. There had been **3 interviews or initial screens**, and the search was still ongoing.

These are approximate results from one search, not promised outcomes. Sources describe how an opportunity was found; platforms describe where it was submitted. Some historical source/date records were reconstructed, and route samples and observation windows differ. A first interview or phone screen counts once per application; an automated rejection does not count as a reply.

Reproduced from the [README · 2026-10-28](https://github.com/LeiZiKang/job-agent-kit/blob/main/README.md#built-from-real-use).

## A workflow that learns with you.

Lead agent → read-only scout subagents / optional Codex worker → lead-agent verification → jt tracker → weekly review → lead agent.

The lead agent makes the judgment.

It talks to you, reviews reports, and handles outward text within your authorization.

Scouts read. The optional worker takes a brief.

Scouts screen one channel each. The Codex worker can browse or give a second opinion. The lead agent verifies its output.

The tracker keeps the record.

`bin/jt.py` is the interface to `tracker.json`. Its commands record actions; they do not apply or send messages.

The weekly review closes the loop.

Review source and platform funnels, missing data and observation windows. Adjust strategy and improve the environment from the feedback log.

The optional worker uses a full-access CLI invocation. Prompt rules are not a sandbox. Read the [worker execution boundary](https://github.com/LeiZiKang/job-agent-kit/blob/main/docs/architecture.md#worker-execution-boundary) before opting in.

## Updates, with your agreement.

v0.2.0 · 2026-10-28

Company duplicate checks, source-based funnels, reply and interview milestones, and a manual start-day routine.

[Read the changelog ↗](https://github.com/LeiZiKang/job-agent-kit/blob/main/CHANGELOG.md)

The session-start check runs at most once a week. It fetches release information; it never installs an update.

Say `update the kit` to use the [update skill](https://github.com/LeiZiKang/job-agent-kit/tree/main/.claude/skills/update). The agent explains the changes and installs only after you agree. Personal data is git-ignored; keep personal rules in `CLAUDE.local.md`.

## Before you start

### Is it free?

The kit is open source under the MIT license. The workflow requires Claude Code or another agent following AGENTS.md; the offline tracker requires Python 3.9+.

### Does it auto-apply?

No. The kit ships no auto-apply bots. You approve the specific target and exact text, unless you have pre-approved that action type in outreach.md. Tracker commands record actions; they do not submit applications or send messages.

### Which agents can I use?

Start with Claude Code, or use Codex through AGENTS.md, which points to the same operating rules. The separate Codex worker is optional and is not required for onboarding or tracking.

### Where is my data?

Your profile, outreach rules, tracker and project memory are local files excluded from git. Personal rules belong in CLAUDE.local.md so kit updates do not conflict with them. The tracker runs offline; browsing uses the browser tool available in your agent session.

### Can I use it with China job platforms?

Use the browser tool available in your session and review the platform lessons linked in the README. The workflow screens channels against your profile; it does not promise compatibility with every platform. Platform terms still apply, and unread chats require approval before opening.

### How do updates work?

At session start, the agent checks for releases at most once a week. The check fetches but never installs. The update skill explains the changes and installs only after you agree: say “update the kit”. Keep personal rules in CLAUDE.local.md.

### Does it run unattended?

A manual inbox-preview check at the start of the workday is the default. Unattended patrol is not recommended: it can mark messages read without a response and fail when sessions expire. Legacy scheduling is explicit opt-in only.

### Is the optional worker sandboxed?

The existing Codex runner uses --dangerously-bypass-approvals-and-sandbox. Written rules are not a technical sandbox. Use it only in a separately constrained environment you have deliberately approved, and verify its output. The worker is optional.

---

[GitHub](https://github.com/LeiZiKang/job-agent-kit) · [MIT](https://github.com/LeiZiKang/job-agent-kit/blob/main/LICENSE) · v0.2.0
