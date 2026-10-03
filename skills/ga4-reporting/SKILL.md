---
name: ga4-reporting
version: 0.1.0
description: >-
  Answer website and app traffic questions from the person's Google
  Analytics 4 property through their connected account — sessions, users,
  sources and channels, landing pages, conversions and key events, devices
  and countries, trends against the previous period — and explain what
  changed and the likely why, with every figure tied to the report that
  produced it. Read-only. Use when the user says "Google Analytics", "GA4",
  "traffic", "where do visitors come from", "conversions", "what changed
  this week", "top pages", "bounce", "campaign performance". Needs Google
  Analytics connected. Not for search queries (search-console).
metadata:
  openclaw:
    emoji: "📉"
  orchestra:
    requires:
      integrations:
        - google_analytics
---
# GA4 Reporting — what happened on the site, and the likely why

Analytics is useful when it answers a question someone actually has: did the
launch bring visitors, which channel converts, why did traffic drop on
Tuesday. This skill runs the GA4 reports that answer it, compares with the
right baseline, and separates what the data shows from what it suggests.

## Related skills
- **search-console** — what people searched before they arrived.
- **build-dashboard** — a standing view on a Canvas page.
- **seo-audit** — when organic traffic dropped and the site may be why.
- **orch-composio** — the tool every call goes through.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Traffic, acquisition, engagement and conversion questions; weekly reports.
- **Do NOT use** to change the GA4 configuration (events, conversions,
  filters, users); propose and let the person do it.

## Workflow
1. **Check the connection**: `orch-composio connections`; not connected →
   say so and stop. List properties (`GOOGLE_ANALYTICS_LIST_ACCOUNT_SUMMARIES`
   or `GOOGLE_ANALYTICS_LIST_PROPERTIES`) and use the one the procedure names.
2. **Confirm the schema before first use** (`orch-composio schema --slug
   GOOGLE_ANALYTICS_RUN_REPORT`). Use `GOOGLE_ANALYTICS_GET_METADATA` to get
   valid dimension and metric names rather than guessing them.
3. **Run the report the question needs** (`GOOGLE_ANALYTICS_RUN_REPORT`;
   `GOOGLE_ANALYTICS_RUN_REALTIME_REPORT` for "right now";
   `GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT` for a funnel), always with a
   comparison period.
4. **Explain the change**: which channel, page, country or device carried
   it; check annotations and known events (a campaign, a release, tracking
   changes) before concluding.
5. **Say what the data cannot tell**: sampling, consent-mode gaps, thresholds
   that hide small numbers.

## Standards
- Every figure names its metric, period and comparison.
- Users, sessions and events are different things; never mix them in one
  sentence.
- A change in tracking is ruled out before a change in behaviour is claimed.
- Read-only, always.

## Output
The answer in two lines · a small table (metric, this period, previous,
change) · what drove it · caveats.

## Defaults
- Period → last 7 complete days vs the 7 before; monthly reports vs the
  previous month and the same month last year.
- Timezone → the property's.
