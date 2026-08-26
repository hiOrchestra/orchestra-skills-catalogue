---
name: distill
version: 0.1.0
description: >-
  Compress long source material — a document, transcript, thread, or paper —
  into a faithful, tight summary at a target length and for a target reader,
  bottom line first. Use when the user says "summarize", "distill", "TL;DR",
  "condense this", "give me the gist", "boil it down", "key takeaways", or
  "shorten" and points you at existing material, "what are the main points".
  Not for researching new information, and not for producing a formatted
  document.
metadata:
  openclaw:
    emoji: "🗜️"
---
# Distill — long source material → faithful, tight summary

Take source material the user already has and compress it into a summary that a
specific reader can act on: bottom line first, only what matters, meaning
preserved. A good distillation is shorter *and* faithful — it never invents,
never inverts a point, and never buries the through-line under detail.

## Related skills
- **research-brief** — when there is no source to compress yet and you need to
  go *find* the information (web research, corroboration, sources). Distilling
  summarizes what exists; researching gathers what doesn't.
- **build-report** — when the deliverable must be a polished, formatted document
  (DOCX/PDF/deck) rather than a summary answered inline or in a text file, hand
  the distilled content to it.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user hands you long material — a report, transcript, email thread, article,
  paper, meeting notes — and wants it shorter without losing the substance.
- Triggers: "summarize", "distill", "TL;DR", "condense", "the gist", "boil it
  down", "key takeaways", "shorten".
- **Do NOT use** to research a topic from scratch (that is research-brief), or to
  produce a formatted document deliverable (that is build-report). If the source
  is a dataset and the ask is really "what's in this data?", that is an analysis
  task, not a distillation.

## Workflow
1. **Read the whole source first.** Use `orch-files` to read the uploaded doc,
   transcript, or CSV — or `web_fetch` if the source is a URL. Read all of it
   before writing a word; summarizing from the first few paragraphs is how you
   miss the actual point or the caveat buried at the end. For very long files,
   read in chunks (`wc -c` then `sed -n`/`head -c`) so nothing is silently cut.
2. **Fix the reader and the purpose.** Who is this for and why do they need it —
   an exec who wants the decision, an engineer who wants the mechanism, a
   newcomer who wants orientation? That choice decides what "the point" is and
   what is safe to drop. If unstated, infer from context and state your read.
3. **Find the through-line.** Identify the single main message and the handful of
   points that actually carry it. Separate load-bearing content from supporting
   detail, examples, and repetition.
4. **Draft bottom-line-first.** Lead with the one thing the reader must take away,
   then the supporting points in descending importance. Never make them read to
   the end to learn what it was about.
5. **Cut to the target length.** Remove redundancy, hedging, and filler while
   preserving meaning — tighten wording, don't amputate substance. Hit the
   requested length (or pick a sensible one; see Defaults).
6. **Verify fidelity.** Check every claim against the source: no invented facts,
   no reversed positions, no false certainty where the source hedged. Note
   anything genuinely ambiguous in the source, and flag material you deliberately
   omitted if its absence could mislead.

## Standards
- **Faithful over clever.** The summary must say what the source says — attribute
  claims to the source, and never smuggle in your own opinion as if it were the
  author's.
- **Preserve caveats and qualifiers.** "Might," "in some cases," "not yet proven"
  carry meaning; dropping them turns a hedge into a false certainty.
- **Preserve the source's own conclusion**, even if you find it weak — distilling
  is not editorializing.
- **No fabrication.** Do not add numbers, names, or claims that aren't in the
  source. If the source is unclear, say so rather than resolving it for them.
- **Right length, not just short.** Compression that loses a load-bearing point
  has failed, even if it hit the word count.

## Output
- Lead with the **bottom line** — 1–3 sentences, the single main takeaway.
- Then **key points** — tight bullets in importance order, at the target length.
- Add **caveats / omissions** only if something dropped could mislead, or the
  source itself flagged uncertainty.
- Short source or "just give me the gist" → answer inline. Long source, or the
  user wants something to keep or forward → save the distillation as a file via
  `orch-files` and post the bottom line pointing at it.
- Match the shape to the ask: a one-line TL;DR, an exec paragraph, or a bulleted
  digest — give them the form they asked for.

## Defaults
- No length given → aim for ~10–20% of the source, or a half-page, whichever is
  tighter; offer to go shorter or longer.
- No reader given → assume a busy, informed generalist and lead with the decision
  or the "so what."
- Multiple sources → distill each briefly, then synthesize the shared through-line;
  note where they disagree rather than blending them into false consensus.
- When forced to choose, keep the point and cut the example — a faithful short
  summary beats a comprehensive long one.
