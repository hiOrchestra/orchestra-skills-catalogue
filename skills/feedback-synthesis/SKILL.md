---
name: feedback-synthesis
version: 0.1.0
description: >-
  Turn a pile of customer feedback — support tickets, reviews, survey
  answers, sales call notes, interview transcripts, feature requests — into
  the few themes that matter: what people struggle with or ask for, how
  often, who (which segment), in their own words, and what it suggests
  doing; every theme counted and quoted, never made up. Use when the user
  says "what are customers saying", "synthesize feedback", "themes from
  these reviews", "analyze this survey", "top feature requests", "voice of
  the customer", "what should we build next". Not for one interview's notes
  (meeting-notes) or a market study (research-brief).
metadata:
  openclaw:
    emoji: "🧩"
---
# Feedback Synthesis — what customers keep saying, counted and in their words

Feedback is most useful when it stops being a pile and becomes a ranked list:
the five problems people keep running into, how many said each, which kind of
customer, and the quote that makes it real. This skill reads every item,
codes it, counts it, and returns themes a team can act on — with the line
between what customers said and what you infer kept visible.

## Related skills
- **product-spec** — a theme worth acting on becomes a spec.
- **distill** — when the input is one long document, not many items.
- **analyze-data-quality** / **explore-dataset** — when the feedback comes
  with structured data (NPS, plan, revenue) worth slicing.
- **build-report** — when the synthesis is a document for others.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Any batch of qualitative feedback, from ten items to a few thousand.
- **Do NOT use** to score individual customers or employees, or to quote
  anyone by name outside the team without their consent.

## Workflow
1. **Gather and describe.** What the items are, where from, the period, how
   many, what is known about each author (plan, segment, tenure). Say what
   is missing — e.g. only complaints, only one channel — because it bends
   every conclusion.
2. **Read a sample first** (~30 items) and draft a codebook: short labels
   for problems, requests, praise, and the job the customer was trying to do.
3. **Code every item** with one or more labels; add labels as new patterns
   appear and recode the early items. Keep a note of the quote that best
   shows each label. For large sets, store items and codes in a table
   (`orch-database`, table `feedback_items`) so counts are queries, not
   recollection.
4. **Group labels into themes** — the underlying problem, not the requested
   feature ("I can't find last month's invoice" and "add search to billing"
   are one theme).
5. **Count and slice** each theme: items, share of the set, which segments,
   trend over the period if dated.
6. **Say what it suggests** — separately from the findings — and what you
   would want to learn next.

## Standards
- Every theme has a count and at least one verbatim quote; no quote is
  invented, edited for meaning or attributed to the wrong segment.
- Frequency is not importance: a rare theme from your best customers or a
  churn reason can outrank a common nice-to-have — say which you are using.
- Keep praise; knowing what to protect is a finding.
- Remove names, emails and anything identifying from quotes shown outside
  the team.

## Confidence
- **High** — many items, several segments, consistent wording.
- **Medium** — clear but from one channel or one segment.
- **Low** — a handful of items; a lead to investigate, not a conclusion.

## Output
- **Top themes** (5–8): theme · count and share · segments · trend · two
  quotes · confidence.
- **What it suggests** — 3 bullets, labelled as interpretation.
- **Gaps** — what the set cannot tell you and how to find out.
- The coded table saved with `orch-files` or kept in `feedback_items`.

## Defaults
- No segments known → count by channel and say segments would sharpen it.
- Mixed languages → code in the original, report in the person's language.
- Repeat synthesis → compare with the last one and lead with what moved.
