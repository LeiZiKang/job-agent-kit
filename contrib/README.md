# Legacy patrol (opt-in, not recommended by default)

The author stopped unattended scheduled patrol after real use: opening chats could mark messages
read without a reply, and login sessions expired while nobody was present. The current workflow
is one manual inbox preview check at the start of each workday. Do not open unread conversations
without authorization, even during a manual check.

These macOS-only scripts are retained for users who explicitly choose to maintain a schedule:
- `contrib/patrol.sh`: runs `briefs/patrol/*.md` through the optional Codex worker and extracts
  `## Changes` into `reports/patrol/<date>.md`. Worker output is unverified.
- `contrib/schedule.sh install|uninstall|status`: manages the launchd schedule using optional
  `patrol_times` in local `config.json`, such as `["10:30"]`. Run only after explicit approval
  to install/change a schedule. Moving the script does not migrate an already-installed job;
  its saved path needs updating through an approved reinstall.

Copy `templates/patrol-brief.md` into local `briefs/patrol/<channel>.md`, fill every placeholder,
and review read-receipt behavior before opting in. Requires macOS, zsh, Python, Perl, Codex CLI
and an awake, unlocked session. Do not treat a missing result or expired login as “no messages”.
See [the worker execution boundary](../docs/architecture.md#worker-execution-boundary).
