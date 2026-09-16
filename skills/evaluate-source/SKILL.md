---
name: evaluate-source
version: 0.1.0
description: >-
  Judge how far a source can be trusted before a claim from it is used — is it
  primary or secondhand, who is behind it and what they gain, how it knows what
  it says, how old it is, how it has held up — and grade it. Use when the user
  says "is this source reliable", "can we trust this", "who is behind this
  site", "is this a good source", "how credible is", or whenever a brief rests
  on a source you have not weighed. Not for checking whether a specific claim
  is true (fact-check) or for the research itself (research-brief).
metadata:
  openclaw:
    emoji: "🧭"
---
# Evaluate Source — how much weight this source can carry

A brief is only as good as its weakest load-bearing source. This skill is the
researcher's habit of weighing a source before quoting it: where the
information comes from, who benefits from it being believed, whether it is the
document itself or someone's account of it, and how it has held up. The result
is a grade the brief carries next to the claim.

## Related skills
- **research-brief** — uses this on every source that carries an important claim.
- **fact-check** — tests the claim; this skill tests the source.
- **topic-watch** — a standing watch names its trusted sources once, using this.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Before an important claim rests on a source, especially a single one.
- When the person asks whether something can be trusted.
- **Do NOT use** to dismiss a source because of its type: a forum post by the
  engineer who built the thing can outrank a newspaper's summary of it. Weigh
  the specific document, not the category.

## Workflow
1. **Identify what it is.** Primary (the filing, the dataset, the statement by
   the actor, the paper) or secondary (a report about it). If secondary, find
   and read the primary with `web_fetch`; the secondary becomes a lead.
2. **Who and why.** Who published it, what they gain if it is believed, who
   paid for it. Read the about page, the byline, the disclosures.
3. **How it knows.** Is the method visible — data, interviews, documents,
   firsthand observation? Can it be checked? A claim with no visible method is
   an assertion.
4. **When.** Date of publication and of the underlying facts. A 2023 figure in
   a 2026 article is a 2023 figure.
5. **Track record and independence.** Has this source been right before on
   this kind of claim? Is it independent of the other sources you hold, or do
   they all trace to the same origin (one press release, ten articles)?
6. **Grade it** on the scale below, in one line, and attach the grade wherever
   the claim appears.

## Standards
- Two sources that copy the same origin are one source.
- "Official" is not "true": an official source is authoritative about its own
  positions and figures, and interested about everything else.
- Anonymous sourcing lowers the grade; it does not zero it. Say what the
  outlet's record is.
- Aggregators, AI summaries and encyclopedias are leads; the grade belongs to
  what they cite.
- Never grade a source you have not opened.

## Grades
- **A** — primary, method visible, independent, current. Carries a claim alone.
- **B** — credible secondary or primary with a stake; needs one independent
  corroboration for an important claim.
- **C** — unclear method or strong interest; a lead to verify, not a source to cite.
- **D** — known unreliable, undated, or unverifiable; not used, or used only
  to say that the claim circulates.

## Output
One line per source: `[grade] title — publisher — date — what it is (primary /
secondary) — the reason for the grade in ten words`. For a single asked-about
source, the line plus a short paragraph on what it can and cannot be trusted
for.

## Defaults
- Many sources → grade the ones under the important claims; list the rest.
- Grade unknown after reading → C, and say what would raise it.
- Conflicting sources of equal grade → report both; the brief carries the
  disagreement.
