---
name: content-plan
version: 0.1.0
description: >-
  Plan a content calendar or strategy for a channel, campaign, or period —
  audience, content pillars, formats, cadence, and a concrete dated schedule of
  pieces. Use when the user says "content plan", "content calendar", "editorial
  calendar", "what should I post", "plan my content", "social media strategy",
  or "content for next month/quarter". Not for writing an individual piece
  (write-article) or researching a topic from scratch (research-brief).
triggers:
  - content plan
  - content calendar
  - editorial calendar
  - plan my content
  - what should I post
  - social media strategy
  - content strategy
  - content for next month
  - posting schedule
metadata:
  openclaw:
    emoji: "🗓️"
requires:
  bins: []
  env: []
  config: []
---

# Content Plan — audience, pillars, cadence → a dated schedule

Turn a vague "we need to post more" into a plan someone can execute: who it's
for, the few themes worth owning, the formats and cadence that are actually
sustainable, and a concrete dated schedule of pieces. The deliverable is a
calendar, not a pep talk — every row has a date, a pillar, a format, and a
working title.

## Related skills
- **research-brief** — when you first need to understand the space (audience,
  competitors, what's working) before planning, run that and feed its findings
  in. This skill assumes you already know the ground or can learn it quickly.
- **write-article** — when the ask is to actually *draft* one of the pieces, not
  to plan the calendar. Plan here, then hand individual pieces to that.
- **build-report** — when the plan should ship as a polished document or deck
  for a client or stakeholder rather than an inline table, hand it the schedule.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user wants a *plan of what to publish over time* — a calendar, an editorial
  strategy, a posting schedule for a channel/campaign/period.
- Triggers: "content plan", "content calendar", "plan my content for Q3", "what
  should I post on LinkedIn", "social strategy", "editorial calendar".
- **Do NOT use** to write a single post or article (that's write-article), to
  research a topic with no publishing goal (research-brief), or to plan
  non-content project work (that's a general planning task).

## Workflow
1. **Clarify the brief.** Pin down goal (awareness, leads, retention…), audience,
   channel(s), timeframe, and cadence appetite. If the user is silent, state
   sensible assumptions (see Defaults) and proceed — a plan they can react to
   beats an interrogation.
2. **Learn the space (only if needed).** If you don't know the audience or what
   already works, use `web_search`/`web_fetch` on competitors and the channel,
   and `orch-database` to check past performance if the tenant has it. Skip this
   when the ground is already known — don't pad the plan with busywork.
3. **Define 3–5 content pillars.** The recurring themes the channel will own.
   Fewer, sharper pillars beat a scattershot list — they give the calendar a
   spine and make each piece easy to place. Tie each pillar to the goal and the
   audience's actual interest, not to what's easy to produce.
4. **Map formats to pillars.** Decide the format mix (e.g. how-to posts, short
   video, carousels, newsletters) per channel, and which pillars suit which
   formats. Match formats to where the audience is and what the team can sustain.
5. **Set a realistic cadence.** Choose frequency you can hold for the whole
   timeframe — a plan that collapses in week two is worthless. Bias toward
   consistency over volume.
6. **Build the dated schedule.** Produce a table: one row per piece, spread
   across the timeframe, balanced across pillars, with a date, channel, pillar,
   format, and a working title/hook.
7. **Seed the first few pieces.** For the earliest 2–3 slots, add a one-line angle
   or key point so the user can start immediately, not just admire the grid.

## Standards
- Every scheduled row is concrete: a real date, a pillar, a format, a working
  title — no "TBD post" filler.
- Pillars and cadence trace back to the stated goal and audience; if you invented
  either, say which assumption it rests on.
- Cadence is honestly sustainable for the timeframe and team — flag it if the
  requested frequency looks unrealistic rather than quietly promising it.
- Coverage is balanced: no single pillar swallows the calendar unless the goal
  demands it.
- Don't fabricate performance data or audience claims; if you didn't verify
  something, mark it as an assumption.

## Output
- **Overview** — goal, audience, channel(s), timeframe, cadence in a few lines.
- **Pillars** — the 3–5 themes, each with a one-line rationale.
- **Format & cadence** — the mix per channel and how often you'll post.
- **Schedule** — the dated table (Date · Channel · Pillar · Format · Working
  title), the heart of the deliverable.
- **First pieces** — 2–3 seeded angles to start now.
- **Open questions** — anything you assumed that the user should confirm.

A full calendar (a month+ or multi-channel) → save it as a file via `orch-files`
and post a short summary pointing at it. A short or single-channel plan →
deliver inline. If the user wants a client-ready document or deck, hand the
schedule to **build-report**.

## Defaults
- If goal is unstated, assume awareness/engagement for the named channel.
- If timeframe is unstated, plan the next 4 weeks.
- If cadence is unstated, propose a modest sustainable one (e.g. 2–3×/week for
  social, weekly for a newsletter) and let the user dial it up.
- Prefer fewer, well-differentiated pillars over an exhaustive list.
- One channel done well beats spreading thin across five — plan for what the
  user can actually maintain.
