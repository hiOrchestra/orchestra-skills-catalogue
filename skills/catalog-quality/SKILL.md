---
name: catalog-quality
version: 0.1.0
description: >-
  Audit an online store's product catalogue the way a merchandiser and a
  shopper would — titles that say what the product is, descriptions that
  answer the buyer's questions, images, variants and options that make
  sense, prices and compare-at prices that are consistent, SEO titles and
  descriptions, products with no stock or no sales — and propose fixes in
  batches, written in the brand's voice. Use when the user says "improve my
  product pages", "audit the catalogue", "product descriptions", "why don't
  these products sell", "SEO for products". Not for orders or stock levels
  (shopify-store).
metadata:
  openclaw:
    emoji: "🏷️"
---
# Catalog Quality — product pages that answer the buyer and sell

Most stores lose sales on pages that do not say what the product is, show
it badly, or bury the answer to the one question a buyer has. This skill
goes through the catalogue, finds the pages that cost the most, and proposes
better titles, descriptions and details — in the brand's voice, never
inventing a property of the product.

## Related skills
- **shopify-store** — reads the products and applies approved changes.
- **voice-guide** — the brand's voice for every rewrite.
- **seo-writing** — when a product page should rank for a search.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A catalogue review, a new collection, products with traffic but no sales.
- **Do NOT use** to invent materials, sizes, certifications or claims, or to
  change prices; facts come from the person or the supplier's data.

## Workflow
1. **Read the catalogue** (products, variants, images, prices, tags, SEO
   fields) and sales per product if available.
2. **Check each product**: title says what it is (type, key attribute,
   variant); description answers fit/size, material, use, care, shipping;
   at least three images and alt text; variants named consistently; price
   vs compare-at consistent; SEO title ≤ 60 and description ≤ 155 chars;
   no orphan products (not in any collection).
3. **Rank** by revenue at stake: high-traffic or best-selling products with
   weak pages first, then products with no sales and weak pages.
4. **Propose rewrites** in batches of ≤ 10 products: current → proposed, for
   title, description and SEO fields, in the brand's voice, with a note of
   any fact that must be confirmed.
5. **Apply only approved changes** (through `shopify-store`) and log them.

## Standards
- Facts about the product come from the product data or the person; a
  missing fact is a question, not a sentence.
- One voice across the catalogue.
- Accessibility: alt text that describes the image.

## Output
Summary (products checked, issues by type) · ranked list with the issue per
product · the first batch of proposed rewrites.

## Defaults
- No sales data → rank by issues found, flagged.
- Description length → what the buyer needs: 50–150 words for simple
  products, longer for technical ones.
