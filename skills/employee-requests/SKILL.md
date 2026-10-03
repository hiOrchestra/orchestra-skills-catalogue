---
name: employee-requests
version: 0.1.0
description: >-
  Handle the everyday requests and questions employees bring to people ops —
  time off and its balance, a certificate or letter, a change of personal
  details, an expense or equipment question, "who do I ask about" — by
  applying the approved handbook, keeping a register of requests and
  balances, drafting the reply or the letter for the person's yes, and
  escalating what is sensitive. Use when the user says "log this time-off
  request", "how many days does X have left", "write an employment
  certificate", "an employee asked", "people requests", "leave tracker".
  Not for writing the policy itself (policy-handbook).
metadata:
  openclaw:
    emoji: "🙋"
---
# Employee Requests — every request answered the same way, and recorded

Small requests are where people ops earns trust: a day off approved quickly,
a certificate the same afternoon, the same answer for the same question. This
skill applies the approved handbook to each request, keeps the register and
the balances, drafts the reply, and knows which requests are not for an agent.

## Related skills
- **policy-handbook** — the rules every answer comes from.
- **action-tracker** — requests waiting on someone.
- **onboarding-plan** — when the request is a new joiner's.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Time off, letters and certificates, personal data changes, equipment,
  "how does X work here".
- **Escalate, never handle**: complaints or grievances, harassment or
  discrimination, health and medical matters beyond a sick day, pay
  disputes, disciplinary matters, resignations and dismissals, anything a
  person says in confidence. Say who it goes to and reply only with an
  acknowledgement the person approves.

## Workflow
1. **Register** the request in `orch-database` (table `people_requests`:
   id, employee, type, dates, details, status, decided_by, decided_at).
   For time off, keep balances in `leave_balances` (employee, year,
   entitled, taken, pending).
2. **Apply the handbook**: find the approved section; check eligibility,
   notice, balance, overlaps with others in the same team.
3. **Draft** the reply or the document (certificate, letter) from the
   approved template, with facts from the register only — never invented.
4. **Decision is the person's**: approvals and refusals are proposed with
   the reason and the section; recorded only after their yes.
5. **Tell** the employee (drafted, for the person's yes) and update the
   balance and the register.
6. **Weekly**: who is off next week, pending requests, balances that will
   be lost at year end.

## Standards
- Employee data is personal data: minimum needed, never shared beyond who
  must know, never discussed with other employees.
- Same rule for everyone; an exception is the person's call and is
  recorded as an exception.
- Letters state only verified facts from the register.

## Output
Per request: what was asked · the rule that applies · proposed decision and
reason · draft reply or document. Weekly: off next week, pending, balances
at risk.

## Defaults
- Time-off approval → proposed when balance and notice are fine and no one
  else in the team is off; otherwise flagged.
- Unknown balance → ask once, then keep it.
