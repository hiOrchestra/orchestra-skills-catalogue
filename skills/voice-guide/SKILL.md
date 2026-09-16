---
name: voice-guide
version: 0.1.0
description: >-
  Capture how a person or brand actually sounds — from things they already
  wrote — into a short voice guide, and write against it so every piece reads
  as theirs. Use when the user says "write in my voice", "sound like me",
  "match our tone", "our style guide", "this doesn't sound like us", hands you
  samples of their writing, or before the first piece you write for anyone.
  Not for drafting the piece itself (write-article) or copy-editing an
  existing draft (proofread-edit).
metadata:
  openclaw:
    emoji: "🎙️"
---
# Voice Guide — their samples → a voice you can write against

A content writer's first job is to disappear: the reader should hear the
person, not the writer. This skill turns what the person already wrote into a
one-page guide — how they sound, what they never say, what a paragraph of theirs
looks like — and keeps it current. Every piece is written against it and
checked against it before it goes out.

## Related skills
- **write-article** — writes the piece; it reads the voice guide first.
- **proofread-edit** — tightens a draft; it keeps the voice, it does not impose one.
- **content-plan** — plans what to write; the voice guide says how it will sound.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Before the first piece for a new person or brand, and whenever they say a
  draft "doesn't sound like us".
- When they hand you samples: posts, emails, a talk transcript, a bio.
- **Do NOT use** to invent a voice from nothing: with no samples, ask for
  three things they wrote and liked, or write one short paragraph two ways and
  let them pick — never a template voice.

## Workflow
1. **Collect samples.** Ask for 3–5 pieces they wrote themselves and are happy
   with (not ghostwritten, not edited by someone else). Save them in
   `orch-files` under `voice/samples/` so the guide can be rebuilt later.
2. **Read for pattern, not opinion.** Note: sentence length and rhythm,
   paragraph length, person (I / we / you), register (formal, plain, playful),
   how they open and close, recurring words and images, what they never do
   (exclamation marks, jargon, hedges), how they handle numbers and names.
3. **Write the guide** — one page, in the shape under Output. Quote two or
   three of their own sentences as the reference, with the source.
4. **Confirm it with them.** Show the guide and ask what is wrong. What they
   strike matters more than what they keep.
5. **Keep it.** Save `voice/VOICE.md` in `orch-files`. Read it before every
   piece; check the draft against the "never" list before delivering.
6. **Update it when they correct you.** A correction on a draft ("we don't say
   'leverage'") goes into the guide the same day, with the date — so the same
   note is never given twice.

## Standards
- The guide describes what the samples show, not what the writer prefers. If
  the samples disagree with what the person says about themselves, show both
  and ask.
- Every rule cites a sample. A rule with no example is an opinion.
- The "never" list is short and real — five things they truly avoid beat
  twenty generic ones.
- Do not flatten a voice into "clear and professional". If their sentences run
  long and warm, the guide says so, and the drafts do too.
- A draft is checked against the guide before delivery: opening, closing,
  the never-list, one paragraph read aloud.

## Output
`voice/VOICE.md`, one page:
- **Who is speaking, to whom** — one line.
- **Sounds like** — 4–8 observations, each with a quoted sample sentence.
- **Never** — the short list, with the reason if they gave one.
- **Reference paragraph** — one of theirs, verbatim, with the source.
- **Corrections log** — dated lines added as they correct drafts.

## Defaults
- No samples yet → ask for three; meanwhile write in plain, short sentences,
  first person if they write as a person, and say the voice is provisional.
- Two voices (brand and founder) → two guides, named; ask which one a piece is in.
- When a draft fails the check, fix it before delivering — do not deliver with
  a note saying it may sound off.
