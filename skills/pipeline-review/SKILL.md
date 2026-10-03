---
name: pipeline-review
version: 0.1.0
description: >-
  Run the weekly pipeline review from the CRM — what moved, what is stuck,
  what will really close this month versus what the CRM says, deals with no
  next step, and the three conversations worth having — with every number
  traced to the deals behind it. Works with any CRM the agent can read. Use
  when the user says "pipeline review", "forecast this month", "what's
  closing", "which deals are stuck", "sales meeting prep", "how's the
  pipeline". Not for cleaning the data (crm-hygiene).
metadata:
  openclaw:
    emoji: "🧮"
---
# Pipeline Review — the honest forecast and the deals that need a push

A pipeline review is useful when it separates what the CRM says from what is
likely: deals marked "closing this month" with no activity in three weeks
are hopes, not forecast. This skill reads the deals, sorts them by what they
need, and gives the team the forecast and the few conversations that change
it.

## Related skills
- **hubspot-crm** — fetches the deals and activity in HubSpot.
- **crm-hygiene** — when the review shows the data itself is unreliable.
- **build-dashboard** — the pipeline as a Canvas page.
- **action-tracker** — next steps agreed in the review.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Weekly, before a sales meeting, at month or quarter end.
- **Do NOT use** to change deal stages or amounts on the agent's own
  judgement; propose changes for the owner's yes.

## Workflow
1. **Fetch** open deals with stage, amount, close date, owner, created and
   last-activity dates, next step; and deals closed (won/lost) since the
   last review.
2. **What moved**: new deals, stage changes, won and lost with amounts.
3. **Commit vs. hope**: for deals closing in the period, mark each as
   likely (recent activity, next step booked, stage advanced), at risk (no
   activity in 14+ days, close date already moved, no next step) or
   unlikely (past close date, stalled for twice the stage norm).
4. **The forecast**: CRM total for the period, likely total, at-risk total.
5. **Stuck and naked deals**: older than their stage norm; no next step.
6. **Three conversations**: the deals where one action this week changes
   the forecast most, with the action.

## Standards
- Every figure is the sum of named deals; the deals are listed.
- "Likely" rests on activity evidence, not on the owner's optimism or the
  stage's default probability.
- Won and lost reasons are recorded as the CRM states them, not inferred.

## Output
Moved since last review · forecast (CRM / likely / at risk) · stuck and
no-next-step lists · three conversations · open questions for owners.

## Defaults
- Period → current month; at quarter end, the quarter.
- Stage norm → median days deals spent in that stage over the last 6 months.
