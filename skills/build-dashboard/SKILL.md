---
name: build-dashboard
version: 0.1.0
description: >-
  Turn a dataset into a visual dashboard — the handful of KPIs and charts that
  answer the stakeholder's question — on the portal Canvas or as a report. Use
  when the user says "build a dashboard", "visualize this data", "dashboard
  for our KPIs", "make charts from this", "sales/marketing dashboard", or
  "show me the metrics that matter". Not for the underlying analysis or the
  trust check — do those first.
metadata:
  openclaw:
    emoji: "📊"
---
# Build Dashboard — dataset → the metrics that matter, shown

Turn a dataset into a focused visual dashboard: the 4–8 metrics and charts that
answer a specific person's specific question, not every number the data can
produce. A good dashboard is an argument, not a wall of tiles — each element
earns its place by informing a decision. Label everything, and always say what
window of data it covers and where it came from.

## Related skills
- **explore-dataset** — when you don't yet know what the data says. Do the
  exploratory analysis first; a dashboard visualizes conclusions you've already
  reached, it isn't how you find them.
- **analyze-data-quality** — when it's unclear whether the data can be trusted
  (gaps, dupes, stale, invalid values). Run that first — a polished dashboard
  built on bad data just launders the errors into something people believe.
- **build-report** — when the deliverable should be a static document
  (DOCX/PDF/deck) rather than an interactive Canvas surface. Hand it the chosen
  metrics and charts.
- **build-data-view** — when people need to *work in* the records rather than
  read the numbers: find a row, filter, open it, change its status. A dashboard
  is read; a data view is operated. They pair well — KPI tiles on top, the
  filterable list below.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The data is understood and trusted, and someone needs to *see* the key metrics
  — a recurring KPI view, a one-off "show me how X is doing", a leadership board.
- Triggers: "build a dashboard", "visualize this", "dashboard for our KPIs",
  "make charts from this", "show me the metrics that matter".
- **Do NOT use** to discover what's in the data (that's **explore-dataset**) or
  to vet whether it's reliable (that's **analyze-data-quality**). Don't reach for
  it when a single number or one chart answers the ask — just answer.

## Workflow
1. **Pin the audience and the questions.** Name who will look at this and the
   exact decisions they make from it. A CFO's revenue board and an ops lead's
   pipeline view are different dashboards from the same table. Write down the 3–5
   questions the dashboard must answer — every chart later maps to one of them.
2. **Confirm the data is explored and trusted.** Make sure the shape, meaning of
   each field, and any quality caveats are already known (via **explore-dataset**
   / **analyze-data-quality**). If not, stop and do that first — don't visualize
   numbers you can't vouch for.
3. **Load and shape the data.** Read the source with `orch-files` (uploaded CSV)
   or `orch-database` (tenant tables). Compute the aggregates each metric needs
   (totals, rates, period-over-period, segments) rather than plotting raw rows.
4. **Choose the 4–8 metrics.** Force the cut — a dashboard that shows everything
   answers nothing. Each metric must tie to a question from step 1; drop the
   rest. Prefer decision-driving metrics (trend, rate, comparison) over vanity
   counts.
5. **Pick the right chart per metric.** Match form to intent: trend over time →
   line; parts of a whole → stacked bar (not a pie past a few slices);
   comparison across categories → bar; single headline number → a big KPI tile
   with its delta. Don't decorate — the chart type is a claim about the data.
6. **Lay it out top-down.** Top-line KPI tiles first (the answers at a glance),
   then the breakdowns and trends that explain them. Order by importance, group
   related charts, and keep it to one focused screen where you can.
7. **Build it.** For an interactive surface, build on `orch-canvas`. For a static
   deliverable, hand the chosen metrics and charts to **build-report**
   (`orch-docs`). Use `orch-img` only if a specific static image is needed.
8. **Label and stamp.** Give every chart a plain-language title, axis labels, and
   units. State the data window (e.g. "Jan–Jun 2026") and the source table/file
   prominently. An unlabeled dashboard is a rumor.

## Standards
- Every chart answers one of the stated questions; if it doesn't, cut it.
- Chart type fits the data relationship — no pie charts for many categories, no
  dual axes that mislead, no truncated y-axis that exaggerates a trend.
- Numbers on the dashboard trace back to the source; never hand-type or estimate
  a figure into a tile.
- Data window and source are always visible, and any quality caveat from the
  trust check is carried through, not hidden.
- Fewer, sharper metrics beat a dense grid of tiles nobody reads.

## Output
- **Interactive** → build on `orch-canvas` and share the link, with a short note
  on what each section shows and the data window.
- **Static** → produce the document via **build-report** / `orch-docs` and save
  it with `orch-files`, then post a brief summary pointing at it.
- Either way, lead your reply with the 2–4 headline findings the dashboard makes
  visible — the dashboard is the evidence, not a substitute for the takeaway.

## Defaults
- If the audience or questions are unstated, assume the person who owns the data
  and the most obvious decision it drives; state that assumption and proceed.
- Default window = the most recent complete period the data supports; say which.
- When torn between more metrics and more clarity, choose clarity — 6 sharp tiles
  over 15 crowded ones.
- Prefer `orch-canvas` for anything someone will revisit; a report for a one-time
  hand-off.
