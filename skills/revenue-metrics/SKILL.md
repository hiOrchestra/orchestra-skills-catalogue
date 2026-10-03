---
name: revenue-metrics
version: 0.1.0
description: >-
  Compute subscription revenue metrics correctly and explain them — MRR and
  ARR, new, expansion, contraction and churned MRR, logo and revenue churn,
  net revenue retention, ARPA, collection rate — from billing data (Stripe or
  an export), with every definition stated and every number reconcilable to
  the invoices behind it. Use when the user says "MRR", "ARR", "churn rate",
  "net retention", "NRR", "SaaS metrics", "investor update numbers", "how is
  revenue growing". Not for reading Stripe itself (stripe-revenue).
metadata:
  openclaw:
    emoji: "📊"
---
# Revenue Metrics — the numbers investors ask for, computed the same way every month

SaaS metrics are easy to compute wrong: annual plans counted as one month,
discounts ignored, one-off charges inside MRR, churn divided by the wrong
base. This skill states the definitions, computes each metric from the
billing data, and keeps the method fixed so month-on-month comparisons mean
something.

## Related skills
- **stripe-revenue** — the billing data these metrics are built from.
- **build-dashboard** — the metrics as a Canvas page.
- **build-report** — the monthly or investor update.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Monthly metrics, board or investor updates, pricing changes analysis.
- **Do NOT use** to produce audited financials or revenue recognition for
  statutory accounts; these are management metrics.

## Workflow
1. **Agree definitions once** and write them into the procedure: MRR =
   recurring subscription amount normalised to a month, after discounts,
   excluding tax, one-offs and usage unless agreed; annual plans ÷ 12;
   trialing excluded; past-due included until cancelled (or not — choose
   and keep).
2. **Build the movement table** per customer per month: starting MRR, new,
   expansion, contraction, churned, ending MRR.
3. **Compute**: MRR, ARR (MRR × 12), MRR movements, logo churn (customers
   lost ÷ customers at start), revenue churn (churned + contraction ÷
   starting MRR), NRR ((start + expansion − contraction − churn) ÷ start),
   ARPA, collection rate (collected ÷ billed).
4. **Reconcile**: ending MRR of one month equals starting MRR of the next;
   MRR ties to the active subscriptions list.
5. **Explain**: the three biggest movements by customer, and what changed in
   the trend.

## Standards
- Definitions are printed with the numbers, every time.
- One currency per figure; conversion rates stated when combined.
- A changed definition restates the history, with a note.
- No rounding until the final figure.

## Output
Metrics table (this month, last month, 3 and 12 months ago when available)
· MRR movement waterfall · three biggest movements · definitions used.

## Defaults
- Currency → the account's main currency; others converted at month-end rate,
  flagged.
- Churn base → customers and MRR at the start of the month.
