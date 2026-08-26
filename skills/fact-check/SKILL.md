---
name: fact-check
version: 0.1.0
description: >-
  Verify a specific factual claim — or a list of claims — against primary
  sources and rule each True / False / Misleading / Unverifiable with evidence
  and a confidence level. Use when the user says "fact-check this", "is it
  true that…", "verify this claim", "did X really happen", "debunk", "is this
  accurate", or pastes a statement/quote/stat and wants it checked, "check
  whether", "verify these numbers". Not for open-ended research on a topic
  (that is research-brief), and not for opinions or predictions that cannot be
  verified.
metadata:
  openclaw:
    emoji: "✅"
---
# Fact-Check — verify specific claims against primary sources

Take a specific claim (or a list of them) and rule on each one: True, False,
Misleading, or Unverifiable, backed by primary-source evidence and a confidence
level. The job is a verdict with proof, not a topic survey — check what was
actually asserted, and be honest about what you cannot confirm.

## Related skills
- **research-brief** — when the user wants *synthesized knowledge* on a topic
  ("brief me on…", "what do we know about…") rather than a verdict on a specific
  assertion. Fact-check answers "is this true?"; research-brief answers "what's
  the picture?". If a claim needs broad context to even interpret, gather it the
  research-brief way, then rule.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user hands you a concrete, checkable assertion — a statement, quote,
  statistic, headline, or a bullet list of them — and wants it verified.
- Triggers: "fact-check this", "is it true that…", "verify this claim/these
  numbers", "is this accurate", "did X really happen", "debunk this".
- **Do NOT use** for open-ended research on a subject (use research-brief), or
  for opinions, value judgments, and future predictions — those aren't
  verifiable facts. If a "claim" is actually an opinion, say so and stop.

## Workflow
1. **Extract the exact checkable assertion(s).** Restate each claim in your own
   words as a precise, testable statement, splitting compound claims into
   separate ones. Vague framing hides where a statement is right vs. wrong, so
   pin down the specific subject, number, date, and scope being asserted.
2. **Find primary/authoritative sources.** Use `web_search` to locate them and
   `web_fetch` to read the source itself — the original study, filing, dataset,
   official statement, or the on-the-record quote in context. Go to the source
   the claim rests on, not a headline about it, because paraphrases drift.
3. **Corroborate across ≥2 independent sources.** Confirm each claim against at
   least two sources that don't trace back to the same origin. One source (or
   several echoing one press release) can be wrong together; independence is
   what makes a verdict trustworthy.
4. **Rule each claim.** Assign a verdict (True / False / Misleading /
   Unverifiable) and a confidence, and state the evidence that decided it —
   quote or cite the specific figure/passage. Watch for the Misleading case:
   technically-accurate numbers stripped of context, cherry-picked dates, or
   right-fact-wrong-implication.
5. **Separate verified from unverified.** Keep what you confirmed distinct from
   what you couldn't — never round an Unverifiable up to True because it sounds
   plausible. Note what evidence *would* settle an open claim.
6. **Deliver** in the structure under Output.

## Standards
- Every verdict cites the specific evidence that decided it (source title + URL,
  and the exact figure or quoted passage) — a ruling without proof is an opinion.
- Go to the primary source. Treat aggregators, social posts, and AI summaries as
  leads pointing at a source, never as the source.
- Quote claims and evidence exactly; don't paraphrase a number or a quote into
  something the source didn't say.
- Distinguish "false" (contradicted by evidence) from "unverifiable" (no
  adequate source either way) — they are different verdicts, not the same doubt.
- Never fabricate a source, statistic, or quote. If sources conflict or the
  record is thin, say so and let it lower the confidence.

## Confidence & verdicts
Rule each claim:
- **True** — the assertion is accurate as stated.
- **False** — the assertion is contradicted by the evidence.
- **Misleading** — partly true but leaves a false impression (missing context,
  cherry-picked, or right fact / wrong implication).
- **Unverifiable** — no adequate primary source confirms or refutes it.

And tag each verdict with confidence:
- **High** — multiple independent, credible, primary sources agree.
- **Medium** — credible but limited, older, or only partially corroborated.
- **Low** — single source, contested, or indirect evidence — call it out.

## Output
Lead with the **verdict** for each claim, up front and unmissable. For a single
claim: the verdict + confidence in the first line, then the evidence, then the
sources. For a list: a one-line **verdict table** (claim → verdict → confidence)
first, then a short evidence paragraph per claim, then a numbered **Sources**
list (title — URL — date). Where a claim is Misleading, say plainly what's true
and what impression it wrongly creates.

Many claims or a formal write-up → save it as a file via `orch-files` and post a
short summary with the headline verdicts. A single quick check → answer inline.

## Defaults
- If the "claim" is an opinion or prediction, say it isn't fact-checkable and
  stop — don't manufacture a verdict.
- If a claim is ambiguous, state the most reasonable interpretation, check that,
  and note the assumption — don't stall.
- Prefer the most recent authoritative source, and flag when a claim was true at
  one time but is now stale.
- When you genuinely can't confirm, "Unverifiable" is the right answer — say so
  rather than guessing.
