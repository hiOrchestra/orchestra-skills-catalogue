---
name: keyword-research
version: 0.1.0
description: >-
  Find the searches a business can realistically win and that bring the
  people it wants — the real queries behind its offer, grouped by intent,
  weighed by how hard the current results are to beat and how close the
  searcher is to buying — and turn them into a short list of pages to build
  or fix. Use when the user says "keyword research", "what should we rank
  for", "what do people search", "topics for SEO", "find keywords",
  "content gaps", "what are competitors ranking for". Not for writing the
  page (seo-writing), auditing the site (seo-audit) or planning a calendar
  (content-plan).
metadata:
  openclaw:
    emoji: "🧭"
---
# Keyword Research — the searches worth winning, and the page each one needs

A keyword list is only useful if every line ends in a decision: build this
page, fix that one, ignore the rest. This skill starts from the business and
its buyers, finds the queries they actually type, reads what ranks for each,
and returns a short list of targets — each with its intent, the page it
needs and an honest read of how hard it is.

## Related skills
- **seo-writing** — writes the page for a target this skill picked.
- **content-plan** — puts the chosen targets on a calendar.
- **seo-audit** — whether the existing pages can rank at all.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Deciding what a site should be found for, or why it is found for the
  wrong things.
- **Do NOT use** to produce a long export of volumes with no decision
  attached, or to promise traffic. Without a paid keyword tool you have no
  exact volumes — say so and rank by evidence instead.

## Workflow
1. **Start from the buyer, not the word.** What the business sells, to whom,
   the problem the buyer has before they know the product, the words the
   buyer uses (from their emails, calls, reviews — ask for them). Ask once,
   in one round.
2. **Seed queries** in three bands: the problem ("how to …", "why does …"),
   the solution category ("best … for …", "… software"), the decision
   ("… vs …", "… pricing", "… alternative"). Add the language and market.
3. **Expand from evidence.** `web_search` each seed and read: the autocomplete
   and "People also ask" questions, related searches, the titles that rank.
   Note the queries competitors' pages are built around (`web_fetch` their
   key pages' titles and headings).
4. **Read the results page for every candidate.** Who ranks (big brands,
   forums, small sites like this one), what format wins (guide, list, tool,
   product page), whether the intent matches what the business offers.
5. **Group into topics** — queries one page can answer together — and give
   each topic: intent, closeness to buying, difficulty (below), whether the
   site already has a page for it (ask for the sitemap or `web_fetch` it).
6. **Pick.** The few topics where intent fits the offer, difficulty is
   winnable, and the page does not exist or is weak. Say why each made it
   and name two that did not.

## Standards
- Every target is backed by what you saw in the results, not by a guess at
  volume. If the person has a keyword tool or Search Console export, use its
  numbers and say which.
- One page per intent: two targets that one page answers are one target.
- Never put a query on the list that the business cannot honestly answer.
- Brand and competitor names only where comparing is fair and accurate.

## Difficulty
- **Winnable** — results include small or mid sites, forums, or pages that
  answer badly.
- **Stretch** — mostly strong sites, but a clear gap in what they cover.
- **Not now** — dominated by large brands or official sources answering
  well; revisit when the site has authority.

## Output
- **Target list** (5–12 rows): topic · main query · 2–4 related queries ·
  intent · stage (problem / solution / decision) · difficulty · existing page
  or "new" · why.
- **First three to build or fix**, in order, one line each.
- **Left out** — two or three tempting queries and why not.
- Save the full list with `orch-files`.

## Defaults
- No market given → the site's language and the person's country.
- Early-stage site → favour problem and decision queries over broad category
  terms.
- Asked for volumes with no tool connected → explain the gap once, offer to
  use an export if they have one, and proceed on evidence.
