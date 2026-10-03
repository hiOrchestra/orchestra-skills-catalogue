---
name: shopify-store
version: 0.1.0
description: >-
  Work inside the person's Shopify store through their connected account —
  orders, fulfilment status, refunds, customers, products, variants and
  inventory levels; answer questions from live data ("how did we sell this
  week", "where is order 1042", "what is low on stock"); and change product
  details or inventory only after the person approves the exact change,
  keeping a log. Never cancels, refunds or fulfils orders. Use when the user
  says "Shopify", "my store", "orders", "this order", "stock levels",
  "update the product", "best sellers". Needs Shopify connected. Not for
  auditing listings (catalog-quality).
metadata:
  openclaw:
    emoji: "🛍️"
  orchestra:
    requires:
      integrations:
        - shopify
---
# Shopify Store — the store's numbers and records, read live, changed with care

A store owner's questions are concrete: what sold, what shipped, what is
running out, what this customer ordered. This skill answers them from the
live store, and changes products or stock only with an approved preview.
Anything that moves money or a parcel — refunds, cancellations,
fulfilment — stays with the person.

## Related skills
- **catalog-quality** — audits product listings; this skill applies the
  approved fixes.
- **reorder-plan** — what to restock, from the inventory read here.
- **support-reply** — answering a customer about their order.
- **orch-composio** — the tool every call goes through.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Questions about orders, customers, products or stock; approved edits to
  products and inventory.
- **Do NOT use** to cancel, refund, fulfil or edit orders, create discounts,
  change prices in bulk, or delete anything — propose and let the person do
  it in Shopify.

## Workflow
1. **Check the connection**: `orch-composio connections`; not connected →
   say so and stop.
2. **Find the action and confirm its schema** (`orch-composio schema --slug
   <SLUG>`). Core reads: `SHOPIFY_GET_ORDERS_WITH_FILTERS`,
   `SHOPIFY_GET_ORDER`, `SHOPIFY_GET_ORDER_FULFILLMENTS`,
   `SHOPIFY_GET_ORDER_REFUNDS`, `SHOPIFY_COUNT_ORDER`,
   `SHOPIFY_GET_CUSTOMERS_SEARCH`, `SHOPIFY_GET_CUSTOMER_ORDERS`,
   `SHOPIFY_COUNT_PRODUCTS`, `SHOPIFY_GET_INVENTORY_LEVELS`,
   `SHOPIFY_GET_INVENTORY_ITEMS`. Anything else: `orch-composio tools
   --toolkit shopify --search "<what>"`.
3. **Answer from live data**: sales for a period (orders, revenue, average
   order, refunds), an order's status and where it is, a customer's
   history, stock by product and location, best and worst sellers.
4. **Product or inventory changes are proposals**: product, field, current
   → new; wait for the yes; execute exactly that; read back; log it in
   `orch-database` (table `store_changes`).

## Standards
- Revenue figures say whether they include tax, shipping and refunds.
- Customer data is used only to answer the question asked, and stays in the
  conversation.
- Never touch an order's money or fulfilment.
- If a figure needs more orders than one page returns, page through all of
  them before reporting.

## Output
Answers first, then the records (order no. · date · customer · total ·
status). Sales summaries as a small table with the period and what is
included. Changes: preview, then "done", with the log.

## Defaults
- Period → last 7 days, compared with the 7 before.
- Currency → the store's currency.
- Low stock → below 14 days of average sales, or below 5 units when there is
  no sales history.
