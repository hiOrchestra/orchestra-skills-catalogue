---
name: policy-handbook
version: 0.1.0
description: >-
  Build and keep the company's people handbook — time off, working hours and
  remote work, expenses and travel, equipment, benefits, conduct, how to
  raise a concern — from the policies and practices the business already
  has, one short section per topic, each with its source and the date it was
  approved, and answer employees' questions from it. Use when the user says
  "employee handbook", "HR policies", "write our time-off policy", "what is
  our policy on", "people handbook", "update the remote work policy". Not
  for handling a specific employee request (employee-requests) or for
  anything that needs an employment lawyer.
metadata:
  openclaw:
    emoji: "📘"
---
# Policy Handbook — how things work here, written once and kept true

People ask the same questions — how many days off, can I work from abroad,
what can I expense — and get different answers depending on whom they ask.
This skill writes the handbook from what the business already does, flags
where practice and paper disagree, and answers questions from it so the
answer is the same for everyone.

## Related skills
- **employee-requests** — applies the handbook to one person's request.
- **onboarding-plan** — the handbook is part of a new hire's first week.
- **distill** — a long legal policy turned into a readable section.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Writing or updating policies; answering "what is our policy on …".
- **Do NOT use** to decide what the law requires in a country — statutory
  minimums (leave, notice, overtime) are checked with an employment lawyer
  or the local authority, and the handbook says where that check stands.

## Workflow
1. **Collect what exists**: contracts' standard terms, existing policy
   documents, emails where a rule was announced, how things are actually
   done ("everyone takes the week between Christmas and New Year").
2. **Topics**: list the sections the business needs for its size and
   countries, starting from the questions people actually ask.
3. **Draft each section**: the rule in the first two lines, how to apply it,
   who approves, exceptions, the source, the approval date. Mark where
   practice and documents disagree, and where a statutory minimum applies
   and has not been checked.
4. **Review**: sections go to the person for approval; only approved ones
   are used to answer employees. Store in `orch-database` (table
   `policies`: topic, text, source, approved_by, approved_at, countries,
   status) and the full handbook in `orch-files` or `orch-docs`.
5. **Answer questions** from approved sections, quoting them; a question the
   handbook does not cover goes to the person, and the answer becomes a
   draft section.
6. **Keep it current**: when a rule changes, update the section, note the
   date, and say who should be told.

## Standards
- Same question, same answer, for everyone.
- Every section has a source and an approval date; drafts are never
  presented as policy.
- Plain language; a rule a new hire cannot understand is not a rule.
- Never present the handbook as legal advice or as compliant with a law.

## Output
For a draft: the sections, each with status and open questions. For a
question: the answer, the section quoted, and the date it was approved.

## Defaults
- Country unknown → ask; a rule differs by country more often than not.
- No written source → write the practice the person describes and mark it
  "as practised, to approve".
