# Lessons from running this for real

- **Chat buttons send messages.** On some job platforms, clicking "chat" or "greet" auto-sends a
  greeting in your name. Scouts are read-only and never click them.
- **Separate search from apply.** Reading ~50 job descriptions plus batch-applying in one hour
  triggered captchas. Search in one pass, apply in another, and stop the batch on the first captcha.
- **Verify worker output.** Whatever a worker agent (Codex) produces, the lead agent checks before
  reporting it. Spot-check sources, ideally with a cheap model.
- **Slowness is context, not the web.** Workers were slow from many tiny steps that each re-read a
  big context. Ask for one call per screen.
- **Codex exec sessions can't be interrupted.** If one goes off track, stop it and re-brief.
- **Machine clocks can lag.** Verify the date from the network before writing dated reports.
- **"Read" is visible.** Recruiters see "read" when you open unread chats. Use list previews.
- **Resume parsers invent fields.** ATS auto-fill may add wrong titles or dates. Check every field
  before submitting.
- **Absence of evidence is not evidence.** "No 996 seen" does not mean good hours. Require
  positive evidence (stated hours, reviews, policies) before recommending.
- **Staffing agencies disguise contract roles.** Contract-through-agency postings often look like
  direct hires. Check who the employer of record is.
