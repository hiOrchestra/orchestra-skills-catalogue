---
name: analyze-data-quality
version: 0.1.0
description: >-
  Assess whether a dataset can be trusted before anyone analyzes it — check
  completeness, validity, duplicates, outliers, consistency, and freshness, then
  report each issue with a severity and a go / caution / no-go verdict. Use when
  the user says "is this data clean?", "can I trust this data?", "check the data
  quality", "audit this dataset", "any problems with this CSV", or "is this table
  reliable". Not for finding insights (explore-dataset) or building a visual
  (build-dashboard).
triggers:
  - is this data clean
  - can I trust this data
  - check the data quality
  - audit this dataset
  - any problems with this CSV
  - data quality check
  - is this table reliable
  - validate this data
  - how good is this data
metadata:
  openclaw:
    emoji: "🧪"
requires:
  bins: []
  env: []
  config: []
---

# Analyze Data Quality — is this dataset trustworthy?

Judge whether a dataset is fit to analyze *before* anyone draws conclusions from
it. Profile every column, hunt for the six classic defects — missing values,
invalid values, duplicates, outliers, broken consistency, and staleness — rate
each by severity, and end with a plain go / caution / no-go verdict plus how to
fix what's broken. The job is trust, not insight.

## Related skills
- **explore-dataset** — when the data is already trusted and the question is
  "what does it say?" (distributions, patterns, findings), use that. This skill
  is the gate you pass through first.
- **build-dashboard** — when the goal is a visual surface of the metrics that
  matter, not a verdict on whether the underlying data holds up, use that.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Someone is about to analyze, report on, or make a decision from a dataset and
  needs to know if it's sound first.
- Triggers: "is this data clean?", "can I trust this?", "audit this dataset",
  "any problems with this CSV?", "validate this table".
- **Do NOT use** to find patterns or answer questions *within* the data (that is
  explore-dataset), or to render metrics visually (that is build-dashboard).

## Workflow
1. **Load the data and pin its context.** Pull the table with `orch-database`,
   or read an uploaded CSV/file via `orch-files`. Confirm row count and column
   list, and note what the data is *supposed* to represent — you can't judge
   completeness or validity without knowing the intended shape.
2. **Profile every column.** For each: infer its type, and measure null/blank
   rate, distinct-value count, and range or min/max. This one pass surfaces most
   problems and tells you which checks below are even relevant.
3. **Completeness.** Flag columns with high null rates and rows missing required
   fields. A key column that's 30% empty quietly poisons every downstream metric.
4. **Validity.** Check values against their expected domain — dates that parse,
   numbers in plausible bounds, categoricals within a known set, formats (email,
   IDs) that match. Invalid values are worse than missing ones because they look
   real.
5. **Duplicates.** Look for fully duplicate rows and repeated business keys
   (same customer/order twice). Dupes silently inflate counts and sums.
6. **Outliers.** Spot values far outside a column's distribution and decide, in
   context, whether each is a genuine extreme or a data error (a $0 or negative
   price, an age of 900). Note them; don't delete them.
7. **Consistency & referential integrity.** Check that related fields agree
   (start ≤ end date, totals = sum of parts) and that foreign keys point to rows
   that exist. Broken joins are a top cause of wrong analysis.
8. **Freshness.** Find the latest timestamp and compare it to how current the
   data needs to be. Stale data is still "valid" yet leads to wrong decisions.
9. **Rate and verdict.** Assign each issue a severity (below), then give one
   overall go / caution / no-go for analysis with concrete remediation notes.

## Standards
- **Quantify, don't hand-wave.** "email is 12% null (1,431 of 11,920 rows)"
  beats "some emails missing." Numbers are what make the report actionable.
- **Report, don't silently repair.** Your job is to surface issues and recommend
  fixes, not to mutate the source data — that's the owner's call.
- **Separate defect from judgment call.** A broken foreign key is a fact; a
  suspicious outlier is a flag for a human. Say which is which.
- **No fabrication.** If a check couldn't run (column absent, type unknowable),
  say so rather than inventing a clean result.

## Severity
Rate each issue:
- **Critical** — makes analysis wrong or impossible (missing key column, broken
  joins, mass duplicates). Must fix before any analysis → no-go.
- **High** — materially distorts results (heavy nulls in an important field,
  systematic invalid values). Fix or caveat heavily.
- **Medium** — affects some analyses (scattered outliers, minor staleness).
  Proceed with documented caveats.
- **Low** — cosmetic or negligible (rare edge nulls, formatting nits). Note and
  move on.

Overall verdict: **Go** (no Critical/High), **Caution** (High present, usable
with caveats), or **No-go** (any Critical unresolved).

## Output
Lead with the **verdict** (go / caution / no-go) and a one-line why. Then an
**issues table** — issue, column(s), severity, count/rate, recommended fix —
ordered most-severe first. Follow with the **column profile** (type, null rate,
distinct, range) and any **caveats** an analyst must carry forward.

Substantial audit → save the report as a file via `orch-files` and post a short
summary with the verdict. Quick check on a small table → answer inline.

## Defaults
- No stated expected schema? Infer types and reasonable domains from the data,
  and state the assumptions you're judging against.
- Big table? Profile the full set for counts/nulls; sample for eyeballing values.
- When unsure whether an extreme value is an error, flag it as a Medium for human
  review rather than ruling on it yourself.
- A short report naming the 3 issues that actually block analysis beats an
  exhaustive list of every cosmetic nit.
