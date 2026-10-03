---
name: expense-categorize
version: 0.1.0
description: >-
  Take a bank or card statement export and categorise every movement with
  the business's own chart of categories, match each one to its invoice or
  receipt, and list what has no document, what looks duplicated, and what is
  personal or unusual — learning the rules from the person's corrections.
  Use when the user says "categorise my expenses", "reconcile the bank",
  "match receipts", "what's missing an invoice", "clean up the bank export",
  or sends a bank CSV. Not for reading invoices (invoice-capture) or the
  monthly close (month-end-close).
metadata:
  openclaw:
    emoji: "🗂️"
---
# Expense Categorize — every movement in its place, with its document

A bank export is the truth about what moved; invoices are the explanation.
This skill puts each movement in the business's own category, finds the
document that explains it, and leaves a short list of what still needs the
person: movements with no invoice, doubtful categories, anything unusual.

## Related skills
- **invoice-capture** — the documents this skill matches against.
- **analyze-data-quality** — when the export itself looks broken.
- **month-end-close** — uses the reconciled movements.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A statement export (CSV, XLSX) from a bank, card or payment provider.
- **Do NOT use** to move money, to decide how something is treated for tax,
  or to re-categorise a closed period without the person's yes.

## Workflow
1. **Read the export** and describe it: account, period, rows, opening and
   closing balance if present. Check the balance reconciles; say so if not.
2. **The categories are theirs.** Use the chart in their procedure; if
   none, propose a short one (revenue, cost of sales, software, payroll,
   rent, travel, marketing, taxes, transfers, owner, other) for their yes.
3. **Rules first, then judgement.** Apply the rules learned from earlier
   corrections (merchant → category). For the rest, categorise from the
   merchant and description, marking each as rule or guess.
4. **Match documents**: each outflow to an invoice in `invoices` by amount,
   date (± a few days) and supplier; each inflow to a sales invoice.
5. **Store** in `orch-database` (table `transactions`: date, description,
   amount, currency, account, category, source (rule / guess / person),
   invoice_id, flags). Corrections from the person become rules in
   `category_rules` so the next month needs fewer.
6. **List what needs them**: no document, guessed categories above a size
   they set, possible duplicates, transfers between own accounts, anything
   that looks personal.

## Standards
- A guess is labelled a guess until the person confirms or a rule covers it.
- Transfers between the business's own accounts are not income or expense.
- Totals per category reconcile to the export's total movement.
- Nothing is deleted or merged silently.

## Output
Summary (period, in, out, net, reconciled yes/no) · totals by category ·
needs you: no document / to confirm / unusual · rules learned this time.

## Defaults
- Guess threshold → confirm anything above the business's typical monthly
  software bill, or 500 in their currency if unknown.
- Card fees, bank fees → "bank fees" without asking.
