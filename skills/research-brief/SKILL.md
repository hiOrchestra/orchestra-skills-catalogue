---
name: research-brief
version: 0.1.0
description: >-
  Turn a research question into a structured, sourced brief — corroborated
  findings with a clear bottom line, not a link dump. Use when the user says
  "research", "look into", "find out about", "brief me on", "background on", or
  "what do we know about" a topic, company, market, competitor, or person and
  wants a synthesized answer with sources. Not for a single quick fact.
triggers:
  - research
  - look into
  - find out about
  - brief me on
  - background on
  - what do we know about
  - deep dive
  - competitive analysis
  - market research
metadata:
  openclaw:
    emoji: "🔎"
requires:
  bins: []
  env: []
  config: []
---

# Research Brief — question → sourced, synthesized brief

Produce a decision-useful brief on a topic, not a pile of links. Scope to the
question and how it will be used, gather from several angles, corroborate the
important claims, and deliver a structured brief with sources and a clear bottom
line. Say what is known, how confident you are, and what is still open.

## Related skills
- **build-report** — when the deliverable should be a polished document
  (DOCX/PDF/deck) rather than an inline/file brief, hand the findings to it.
- **content-plan** — when the goal is to plan content, not to research a topic.
- **analyze-data-quality** — when the question is really "can I trust this
  dataset?", use that instead of researching the web.
- **fact-check** — when the ask is to verify one specific claim (true/false)
  rather than to synthesize a broad picture, hand it to fact-check.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user wants *synthesized knowledge* on a topic/company/market/person, with sources.
- Triggers: "research X", "look into Y", "brief me on Z", "background on…", "what do we know about…", "competitive/market analysis".
- **Do NOT use** for a single quick fact you can answer directly, or for turning
  already-known findings into a document (that is build-report).

## Workflow
1. **Frame the question + its use.** Pin down exactly what is being asked, who
   it is for, and what decision it informs (that sets depth and angle). If the
   ask is ambiguous, state a reasonable interpretation and proceed — do not stall.
2. **Plan the angles.** List the 3–6 sub-questions that actually answer it
   (e.g. for a company: what they do, traction, funding, team, competitors,
   risks). Research the angles, not just the headline.
3. **Gather (multi-source).** Use `web_search` to find sources and `web_fetch`
   to read the primary ones. Prefer official/primary sources over aggregators.
   Capture each source's URL, title, and date as you go.
4. **Corroborate & weigh.** Cross-check important claims across ≥2 independent
   sources. Note disagreements. Weigh source credibility and recency.
5. **Synthesize.** Turn findings into a narrative that answers the question —
   patterns, not a source-by-source dump. Separate fact from inference.
6. **Deliver** in the structure under Output.

## Standards
- Every non-obvious claim carries a source (title + URL).
- Distinguish **fact** (sourced) from **inference** (your reasoning) from
  **speculation** (flag it as such).
- Recency matters: note dates, and flag anything that may be stale.
- Important claims need ≥2 independent sources; single-sourced claims are flagged.
- Never fabricate a source, quote, or statistic. If you cannot verify something,
  say so plainly rather than guessing.

## Confidence labels
Tag each key finding:
- **High** — multiple independent, credible, recent sources agree.
- **Medium** — credible but limited, older, or only partially corroborated.
- **Low** — single source, contested, or speculative — call it out.

## Output
Structure the brief:
- **Bottom line** — 2–4 sentences directly answering the question.
- **Key findings** — bullets, each with its source(s) + confidence label.
- **Details / context** — as much as the use warrants, no more.
- **Open questions / gaps** — what you could not confirm and what would resolve it.
- **Sources** — numbered list (title — URL — date).

Substantial brief → save it as a file via `orch-files` and post a short summary
pointing at it. Quick brief → deliver inline. Match the depth to the ask.

## Defaults
- Breadth first, then depth on the highest-signal threads; time-box the rest.
- Prefer primary/official sources; treat forums/social as leads to verify.
- State assumptions when the question is ambiguous; keep moving.
- A brief with 5 well-sourced, corroborated points beats 20 unverified ones.
