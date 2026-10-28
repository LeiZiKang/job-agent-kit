# Lessons from real use

These are observations from the author's workflow through 2026-10-28, not permanent platform
contracts or safe request-rate guarantees. Verify the visible UI before an authorized action.
Criteria and candidate facts belong in `profile.md`; these notes describe operational pitfalls.

## General
- **A greeting is not resume delivery.** Check both `jt seen` and `jt company`, then read status
  and evidence. A company appearing in the tracker does not prove its recruiter has the resume.
  Review aliases, client names and team overlap before blocking another route or recording a
  reason with `apply --same-company-ok`.
- **Confirm completion.** Consent screens and uploaded attachments are intermediate steps.
  Record submission only after a confirmation page or equivalent evidence; inspect ATS-parsed
  employers, dates and titles before submission.
- **Record outcomes where the funnel reads them.** Human replies go in `update --replied`;
  interviews and phone screens in `update --interview`. Automated acknowledgments/rejections
  are not human replies. A rejection after a real exchange can have both reply and rejection data.
- **Do not act on stale inbox reports.** The user may have replied from a phone. Before reporting
  a message as pending, check current previews or the conversation only within its authorization.
  Keep live observations separate from old evidence; record unknown dates as unknown, not today.
- **Opening is an outward effect.** Unread chats and invitations may send read receipts. The
  author stopped unattended scheduled patrol and checks manually at the start of the workday:
  unattended runs could mark messages read without replying and lose login sessions.
- **Screen the environment with evidence.** An employer category or a benefits tag does not
  prove reasonable hours. Distinguish positive evidence, negative evidence and unknowns. Apply
  the user's policy for unknowns from `profile.md`; clarify the actual employer/client relationship.
- **Keep decisions visible.** Rewrite the current handoff rather than appending a diary. Record
  friction in `claude-feedback.md`; improve the environment weekly. Answer all user questions
  before closing a phase, and maintain reasoned recommendations unless new evidence changes them.

## BOSS 直聘
- A scout once opened an empty recruiter conversation by clicking “立即沟通”. Its brief must
  explicitly prohibit that action: scouts only navigate to `job_detail` pages and read text,
  with **no button clicks**. “Read-only” alone is too vague.
- Opening a chat and delivering a resume are separate steps; attachment sending may be unavailable
  until a reply. Record the observed result rather than inferring delivery from the button name.
- Company abbreviations and local-language names can return different results. Check aliases,
  city fallback and ads; a matching keyword in the list is not proof that the core role fits.
- Serial reads with pauses reduce avoidable load but do not guarantee exemption from rate limits.
  Do not use concurrent workers on the same account/platform or probe limits through hidden APIs.

## 猎聘
- Clicking “聊一聊 / 继续聊” on a job page has automatically sent a message in the user's name.
  Treat it as a send action, not navigation; scouts never click it.
- Accepting an invitation and submitting a resume has also sent platform-generated greetings.
  Approval must cover those effects. An online-resume card is not proof the attachment was sent.
- Reading many JDs and batch-applying in the **same hour** triggered a captcha in actual use.
  Separate search and application sessions; avoid parallel tabs. Even list-only searches have
  triggered verification. There is no demonstrated safe quota; stop the batch on the first block.
- Resume synchronization can misparse work history. Do not click “sync attachment to online
  resume” as routine maintenance. A web placeholder saying content is app-only does not establish
  who sent it or whether it is an advertisement; verify before reporting an outbound message.

## LinkedIn
- Invitation-note lengths and quotas depend on the account and UI. Read the displayed allowance;
  do not hardcode historical limits or work around exhausted quotas.
- A connection request is not an application, referral or accepted connection. Confirm each state.
  Send T5c at most once after acceptance and only within its approved scope; if no application
  exists, use an approved T1b message without claiming to have applied.
- Keep search, invitations and follow-up messages separate in reports and evidence. A sent request
  must not be counted as a human reply in the application funnel.

## 脉脉
- Opening invitation cards can mark them read. Preview lists first; do not open unread cards for
  scouting unless authorized and the user is ready to respond.
- On some invitation cards, “同意” sends the resume before messaging becomes available. It is
  not a harmless way to ask who the client is. “感兴趣” can also submit an application; scouts
  never click it. Some “立即沟通” buttons lead to membership purchase rather than a free chat.
- After an action, the detail view may move to another job. Reconfirm the target before any
  further authorized action. Search and chat capabilities differ between web and app, and rate
  limits may affect both. Do not change accounts or settings to get around a block.

## Workers
- Use a written brief with one route, budget, prohibited actions and exact output path. Keep
  screening criteria in `profile.md`, not duplicated personal facts in each worker prompt.
- Use the host's managed background-task facility (for example `run_in_background`), never bare
  `&`. Detached work has finished without a completion notification and its results were missed.
  Every polling loop and background wait needs a deadline; clean up task-owned processes.
- Create a valid partial result early, save each verified finding, and report incomplete coverage.
  A timeout or missing file is not evidence that no suitable jobs exist.
- Re-read current result files before final review; a startup handoff snapshot can miss work
  completed during the session. Check worker evidence before claiming anything to the user.
- Stop and re-brief a worker that goes off track. A fixed prompt is an instruction boundary,
  not a technical sandbox. The legacy runner currently retains its full-access CLI option;
  see [architecture](architecture.md#worker-execution-boundary) before opting in.
