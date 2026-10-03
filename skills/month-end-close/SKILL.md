---
name: month-end-close
version: 0.1.0
description: >-
  Run the monthly close as a checklist: every bank account reconciled, every
  invoice in, bills to pay and invoices to chase listed, the month's profit
  and loss and cash position summarised, what changed versus last month
  explained, and a clean package for the accountant. Use when the user says
  "close the month", "month end", "monthly numbers", "P&L for September",
  "what do I send my accountant", "cash position", "how did we do this
  month". Not for single invoices (invoice-capture) or categorising one
  export (expense-categorize).
metadata:
  openclaw:
    emoji: "📕"
---
# Month-End Close — the month finished, explained, and ready to hand over

A close is done when the numbers are complete, reconciled and explained —
not when a report is printed. This skill runs the checklist, says what is
still missing, produces the month's summary in plain language, and packages
everything the accountant needs, so the person spends ten minutes on the
month instead of a weekend.

## Related skills
- **invoice-capture** and **expense-categorize** — the inputs.
- **build-report** — when the summary goes to partners or investors.
- **action-tracker** — bills to pay and invoices to chase.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- After the month ends, or for any period the person names.
- **Do NOT use** to file taxes, sign off accounts, or tell them what they
  owe in tax — that is their accountant's.

## Workflow
1. **Checklist** for the period, each item done / missing: every account's
   export received and reconciled; every outflow with a document; sales
   invoices issued for everything delivered; payroll recorded; recurring
   costs present (a subscription that did not appear is a question).
2. **Payables and receivables**: bills due in the next 30 days; customer
   invoices overdue, by days late, with the amount.
3. **The month in numbers**: revenue, costs by category, profit, cash at
   start and end, with last month and the same month last year if available.
4. **What changed**: the three biggest movements versus last month, each
   explained from the transactions (a new hire, an annual bill, a big
   customer paying late).
5. **The package**: the categorised transactions, the invoice list with
   files, the open items, in the format the accountant asked for (`orch-files`).
6. **Lock**: once the person says the month is closed, mark it; later
   changes to that period need their yes and are noted.

## Standards
- Missing is reported as missing — never a total that silently excludes it.
- Explanations come from transactions, not from assumptions.
- Management numbers are labelled as such; they are not the statutory
  accounts.
- The package contains only what the accountant needs.

## Output
Checklist status · the month in numbers (table) · what changed (3 bullets) ·
to pay / to chase · what the accountant gets and where it is.

## Defaults
- Close day → the 5th of the next month.
- Comparisons → previous month; same month last year when the data exists.
- Format for the accountant → CSV of transactions + folder of documents.
