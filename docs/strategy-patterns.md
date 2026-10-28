# Optional strategy patterns

These are hypotheses to adapt to `profile.md` and the user's own outcomes, not universal hiring
rules. Review them weekly; never override hard lines or invent experience to improve a funnel.

## Two routes: conventional channels and direct engineering contact
Keep a conventional route for screened job boards, recruiters, referrals and suitable company
sites. Alongside it, try public hiring posts from engineering leads or teams willing to review
work directly. Use one relevant project and an approved portfolio link (T1b), rather than a
keyword-heavy pitch. Direct contact can bypass an HR screen; it does not bypass approval or
create permission to scrape private contacts. Recruiter and inbound messages deserve timely
triage before launching another wide search.

## Prefer Mid-level cold applications when the profile fits
For a candidate whose verified experience fits Mid-level work, prioritize those openings in
cold applications. Consider Senior only when the responsibilities and evidence support it;
otherwise keep it as `maybe` and spell out the gap. Job titles and years can be imperfect signals.
The level policy belongs in the user's profile; this is not a ban on senior candidates or roles.

## Filter working conditions, not company labels
Choose evidence of reasonable planning, individual boundaries, clear employment arrangements
and respectful collaboration. An international company label is not proof of these conditions;
a local company label is not proof against them. Record what is observed and what is unknown.
If public evidence is thin, prepare questions for an authorized conversation instead of inventing
certainty. The profile decides which unknowns are acceptable.

## Keep a decision pool
Use `seen_jobs` with `verdict=maybe` for promising roles needing a decision: level gaps, uncertain
work conditions, unclear remote eligibility or possible same-company overlap. Give each a reason
and a next question. `jt status --full` and the board expose this pool. The lead agent reviews it
before any application; it must not silently become an auto-apply queue.

## Let source cohorts decide which searches are worth running
Run `python3 bin/jt.py funnel --by source` for all time and with `--since YYYY-MM-DD` for comparable
application cohorts. Also inspect `--by platform`: platform is where the application happened;
source is how the opportunity was found. For example, a Pirate finding applied through an ATS
keeps `platform=ats` and `source=pirate`.

Use `scout`, `pirate`, `recruiter`, `inbound`, `referral`, `self` or `other` consistently; preserve
missing legacy values as `(unrecorded)`. `recruiter` means recruiter-sourced, while `inbound` is
an employer contacting the candidate directly. Record the first human reply and first interview
or phone screen; later rejection does not erase those events. The funnel counts applications
with a recorded milestone, not every interview round. Automated acknowledgments do not count.

Compare reply/interview yield with time spent, sample size, missing source data and how long
applications have had to mature. A low recent reply rate alone does not prove a route failed.
Reduce repeated low-yield searches; test a narrower route, better fit or a different outreach
approach, then measure again. Pirate discovery can be occasional rather than daily. Propose no
more than three adjustments per weekly review, each with evidence and a follow-up date.
