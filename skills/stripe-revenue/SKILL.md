---
name: stripe-revenue
version: 0.1.0
description: >-
  Read the person's Stripe account through their connected access —
  customers, subscriptions, invoices, charges, payment intents, refunds,
  disputes and balance — to answer revenue questions from live data and to
  flag what needs attention: failed and retried payments, past-due
  invoices, disputes with a deadline, unusual refunds. Read-only: never
  creates charges, refunds, coupons or subscription changes. Use when the
  user says "Stripe", "how much did we bill", "failed payments", "past due",
  "disputes", "who cancelled", "MRR from Stripe". Needs Stripe connected.
  Not for defining the metrics themselves (revenue-metrics).
metadata:
  openclaw:
    emoji: "💳"
  orchestra:
    requires:
      integrations:
        - stripe
---
# Stripe Revenue — what was billed, collected and at risk, read live

Stripe holds the truth about money in and money that failed to come in. This
skill reads it to answer revenue questions and to surface what needs a
person — a card that keeps failing, an invoice past due, a dispute with a
deadline. It never moves money: no charges, refunds, credits or
subscription changes.

## Related skills
- **revenue-metrics** — how MRR, churn and the rest are computed from what
  this skill reads.
- **account-health** — payment signals feed customer health.
- **build-dashboard** — revenue on a Canvas page.
- **orch-composio** — the tool every call goes through.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Revenue questions, collections follow-up, dispute deadlines, cancellations.
- **Do NOT use** to refund, charge, cancel, pause or change a subscription,
  create coupons or answer a dispute — prepare the facts and let the person
  act in Stripe.

## Workflow
1. **Check the connection**: `orch-composio connections`; not connected →
   say so and stop.
2. **Confirm the schema before first use** (`orch-composio schema --slug
   <SLUG>`). Core reads: `STRIPE_LIST_CUSTOMERS`, `STRIPE_SEARCH_CUSTOMERS`,
   `STRIPE_LIST_SUBSCRIPTIONS`, `STRIPE_SEARCH_SUBSCRIPTIONS`,
   `STRIPE_LIST_INVOICES`, `STRIPE_SEARCH_INVOICES`, `STRIPE_LIST_CHARGES`,
   `STRIPE_LIST_PAYMENT_INTENTS`, `STRIPE_LIST_REFUNDS`,
   `STRIPE_LIST_DISPUTES`, `STRIPE_GET_BALANCE_HISTORY`.
3. **Page through everything** in the period before computing a total;
   Stripe lists are paginated and a first page is never the answer.
4. **Answer**: billed, collected, refunded, disputed for the period, by
   currency; new, cancelled and changed subscriptions; failed payments and
   their retry state; invoices past due with days and amounts; disputes with
   their evidence deadline.
5. **Flag what needs a person**: past-due over the agreed threshold,
   disputes due within 7 days, customers with repeated failures, refunds
   larger than usual.

## Standards
- Amounts in the currency and unit Stripe stores, converted from cents and
  labelled; never mix currencies in one total.
- Test-mode data is never mixed with live data; say which one was read.
- Customer and card details are shown only as needed (name, last four).
- Read-only, always.

## Output
Period summary table (billed · collected · refunded · disputed, per
currency) · subscriptions moved · needs attention (with deadlines) · the
records behind each figure on request.

## Defaults
- Period → current month to date, compared with last month.
- Past-due threshold → 7 days.
