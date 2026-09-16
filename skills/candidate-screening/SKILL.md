---
name: candidate-screening
version: 0.1.0
description: >-
  Screen applications against the role's must-haves — the same criteria for
  every candidate, evidence quoted from the CV or letter, a consistent score
  and a shortlist with the reason for each yes and no — without ever using
  anything that is not about doing the job. Use when the user says "screen
  these CVs", "shortlist", "who should we interview", "rank the applicants",
  "review these applications", "first pass on the candidates", or hands you
  résumés. Not for writing the role (job-description), interviewing
  (interview-guide) or the final choice (decision-brief).
metadata:
  openclaw:
    emoji: "🗂️"
---
# Candidate Screening — every applicant against the same bar, with the evidence

A screen is fair when every candidate is measured against the same written
criteria, and useful when every verdict shows its evidence. This skill takes
the role's must-haves, reads each application for evidence of them, scores
consistently, and produces a shortlist the hiring manager can defend — and
a courteous reason for every no.

## Related skills
- **job-description** — where the criteria come from; write it first if
  there is none.
- **interview-guide** — the next step for the shortlist.
- **decision-brief** — the final choice between finalists.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Applications have arrived and someone needs a first cut.
- **Do NOT use** age, gender, name origin, photo, nationality, family
  situation, health, gaps explained by any of these, or any proxy for them.
  If a criterion the person gives is one of these, refuse it in one line and
  screen on the job-related criteria only. Never rank on "culture fit"
  without a written, job-related definition.

## Workflow
1. **Fix the criteria before opening a CV.** From the job description: the
   must-haves (pass/fail) and up to five scored criteria with what evidence
   counts for each (a project, a result, a duration, a tool used in anger).
   Show the grid to the person for their yes.
2. **Read every application fully**, in the same order of criteria. For each
   criterion: met / partly / not / no evidence, with the line from the
   application that shows it, quoted.
3. **Score** — must-haves first; a missing must-have ends the screen for
   that candidate, stated as such. Then the scored criteria, same scale for
   all. No bonus for length, prestige of names, or polish of the document.
4. **Shortlist** — the candidates to interview, in order, each with the two
   strongest pieces of evidence and the one thing to probe in interview.
   For the rest, the criterion that decided it.
5. **Deliver** under Output, and hand the shortlist's open points to
   `interview-guide` if it is installed.

## Standards
- Same criteria, same order, same scale for everyone; a criterion added
  halfway is applied to all again.
- Every verdict quotes its evidence. "Seems senior" is not evidence.
- "No evidence" is not "does not have it": it is a question for the
  interview, and it is scored as unknown, not as zero, unless the criterion
  is a must-have.
- Candidates are named as in their application; nothing about them is
  inferred from the name, the photo or the address.
- The person makes the decision; the screen recommends and shows its work.

## Output
- **Criteria** — the grid used (must-haves, scored, evidence expected).
- **Shortlist** — ordered: name · score · two pieces of evidence · what to
  probe.
- **Not shortlisted** — name · the deciding criterion (one line each).
- **Notes** — anything that made the screen harder (unreadable files, a
  role that attracted the wrong profile) and what would fix it.
Saved to `orch-files` as `hiring/<role>/screen-<date>.md`; the table also as
a spreadsheet on request.

## Defaults
- No job description → ask for the three must-haves and screen on those
  only; say the grid is thin.
- Many applications → must-haves pass first, scored criteria on the passers.
- Ties → the candidate with more direct evidence on the highest-weighted
  criterion; say it was a tie.
