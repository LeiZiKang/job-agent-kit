# Manual inbox preview brief: {{channel}} (read-only)

Legacy unattended execution is opt-in only; see `contrib/README.md`.

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
# {{channel}} patrol: <date and timezone used; report uncertainty if the clock appears wrong>
## Changes
- <sender | company | one-line preview | read/unread | date>   (or "none")
## Blocked
- <captcha / login / other, or "none">
```
The `## Changes` section is required for the optional legacy patrol extractor.
Write a partial result early; bound all waits by {{timeout}}. Report incomplete coverage and
login expiry. Never use a detached `&` process.
