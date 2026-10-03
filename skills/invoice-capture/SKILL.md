---
name: invoice-capture
version: 0.1.0
description: >-
  Read invoices and receipts — PDFs, photos, forwarded emails — and record
  each one exactly: supplier, tax ID, invoice number, dates, net, tax and
  total, currency, what was bought, due date; flag duplicates, missing fields
  and totals that do not add up; never guess a number. Use when the user
  says "log these invoices", "enter this receipt", "process my bills",
  "extract the invoice data", "add to the books", or sends invoices or
  receipts. Not for categorising bank movements (expense-categorize) or
  closing the month (month-end-close).
metadata:
  openclaw:
    emoji: "🧾"
---
# Invoice Capture — every invoice recorded exactly, or flagged

Books are only as good as what goes into them. This skill reads each invoice
or receipt, records the fields an accountant needs exactly as printed, checks
that the arithmetic holds, and flags anything doubtful instead of filling it
in. A blank with a flag is better than a confident wrong number.

## Related skills
- **expense-categorize** — matches captured invoices to bank movements and
  assigns categories.
- **month-end-close** — uses everything captured in the period.
- **action-tracker** — due dates of bills to pay become rows.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Purchase invoices, sales invoices, receipts and credit notes, one or many.
- **Do NOT use** to pay anything, to change an issued invoice, or to give
  tax advice on how an item should be treated — flag it for the accountant.

## Workflow
1. **Read the document** with the native document and image tools (PDF
   text, image reading). For a forwarded email, use the attachment, not the
   email body.
2. **Extract**: type (invoice / receipt / credit note), issuer and their tax
   ID, recipient, invoice number, issue date, due date, line items, net per
   tax rate, tax per rate, total, currency, payment method if stated.
3. **Check**: lines sum to net, net + tax = total, the recipient is this
   business, the tax ID has the right format for the country, the number is
   not already recorded (same supplier + number, or same supplier + total +
   date).
4. **Record** in the instance database (`orch-database`, table `invoices`:
   id, type, supplier, supplier_tax_id, number, issue_date, due_date, net,
   tax, total, currency, category, status (to review / recorded / paid),
   file, flags). Keep the file in `orch-files` and link it. Create the table
   on first use and say so.
5. **Flag, do not fix**: unreadable fields, totals that do not add up,
   foreign currency without a rate, a recipient that is not the business,
   a possible duplicate. Ask the person once for all the flags together.

## Standards
- Numbers are copied, never estimated. Unreadable is a flag.
- Dates in ISO format; amounts with their currency; no rounding.
- Nothing is deleted: a wrong entry is corrected with a note of what changed.
- Financial documents stay in the instance.

## Output
Per batch: how many captured · total by currency · the list (supplier ·
number · date · total · status) · flags to resolve · bills due in the next
14 days.

## Defaults
- Category unknown → leave empty for expense-categorize or the person.
- Currency not printed → the business's currency, flagged.
- Due date missing → issue date + the supplier's usual terms if known, flagged.
