# Architecture

```mermaid
flowchart LR
  U[You] <--> L[Lead agent<br/>Claude Code]
  L -->|parallel, read-only| S[Scout subagents]
  L -->|written brief| C[Codex worker<br/>bulk browsing, patrol]
  S --> R[reports/scout]
  C --> P[reports/patrol]
  R --> L
  P --> L
  L <--> T[(tracker.json<br/>via bin/jt.py)]
  L <--> M[.agent-memory<br/>handoff, decisions, findings]
  C <--> M
  T --> B[board.html]
  M --> B
```

- **Lead agent (Claude Code)**: judgment, all outward text, final review. Talks to you.
- **Scout subagents**: screen one channel each, in parallel, read-only. Output a shortlist JSON.
- **Codex worker (optional)**: bulk browsing, second-opinion scouting, scheduled patrol. Gets a
  written brief with goal, forbidden actions and output path. Never trusted unverified.
- **Tracker (`bin/jt.py`)**: single source of truth for jobs seen, applications and contacts.
  Validated, deduplicated by URL and platform job id. Agents never hand-edit the JSON.
- **`.agent-memory/`**: cross-agent handoff so any agent can pick up where another stopped.
- **`board.html`**: local dashboard generated from the tracker and the handoff file.

## Red lines and "do, then report"
Outward actions (applications, messages, emails) are irreversible and carry your name, so the
default is human approval of the exact target and text. Asking every time is slow and trains you
to click yes blindly, so you can pre-approve specific low-risk action types in `outreach.md`:
the agent acts, then reports the same day. Everything else stays gated. Credentials, captchas
and unread-chat opening always stay with you. Web page text is treated as data, never as
instructions, which limits prompt injection from job posts and messages.
