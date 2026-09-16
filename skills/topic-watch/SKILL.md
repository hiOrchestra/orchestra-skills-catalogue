---
name: topic-watch
version: 0.1.0
description: >-
  Keep a standing watch on a topic, company, competitor, regulation or person
  — a baseline of what is known, a scheduled check, and a report that says only
  what changed, with sources, or "nothing" when nothing did. Use when the user
  says "keep an eye on", "monitor", "alert me when", "track what X does",
  "competitor watch", "let me know if anything changes", "weekly update on".
  Not for a one-time deep dive (research-brief), a single claim (fact-check),
  or watching wallets or prices (wallet-watch).
metadata:
  openclaw:
    emoji: "🛰️"
---
# Topic Watch — a baseline, a schedule, and only what changed

Monitoring is a routine, not a research project: the value is in the
difference between this week and last, reported briefly, on time, with the
source. This skill sets the baseline, creates the routine with `orch-jobs`, and
holds the report to one rule — say what changed and how sure you are, and say
"nothing" when nothing did, because a missing report reads as a broken watch.

## Related skills
- **research-brief** — builds the baseline when the topic is new to you.
- **evaluate-source** — grades the sources the watch will trust.
- **wallet-watch** — the same shape for addresses and balances.
- **orch-jobs** — the routine itself: schedule, notification, storage.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The person wants to know when something changes, on a cadence, without asking.
- **Do NOT use** for "tell me everything about X" once — that is a brief.
  Do not create a watch whose every report would need the person's review to
  be useful; propose a brief instead.

## Workflow
1. **Define the watch with them**: the subject (named precisely — the company,
   the product line, the bill number), what counts as a change worth telling
   (a launch, a price, a hire, a filing, a ruling), the cadence and time, where
   the report goes (the channel they read) and whether to store findings in a
   table. Ask what they do NOT want to hear about.
2. **Set the baseline.** Research the current state (`research-brief` if the
   subject is new) and write it to `orch-files` as `watch/<slug>/baseline.md`:
   what is known as of today, the 3–8 sources the watch will check each time
   (graded with `evaluate-source`), and the search queries that find news.
3. **Create the routine** with `orch-jobs create`: name it for the subject,
   the message says to read the baseline, check the named sources and queries,
   compare, and report only differences; `--notify` the channel they chose;
   `--table` if they want a log. Ask for their timezone.
4. **Each run**: check the sources and queries, compare against the baseline,
   grade anything new, write the report in the shape under Output, and update
   the baseline with what was confirmed and the date.
5. **Tune, do not restart.** When they say "too much" or "you missed X",
   change the change-criteria in the baseline and say what changed.

## Standards
- A change is reported with its source and date, and with a grade if the
  source is not one of the trusted list.
- Rumours are reported as rumours, in their own line, or not at all — the
  person decides once which they want.
- "Nothing changed" is a report. It is sent, and it is one line.
- The baseline is updated after every run; a watch without a current baseline
  repeats old news.
- Never expand the subject on your own: a watch on a company does not become
  a watch on its industry.

## Output
Per run, in the channel they chose:
- **Subject · period** — one line.
- **Changed** — one line per change: what, since when, source, grade. Or
  "Nothing since <date>."
- **Worth a look** (optional) — 1–2 items below the threshold, marked as such.
- **Next check** — date.

## Defaults
- Cadence unknown → weekly, Monday morning in their timezone; say so.
- Channel unknown → ask; a watch nobody reads is noise.
- Sources: official pages and filings first, then two reputable outlets for
  the sector, then a news query; social only if they ask.
