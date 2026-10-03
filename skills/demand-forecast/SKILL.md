---
name: demand-forecast
version: 0.1.0
description: >-
  Forecast how much of each product will sell in the coming weeks or months
  from the sales history — trend, seasonality, promotions and stock-outs
  accounted for — with a range, not a single number, and the accuracy of the
  method on past data shown. Use when the user says "forecast demand", "how
  much will we sell", "sales forecast", "plan next quarter's volumes",
  "seasonality", "predict orders". Not for deciding what to reorder
  (reorder-plan) or general data exploration (explore-dataset).
metadata:
  openclaw:
    emoji: "📈"
---
# Demand Forecast — what will sell, with an honest range

A forecast is a plan with error bars. This skill takes the sales history,
cleans the obvious distortions (stock-outs that hid demand, one-off bulk
orders, promotions), picks a method simple enough to explain, checks how
well it would have predicted the recent past, and gives each product a
range the business can plan against.

## Related skills
- **reorder-plan** — turns the forecast into what to buy and when.
- **analyze-data-quality** — before trusting the history.
- **build-dashboard** — forecast vs actual on a Canvas page.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Planning purchases, production, staffing or cash around volumes.
- **Do NOT use** with fewer than three months of history for a product
  without saying the forecast is a rough guess, or for products with no
  history at all — ask for a comparable product instead.

## Workflow
1. **The history**: sales by product (SKU) by day or week, ideally 12+
   months; stock levels or stock-out dates; promotions and price changes;
   anything unusual (a big one-off order, a closure).
2. **Clean**: mark stock-out periods (sales there understate demand), remove
   or flag one-offs, note promotions. Say what was changed.
3. **Segment products**: steady sellers, seasonal, intermittent (many zero
   weeks), new. Each gets a method that suits it — moving average or
   exponential smoothing for steady, seasonal decomposition for seasonal,
   a rate-based approach for intermittent.
4. **Back-test**: forecast the last 4–8 weeks from the data before them and
   compare with what happened; report the error per segment.
5. **Forecast** the horizon asked, per product, with a low / expected / high
   range, and the assumptions (no new promotion, current price).
6. **Explain** what drives the biggest changes versus last period.

## Standards
- A range always, never a single number; the width is the honest part.
- The method is one a person can explain to their team.
- Known future events (a planned promotion, a new channel) are adjustments
  stated explicitly, not hidden in the numbers.
- When the history is too short or too noisy, say so first.

## Output
Per product: expected, low, high for each period · segment and method ·
back-test error. Plus: the five products that matter most by volume, what
changed, assumptions. Tables saved with `orch-files` or in `orch-database`
(table `forecasts`).

## Defaults
- Horizon → 12 weeks by week.
- Range → roughly the 80% band from the back-test errors.
- Stock-out weeks → excluded from fitting, flagged.
