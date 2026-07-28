---
name: write-article
version: 0.1.0
description: >-
  Draft long-form written content — a blog post, article, or newsletter — from a
  brief, outline, or topic, in the requested voice and length. Use when the user
  says "write a blog post", "draft an article", "write the newsletter", "turn
  this outline into a post", "write me a piece on", or "draft ~800 words on".
  Not for planning a whole content program (content-plan) or polishing an
  existing draft (proofread-edit).
triggers:
  - write a blog post
  - draft an article
  - write the newsletter
  - turn this outline into a post
  - write a piece on
  - draft ~800 words on
  - write me a post about
  - ghostwrite
metadata:
  openclaw:
    emoji: "✍️"
requires:
  bins: []
  env: []
  config: []
---

# Write Article — brief/outline → finished long-form draft

Turn a topic, brief, or outline into a publishable piece — a blog post, article,
or newsletter — in the audience, voice, and length the user asked for. The bar
is a draft that reads like it was written on purpose: a lede that earns the next
paragraph, a clear spine, and every factual claim it can stand behind.

## Related skills
- **content-plan** — when the user wants the whole program (audience, pillars,
  cadence, a dated calendar), plan it there first; this skill drafts one piece
  from that plan.
- **research-brief** — when the piece is fact-heavy and the facts aren't in hand,
  get a sourced brief first, then draft from it — don't research and write in one
  undisciplined pass.
- **proofread-edit** — the polish pass. Draft here, then hand off for the
  line-level copy-edit and tightening; don't try to do both jobs at once.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user wants a single long-form piece drafted: blog post, article, newsletter,
  ghostwritten opinion piece.
- Triggers: "write a blog post on…", "draft an article about…", "turn this outline
  into a post", "write the newsletter", "~800 words on…".
- **Do NOT use** for planning a content calendar or strategy (that is content-plan),
  for editing a draft the user already has (that is proofread-edit), or for a
  document deliverable like a formatted report or deck (that is build-report).

## Workflow
1. **Pin the brief.** Before writing a word, lock four things: audience (who
   reads this and what they already know), goal (what they should think/do after),
   voice (tone, person, formality — match any example the user gives), and length
   (target word count or read-time). These drive every later choice; guessing them
   wrong wastes the whole draft. If the user gave a brief or outline, read it;
   if any of the four is missing and can't be reasonably assumed, ask once.
2. **Get the facts straight — first.** If the piece makes factual, statistical, or
   sourced claims, gather them up front with `web_search` / `web_fetch` (or reach
   for **research-brief**), capturing sources as you go. Reading uploaded material?
   Use `orch-files`. Never invent facts, quotes, or numbers to fill a paragraph.
3. **Outline the spine.** Sketch the arc before drafting: lede angle, the 3–6
   sections that carry the argument, and the close. A piece with a deliberate
   structure reads better than one discovered mid-sentence.
4. **Draft it.** Open with a lede that gives the reader a reason to stay — a
   tension, a stake, a concrete image — not a throat-clear. Then write the body to
   the outline: one idea per section, transitions that connect, concrete over
   abstract, active voice. Hold the requested voice and length throughout. Close
   with a payoff or clear takeaway, not a summary of what they just read.
5. **Self-check against the brief.** Re-read as the target reader: does it hit the
   goal, sound like the requested voice, land near the target length, and is every
   claim supported? Fix structural misses now — a polish pass can't rescue a piece
   aimed at the wrong reader.
6. **Hand off for polish.** Note that a **proofread-edit** pass will tighten line
   by line; don't over-buff prose here at the expense of getting the structure and
   argument right.

## Standards
- The draft matches the requested **audience, voice, and length** — these are the
  contract, not suggestions.
- Every factual claim is one you can stand behind; sourced pieces cite where the
  numbers came from. Never fabricate facts, quotes, statistics, or sources.
- Structure earns its length: a strong lede, one idea per section, real
  transitions, a close that pays off. Cut anything that doesn't serve the goal.
- Concrete beats abstract; active beats passive; specific beats vague. Avoid filler
  ("in today's fast-paced world"), hedging, and the same three sentence shapes.
- If you assumed part of the brief, say so at handoff so the user can correct course.

## Output
- Deliver the draft in the piece's natural format (Markdown headings, sections).
- A short piece (a few hundred words, quick turnaround) → answer inline.
- A substantial piece, or one the user will edit/publish → save it via `orch-files`
  and post a brief note (title, word count, any assumptions) pointing at the file.
- Lead with the draft itself; keep process notes short and after it.

## Defaults
- Voice unstated → clear, warm, professional, second person where natural; match
  any sample the user provides over any default.
- Length unstated → ~700–900 words for a blog post/article, ~400–600 for a
  newsletter; confirm if it matters.
- Ambiguous brief → state a reasonable interpretation, draft, and flag the
  assumption rather than stalling with questions.
- Non-factual/opinion piece → skip the research step; factual piece with no facts
  in hand → get them first, don't wing it.
- One strong, well-shaped draft beats a longer one padded to hit a number.
