---
name: proofread-edit
version: 0.1.0
description: >-
  Copy-edit and tighten an existing draft — grammar, clarity, concision, tone,
  consistency — and return a cleaner version plus a short list of the changes.
  Use when the user says "proofread", "edit this", "copy-edit", "clean this
  up", "tighten this", "polish", "fix the grammar", or hands you text and asks
  for a once-over, "give this a once-over", "make this read better". Not for
  writing from scratch, and not for checking whether the content is true.
metadata:
  openclaw:
    emoji: "🖊️"
---
# Proofread & Edit — tighten a draft, keep the author's voice

Take an existing draft and return a cleaner version — correct, clear, and tight —
without rewriting it into your own voice. The author still recognizes their
words; they just read better. Every substantive change is listed so they can
accept or reject each one, and anything that reads as a factual claim gets
flagged rather than silently "corrected."

## Related skills
- **write-article** — when there is no draft yet and the job is to *produce*
  long-form content from a brief or outline. Proofread-edit improves text that
  already exists; write-article creates it. If the "draft" is a skeleton or a
  few notes, that is a writing job, not an editing one.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user hands you existing text — a post, email, doc, section — and wants it
  cleaner, tighter, or more correct.
- Triggers: "proofread", "edit this", "copy-edit", "clean this up", "tighten",
  "polish", "fix the grammar", "make this read better".
- **Do NOT use** for drafting from scratch (that is write-article), or for
  verifying that claims are *true* — an editor fixes how a sentence reads, not
  whether its facts hold. When a line asserts a checkable fact, flag it for
  verification rather than judging it here.

## Workflow
1. **Read the whole draft first, and pin the target.** Note who it is for, the
   register (formal / casual / technical), and the author's voice. You are
   preserving that voice, so you have to hear it before you touch it. If the
   audience or tone is unclear, infer it from the draft and say what you assumed.
2. **Fix mechanics.** Grammar, spelling, punctuation, agreement, tense, and
   consistency (one spelling of a term, one date/number format, parallel lists).
   These are unambiguous corrections — the low-risk, high-trust layer.
3. **Tighten.** Cut filler and redundancy, replace wordy or passive
   constructions with direct ones, and split sentences that lost the reader.
   Concision is the highest-value edit; most drafts are 10–20% too long.
4. **Improve flow and structure lightly.** Fix ordering, transitions, and
   headings only where they genuinely help. Restructure sparingly — a heavy
   reorganization is closer to rewriting, so propose it rather than imposing it.
5. **Guard the voice.** After each pass, check you have not flattened the
   author's phrasing into generic prose. When unsure between two valid wordings,
   keep theirs.
6. **Flag, don't fix, the factual and the risky.** Mark claims that should be
   verified, ambiguous statements only the author can resolve, and places where
   your edit might change the meaning. Surface these instead of guessing.
7. **Deliver** the revised text plus a labeled change summary (see Output).

## Standards
- **Preserve meaning and voice.** An edit that changes what the author was
  saying is a defect, not an improvement. If a fix risks the meaning, flag it.
- **Every substantive change is inspectable.** The author can see what changed
  and why, and accept selectively. Do not bury edits in a wall of clean text.
- **Correct only what is actually wrong.** Do not impose stylistic preferences
  as if they were rules; "different" is not "better."
- **Never invent content.** You may cut and rephrase, not add new facts, quotes,
  or claims. Gaps get flagged, not filled.
- **Stay in lane.** Factual accuracy is out of scope here — flag it for
  fact-checking rather than ruling on it.

## Severity
Label each change so the author can triage:
- **Mechanical** — objective correctness (grammar, spelling, punctuation,
  consistency). Safe to accept wholesale.
- **Clarity** — concision, word choice, sentence-level readability. Judgment
  calls that improve the line without changing intent.
- **Structural** — reordering, merging/splitting sections, cutting or moving
  paragraphs. Highest-impact and highest-risk — worth the author's attention.

## Output
- **Revised draft** — the clean version, ready to use.
- **Change summary** — a short list of the substantive edits, each tagged
  *Mechanical / Clarity / Structural*, grouped or in document order. Skip the
  trivia (no need to log every comma); capture what the author would want to
  review.
- **Flags** — factual claims to verify, ambiguities needing the author's call,
  and any edit that may have shifted meaning.

Long draft, or the user wants to keep both versions → save the revised text as a
file via `orch-files` and give the change summary inline. Short passage →
deliver both inline. Match the effort to the length.

## Defaults
- Light touch beats heavy hand: prefer the smallest edit that fixes the problem.
- When two wordings are equally valid, keep the author's.
- Preserve deliberate stylistic choices (a fragment for emphasis, a casual
  aside) — edit toward the draft's own register, not a generic one.
- If the draft needs more rewriting than editing, say so and propose the bigger
  change rather than quietly performing it.
- Don't ask for a style guide you weren't given; infer house style from the
  draft and note the conventions you enforced.
