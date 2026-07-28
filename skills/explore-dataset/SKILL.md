---
name: explore-dataset
version: 0.1.0
description: >-
  Explore a dataset to understand its shape and surface what matters —
  distributions, segments, trends, outliers and relationships — before
  committing to a report or dashboard. Use when the user says "explore this
  data", "analyze this CSV/table", "what's in this dataset", "find patterns/
  insights", "what stands out", or hands you data and asks "what does this tell
  us?". Not for judging whether the data is trustworthy, and not for the final
  chart or document.
triggers:
  - explore this dataset
  - analyze this CSV
  - analyze this data
  - what's in this data
  - find patterns in
  - what insights are in
  - what stands out in this data
  - dig into this data
  - exploratory analysis
metadata:
  openclaw:
    emoji: "🔬"
requires:
  bins: []
  env: []
  config: []
---

# Explore Dataset — data → its shape and the findings that matter

Do exploratory analysis: understand what the dataset is, then surface the
handful of patterns worth acting on. The job is not to dump every statistic —
it is to learn the shape (columns, grain, distributions), slice it the ways that
reveal something, and report the 3–5 findings that would change a decision, each
with the evidence behind it and an honest read on how solid it is.

## Related skills
- **analyze-data-quality** — when the real question is "can I trust this data?"
  (completeness, dupes, validity, freshness). Run it *first* on unvetted data;
  exploring dirty data produces confident nonsense.
- **build-dashboard** — when the deliverable is the recurring visual surface of
  the key metrics. Explore first to find what's worth showing, then hand it off.
- **build-report** — when the findings should become a polished document
  (DOCX/PDF/deck) for an audience, hand the analysis to it.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user hands you a dataset (CSV, table, upload) and wants to understand it
  or find what's interesting — patterns, segments, outliers, relationships.
- Triggers: "explore this data", "analyze this CSV", "what's in this dataset",
  "find patterns/insights", "what stands out", "dig into this".
- **Do NOT use** to vet trustworthiness (that is analyze-data-quality — do it
  first if the data is unvetted), to build the final chart/dashboard (that is
  build-dashboard), or to produce the finished document (that is build-report).

## Workflow
1. **Frame the question + how it'll be used.** Pin down what the user wants out
   of this — a decision, a metric, a hunch to confirm. That sets which slices
   matter. If it's an open "just explore," say so and pick the highest-signal
   angles yourself rather than stalling.
2. **Vet first if unvetted.** If the data's provenance is unknown, run
   **analyze-data-quality** (or a quick check) before trusting any pattern.
3. **Learn the shape.** Load the data — `orch-files` for an uploaded CSV/file,
   `orch-database` for a tenant table. Establish the **grain**: what does one
   row represent? List columns, types, and row count. Getting the grain wrong
   invalidates every aggregate downstream, so confirm it explicitly.
4. **Summary stats.** For numeric columns: min/max/mean/median/spread and
   null rates. For categorical: distinct values and frequency of the top ones.
   This tells you where the mass is and where the weird tails live.
5. **Slice by the key dimensions.** Break the main measures down by the
   segments that matter (time, category, region, cohort). Patterns live in the
   cuts, not the grand total — a flat average often hides two opposite stories.
6. **Look for trends, outliers, relationships.** Trends over time; outliers and
   what drives them; correlations between columns. Treat correlation as a lead
   to explain, not a cause — say so.
7. **Surface the findings that matter.** Distill to the 3–5 findings that would
   actually change a decision, each backed by a number. Drop the trivia.
8. **Suggest the next step** — usually build-dashboard (to monitor) or
   build-report (to communicate), or a deeper cut worth pursuing.

## Standards
- Every finding cites its evidence — the number, the slice, the row count it
  rests on. A claim without a figure behind it is an opinion.
- State the grain and any filters applied, so a reader can reproduce the cut.
- Distinguish what the data **shows** (measured) from what you **infer** (a
  likely explanation) from **speculation** (flag it). Correlation ≠ cause.
- Note the base: a 300% jump on 4 rows is noise. Call out small-n findings.
- Never invent numbers. If a column is too dirty or sparse to trust, say so and
  point back at **analyze-data-quality** rather than analyzing around it.

## Confidence labels
Tag each key finding so the user knows how much weight it bears:
- **High** — large n, consistent across slices, robust to obvious confounders.
- **Medium** — real but limited (smaller n, one segment, or partly explained).
- **Low** — suggestive only: tiny sample, noisy, or confounded — call it out.

## Output
Lead with the answer, then the evidence:
- **Headline** — 2–4 sentences: what this dataset is and the single biggest
  takeaway.
- **Shape** — grain (what one row is), row count, columns/types in brief.
- **Key findings** — 3–5 bullets, each with its number/slice + confidence label.
- **Notable outliers / caveats** — what's weird, sparse, or not to be trusted.
- **Suggested next step** — dashboard, report, or a deeper cut.

Non-trivial analysis → save a written summary via `orch-files` and post a short
recap pointing at it; keep any working tables there too. Quick look → inline.

## Defaults
- Breadth first (shape + top slices), then depth on the one thread that looks
  most decision-relevant; time-box the rest.
- When "explore" is open-ended, prioritize the biggest measure and its cut by
  time and by the largest category, then follow what's surprising.
- Prefer robust stats (median, rates) over ones a single outlier can swing.
- Five findings that survive scrutiny beat twenty raw observations.
