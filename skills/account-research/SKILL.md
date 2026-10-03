---
name: account-research
version: 0.1.0
description: >-
  Research a target company before anyone reaches out — what it does, its
  size and stage, what changed recently (funding, hires, launches, expansion,
  a new leader), the signs it has the problem the seller solves, who is
  likely to own that problem, and the honest reason to write now — from
  public sources, each fact linked; and score how well it fits the ideal
  customer. Use when the user says "research this account", "prospect
  research", "find companies like", "is X a good fit", "build a target
  list", "account brief", "who should we contact at". Not for writing the
  outreach (outreach-sequence) or a general market study (research-brief).
metadata:
  openclaw:
    emoji: "🎯"
---
# Account Research — why this company, why now, and who

Outreach that works starts from a reason the prospect would recognise: a
problem they visibly have, a change that makes it urgent, a person who owns
it. This skill finds that reason in public sources — or says plainly that
there is none and the account should wait.

## Related skills
- **outreach-sequence** — writes the messages from this brief.
- **topic-watch** — keeps watching an account for the trigger that makes
  now the right time.
- **evaluate-source** — when a fact's source is doubtful.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Before outreach to a named company, or to build a list of companies that
  fit the ideal customer profile.
- **Do NOT use** to collect personal information beyond a person's
  professional role: no personal addresses, phone numbers, family, health,
  or private social accounts. Do not guess email addresses; mark contact
  details unknown unless the person provides them or they are published for
  that purpose.

## Workflow
1. **The ideal customer profile, written.** Industry, size, geography, the
   problem, the signals that show it, who buys and who uses. Read it from
   the agent's procedure; ask if there is none.
2. **The company.** `web_fetch` its site (home, about, pricing, careers,
   news) and `web_search` for recent news, funding, launches, leadership
   changes, job posts. Record what it does, for whom, size, stage, markets.
3. **The signals.** Evidence it has the problem now: job ads for the role
   the product replaces or supports, a stack visible on its site, complaints
   in reviews, a growth step that strains a process, a regulatory change.
   Each signal with its link and date.
4. **The people.** The role(s) that would own the problem, and named people
   only from the company's own pages, press or professional profiles that
   are public — with the source. No guessing.
5. **Fit and timing.** Score against the profile (below), name the one
   reason to write now, or say there is none.
6. **List mode.** For "find companies like X": `web_search` for peers by
   category, market and size, then run steps 2–5 briefly for each, and rank.

## Standards
- Every fact has a link and a date; anything older than 12 months is
  labelled as old.
- Inference is labelled as inference ("likely uses …, because …").
- No invented personalisation: if nothing specific was found, the brief says
  so and outreach should not pretend otherwise.
- Respect opt-outs and do-not-contact lists the person keeps.

## Fit score
- **Strong** — matches the profile and shows a current signal.
- **Possible** — matches the profile, no current signal; watch it.
- **Poor** — outside the profile; say which criterion fails.

## Output
Per account: one-line what they do · size/stage/market · signals (with
links) · likely owner role and named people with sources · fit · reason to
write now (or "none yet") · open questions. Lists as a table saved with
`orch-files` or in `orch-database` (table `accounts`).

## Defaults
- No profile yet → draft one from the person's best three customers and ask
  for a yes before scoring.
- Many accounts requested → the top ten by fit first, the rest on request.
