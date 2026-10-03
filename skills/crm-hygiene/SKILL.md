---
name: crm-hygiene
version: 0.1.0
description: >-
  Audit a CRM's data the way a careful admin would — duplicate contacts and
  companies, records missing the fields the team relies on, deals with no
  next step or stuck past their stage's normal age, contacts with no owner,
  bad emails and phone formats — and turn it into a ranked list of fixes,
  each with the records and the proposed change, for approval in batches.
  Works with any CRM the agent can read (HubSpot, Pipedrive, Salesforce, an
  export). Use when the user says "clean the CRM", "duplicates", "CRM
  hygiene", "data quality in HubSpot", "missing fields", "stale deals". Not
  for the weekly pipeline conversation (pipeline-review).
metadata:
  openclaw:
    emoji: "🧹"
---
# CRM Hygiene — a CRM the team can trust again

A CRM rots quietly: two records for the same customer, deals nobody has
touched in months, contacts nobody owns. Each one costs a missed follow-up
or a wrong report. This skill finds the rot, ranks it by what it costs, and
proposes fixes in batches small enough to approve with confidence.

## Related skills
- **hubspot-crm** — reads the records and applies approved fixes in HubSpot.
- **analyze-data-quality** — the same discipline for any dataset or export.
- **pipeline-review** — when the question is the deals, not the data.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A periodic clean-up, before a migration or a report that matters, or when
  the team stops trusting the numbers.
- **Do NOT use** to delete anything, or to change records in bulk without a
  preview the person approved.

## Workflow
1. **Agree what "clean" means here** — the fields every contact, company
   and deal must have; the normal age of each deal stage; who may own what.
   Read it from the procedure, or propose it once.
2. **Read** the records (through the CRM's skill, or an export), in pages.
3. **Find**: duplicates (same email; same domain for companies; same name +
   company; fuzzy names flagged separately), missing required fields, deals
   with no next step or close date, deals older than their stage norm,
   records with no owner, malformed emails and phones, closed deals still
   open, contacts with no company.
4. **Rank** by cost: duplicates and stale deals in the open pipeline first,
   then missing fields on active records, then cosmetic issues.
5. **Propose fixes in batches** (≤ 50 records): for each record, the issue,
   the proposed change and why; for duplicates, which record survives and
   what moves into it. Nothing is changed until the yes.
6. **Re-check** after fixes and report the before/after counts.

## Standards
- Every finding shows the records; a count without examples is not a finding.
- Fuzzy duplicates are proposed, never merged without a person looking.
- A field is filled from a source (another record, the company's site),
  never invented.
- Deletion is never proposed as a fix; archiving is the person's call.

## Severity
- **High** — duplicates and wrong data in the open pipeline.
- **Medium** — missing required fields on active records; ownerless records.
- **Low** — formatting, closed or inactive records.

## Output
Summary (records checked, issues by type, before/after if re-run) · the
ranked findings with examples · the first batch of fixes for approval.

## Defaults
- Required fields unknown → email, owner and company for contacts; amount,
  close date, stage and next step for deals.
- Stage norm unknown → twice the median age of deals that left that stage.
