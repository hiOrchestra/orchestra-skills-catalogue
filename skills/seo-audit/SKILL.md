---
name: seo-audit
version: 0.1.0
description: >-
  Audit a live site the way a search engine and a searcher meet it — whether
  pages can be found and indexed, what each page tells search about itself
  (titles, descriptions, headings, canonicals), what is thin, duplicated or
  competing with itself, and what is slow or broken — and turn it into a
  short list of fixes ranked by impact, each with the page and the evidence.
  Use when the user says "SEO audit", "why don't we rank", "check my site for
  SEO", "technical SEO", "indexing", "my traffic dropped", "crawl my site".
  Not for writing or rewriting a piece (seo-writing) or choosing what to
  target (keyword-research).
metadata:
  openclaw:
    emoji: "🩺"
---
# SEO Audit — what stops this site from being found, ranked by what it costs

Most sites do not need a hundred SEO tips; they need the five problems that
actually keep their pages out of the results, in order. This skill reads the
live site from the outside — the way a crawler and a searcher meet it — and
returns those problems with the page, the evidence and the fix.

## Related skills
- **keyword-research** — what the site should rank for; an audit says
  whether it can.
- **seo-writing** — rewrites a page the audit flagged as thin or off-intent.
- **build-report** — when the audit is a document someone else will read.
- **topic-watch** — re-runs the checks on a schedule and reports what changed.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A site that should get search traffic and does not, or lost some.
- A redesign or migration about to ship, or just shipped.
- **Do NOT use** to promise rankings, to run anything against a site the
  person does not own or manage, or to submit anything to a search console.
  You read; the person (or their developer) changes the site.

## Workflow
1. **Scope.** The domain, the pages that earn money or leads, the market and
   language. Ask once if unknown; otherwise take the home page and what it
   links to.
2. **Can it be crawled?** `web_fetch` `/robots.txt` and the sitemap(s) it
   names (or `/sitemap.xml`). Note disallowed paths that hold real pages, a
   missing or stale sitemap, sitemap URLs that redirect or 404.
3. **Sample the pages that matter.** Up to ~30 URLs: the money pages, the
   top-level navigation, a few deep ones from the sitemap. For each,
   `web_fetch` and record: status code and redirects, `<title>`, meta
   description, H1, canonical, `noindex`/`nofollow`, `hreflang` where the
   site is multilingual, word count of the main content, internal links
   in and out, images without `alt`.
4. **Is it in the index?** `web_search` with `site:` for the domain and for
   the key pages. A key page that does not appear is the first finding to
   explain.
5. **Find the patterns, not the instances.** Duplicate or missing titles,
   canonicals pointing elsewhere, pages competing for the same query
   (cannibalisation), thin pages, orphan pages (in the sitemap, linked from
   nothing), redirect chains, mixed `http`/`https` or `www` variants.
6. **Speed and mobile, as the person can check them.** If PageSpeed numbers
   are available through `web_fetch` of the public PageSpeed Insights API,
   use them for the key templates; otherwise name it as unchecked rather
   than guessing.
7. **Rank the findings** by Severity below, then write them up under Output.

## Standards
- Every finding names the URL(s) and shows the evidence — the tag, the
  status code, the search result. "Your titles could be better" is not a
  finding.
- Patterns over lists: "41 product pages share one title" beats 41 rows.
- Say what you could not check (logged-in pages, Search Console data, server
  logs) instead of implying the audit covered it.
- Never promise a ranking, a traffic number or a date. Say what the fix
  removes as an obstacle.
- Fetch politely: a sample, not a crawl of every URL; never more than a few
  requests a second.

## Severity
- **Critical** — pages that should rank cannot be indexed (noindex, blocked,
  404, canonical elsewhere).
- **High** — indexed but misread or competing with itself (missing or
  duplicate titles on key pages, cannibalisation, thin money pages).
- **Medium** — weakens results (meta descriptions, internal linking, slow
  templates, redirect chains).
- **Low** — hygiene (alt text, minor heading order).

## Output
- **Three lines first**: is the site findable, the one problem that costs the
  most, and what to fix this week.
- **Findings table**: severity · issue · pages affected (count + examples) ·
  evidence · fix · who does it (content / developer).
- **Not checked** — what an audit from outside cannot see, and what export
  would let you check it (Search Console performance, coverage report).
- Save the full table with `orch-files` when it runs past a screen.

## Defaults
- No pages named → the home page, its main navigation and five sitemap URLs.
- Multilingual site → audit the person's main market first; flag `hreflang`
  as one finding, not one per page.
- Re-audit → compare with the last saved audit and lead with what changed.
