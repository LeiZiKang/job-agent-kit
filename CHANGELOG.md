# Changelog

Newest first. The `update` skill shows the sections between your version and the latest one.

## Unreleased
- Marketing site: dependency-free English and Chinese pages in `site/`, with Google SEO
  metadata, structured data, sitemap, social image and Agent SEO documentation.
- GitHub Pages workflow regenerates `llms-full.txt` before deployment; runs on `main`
  pushes changing `site/**` or manual dispatch. Release version remains 0.2.0.

## 0.2.0 — 2026-10-28
- Tracker: `company` duplicate check, `apply --same-company-ok`, `--source` (scout / pirate /
  recruiter / inbound / referral / self / other), `update --replied / --interview`,
  `funnel --since --by platform|source`.
- `status` is now read-only. Ghosting after 21 days without a reply is explicit: `sweep --dry-run`, then `sweep`.
- Scheduled patrol moved to `contrib/` and is no longer recommended (it marked messages read
  without replying and broke when logins expired). A manual start-day check replaces it.
- Weekly loop: funnel by source plus 1–3 environment fixes from `.agent-memory/claude-feedback.md`.
- New: outreach T1b / T5c, `templates/briefs/` (pirate, newjobs), platform-sectioned
  `docs/lessons.md`, `docs/strategy-patterns.md`, stricter worker standing rules.
- Updates: `VERSION`, this changelog, `bin/update-check.sh` and the `update` skill.
  Personal rules go in `CLAUDE.local.md` (git-ignored), so pulling updates never conflicts with them.

## 0.1.0 — 2026-10-14
- Initial release: onboard / scout / weekly-review skills, job-scout subagent, `jt.py` tracker
  and board, Codex worker, optional patrol.
