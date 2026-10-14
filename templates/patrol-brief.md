# Patrol brief: {{channel}} (read-only)

## Goal
Check the inbox/messages of {{channel}} (already logged in, in the browser) for changes since the
last run: new messages, replies, interview invites, rejections. Use list views and previews only.
Do NOT open unread chats (recruiters would see "read"). Compare with the previous result file if
it exists.

## Forbidden
- Sending, replying, applying, clicking chat/greet buttons, editing profile or settings.
- Opening unread conversations; accepting terms; touching passwords, 2FA or captchas.
- On a captcha, login wall or lock screen: stop and report it.
- Proxy or network settings.

## Working style
One tool call per screen; avoid many tiny steps.

## Output
Write `reports/patrol/{{channel}}-result.md`:

```
# {{channel}} patrol: <date from network, not local clock>
## Changes
- <sender | company | one-line preview | read/unread | date>   (or "none")
## Blocked
- <captcha / login / other, or "none">
```
The `## Changes` section is required; the scheduler extracts it.
