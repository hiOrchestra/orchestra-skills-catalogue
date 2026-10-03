---
name: reorder-plan
version: 0.1.0
description: >-
  Decide what to reorder, how much and when — from current stock, open
  orders, the demand forecast, each supplier's lead time and minimum order —
  with reorder points and safety stock per product, the products at risk of
  running out, excess stock tying up cash, and purchase orders drafted for
  the person's yes. Use when the user says "what should I reorder", "are we
  running out", "reorder points", "safety stock", "draft purchase orders",
  "overstock", "inventory planning". Not for the forecast itself
  (demand-forecast).
metadata:
  openclaw:
    emoji: "📦"
---
# Reorder Plan — order the right amount, just in time

Running out loses sales; overstock ties up cash and space. This skill sets,
for each product, the stock level at which to reorder and how much,
from the forecast, the supplier's lead time and the service level the
business wants — and turns today's stock into a short list: order now,
watch, too much.

## Related skills
- **demand-forecast** — the expected demand this plan uses.
- **analyze-data-quality** — when stock counts look wrong.
- **action-tracker** — purchase orders sent and their expected arrival.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Regular inventory reviews, before a season, when a supplier changes terms.
- **Do NOT use** to place orders or contact suppliers: the plan drafts
  purchase orders; the person sends them.

## Workflow
1. **The inputs**: current stock per product (and per location), open
   purchase orders and their dates, the forecast, each supplier's lead time
   (and how reliable it is), minimum order quantity, pack size, unit cost.
2. **Service level** per product class, agreed with the person (e.g. 95%
   for top sellers, 90% for the rest).
3. **Compute** per product: demand during lead time, safety stock from the
   forecast range and lead-time variability, reorder point = lead-time
   demand + safety stock, order quantity rounded to MOQ and pack size.
4. **Classify today's stock**: below reorder point → order now; within two
   weeks of it → watch; above several months of cover → excess (with the
   cash it holds).
5. **Draft purchase orders** grouped by supplier, with quantities, expected
   arrival and cost, for the person's yes. Note where combining orders meets
   a supplier minimum or a shipping threshold.
6. **Track**: sent orders become rows with expected arrival; late arrivals
   are flagged.

## Standards
- Every recommended quantity shows the numbers behind it.
- Lead times are the real ones observed, not the supplier's brochure, when
  the data allows.
- Never round down below what the safety stock requires to fit a budget
  without saying the service level drops.
- Units and currencies are explicit everywhere.

## Output
Order now (product · stock · reorder point · quantity · supplier · arrival ·
cost) · watch · excess (with cash tied up) · draft POs per supplier ·
assumptions.

## Defaults
- Service level → 95% for the top 20% of products by revenue, 90% otherwise.
- Lead time unknown → ask; until then, 14 days flagged.
- Review cadence → weekly.
