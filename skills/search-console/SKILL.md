---
name: search-console
version: 0.1.0
description: >-
  Read the person's Google Search Console through their connected account —
  the queries people searched, clicks, impressions, click-through rate and
  average position by query, page, country and device; sitemaps and their
  status; and how Google sees a given URL (indexed or not, and why) — to
  explain organic search performance and find the queries and pages worth
  working on. Read-only except submitting a sitemap with the person's yes.
  Use when the user says "Search Console", "what do people search to find
  us", "impressions", "position", "is this page indexed", "organic
  clicks dropped". Needs Google Search Console connected. Not for on-site
  traffic after the click (ga4-reporting).
metadata:
  openclaw:
    emoji: "🔭"
  orchestra:
    requires:
      integrations:
        - google_search_console
---
# Search Console — what people search, where you show up, and what Google indexed

Search Console is the only first-hand record of how a site appears in
Google: the queries, the positions, the clicks, and whether a page is in the
index at all. This skill reads it to explain organic performance and to find
the quick wins — queries where the site already shows up but too low or
with too few clicks.

## Related skills
- **ga4-reporting** — what visitors did after the click.
- **seo-audit** — the site-side reasons a page is not indexed or ranking.
- **keyword-research** — targets beyond what the site already shows for.
- **orch-composio** — the tool every call goes through.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Organic search questions, index checks, finding quick wins.
- **Do NOT use** to add or delete properties, remove URLs or change
  settings; submitting a sitemap is the only write, and only with a yes.

## Workflow
1. **Check the connection**: `orch-composio connections`; not connected →
   say so and stop. List sites (`GOOGLE_SEARCH_CONSOLE_LIST_SITES`) and use
   the property the procedure names (domain or URL-prefix).
2. **Confirm the schema before first use** (`orch-composio schema --slug
   GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`).
3. **Performance**: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` by query,
   page, country or device for the period and a comparison period.
4. **Quick wins**: queries with high impressions and position 5–20, or
   position 1–5 with CTR well below the norm for that position — each with
   the page that ranks and what to change (title, snippet, content depth).
5. **Index checks**: `GOOGLE_SEARCH_CONSOLE_INSPECT_URL` for a page,
   `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS` for sitemap status; explain the
   verdict in plain words.
6. **A drop**: split by query and page to find where it happened; check
   whether position fell (ranking) or impressions fell (demand or indexing).

## Standards
- Search Console data lags 2–3 days; the latest days are partial — say so.
- Position is an average; a change of one place on a long-tail query is noise.
- Anonymised queries make query totals smaller than page totals; never
  present that gap as lost traffic.
- Read-only except an approved sitemap submission.

## Output
The answer in two lines · table of queries or pages (clicks, impressions,
CTR, position, change) · quick wins with the fix · index verdicts.

## Defaults
- Period → last 28 days vs the previous 28.
- Quick-win list → top 10 by impressions.
