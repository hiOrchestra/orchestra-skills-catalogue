# The craft floor

Direction is what makes a page distinctive. This is what makes it *good*, and it
is the same underneath every direction on `{baseDir}/references/aesthetics.md`.
None of it is opinion — it is settled craft with a literature, cited at the end.

## Measure, before anything else

Running text sits between **45 and 75 characters per line**, 66 being the
classic target. Wider and the eye loses the return; narrower and rhythm breaks.
This single number decides your column widths, so set it first and lay out
around it — not the other way round.

Set it with `max-width` in `ch`, not by guessing pixels: `max-width: 66ch`.

## Scale, and the size of the jump

Pick a ratio and stay on it. A type scale is a small set of sizes derived from
one step (1.2 minor third for dense interfaces, 1.25–1.333 for editorial,
1.5+ only when you want drama). Sizes off the scale are the single most common
tell of a page assembled rather than designed.

Hierarchy is **weight, colour, space and position** before it is size. Making
every distinction with a bigger number is what produces the shouting hero
followed by undifferentiated grey.

## Vertical rhythm

Line-height for body text lands near **1.4–1.6**; display sizes go tighter,
often below 1.1, because large type needs less leading, not more. Space between
blocks should be multiples of a base unit so the page has a pulse. Space *above*
a heading is always larger than the space below it — the heading belongs to what
follows, and getting this backwards makes a page feel unglued even when nothing
is obviously wrong.

## The grid is the invisible part

Decide the columns and hold them. Every top-level block starting on the same
left edge is what "professional" actually looks like from twenty feet away —
and the failure is exactly what the `cloudflare` verifier's *text lines up on a
column* check exists to catch. Break the grid deliberately and rarely: one
full-bleed image, one pull-quote in the margin. A break that happens twice is
not a break, it is an inconsistency.

## Colour

Work in roles, not swatches: ground, ink, muted ink, line, accent, and the
semantic set (good / warning / critical) which is separate from your accent and
never doubles as it.

Neutrals are chosen, not inherited. A pure mid-grey reads as unconsidered; give
your greys a slight bias toward the accent's hue and the page reads as one
family. Pure white and pure black are legitimate grounds when the subject wants
them, but pick them on purpose.

Contrast is not negotiable: **4.5:1 for body text, 3:1 for large text and for
meaningful non-text** (WCAG AA). Check it rather than eyeballing it — mid-tone
accents on mid-tone grounds fail far more often than they look like they do.

## Type that reaches the reader

A font stack naming a face that ships with only one operating system is a
different design on every other machine. `Iowan Old Style`, `Baskerville`,
`Palatino`, `Avenir`, `Segoe UI`, `Calibri` — all of these render for their own
platform's users and silently fall back for everyone else.

Either ship the face (`@font-face`, subset, `font-display: swap`) or build on
one that is genuinely everywhere. Do not design against a face you have not
loaded. The verifier checks this.

## Micro-typography

The details that separate typeset from typed: real quotation marks and
apostrophes (’ “ ” not ' "), an en dash for ranges and an em dash for asides,
non-breaking spaces before units and after short words that should not end a
line, `font-variant-numeric: tabular-nums` wherever digits line up in a column,
and `text-wrap: balance` on headings.

Dates, times, numbers and currency follow the **reader's** locale, not the
developer's. `7/6/2026` is ambiguous outside the United States and wrong
everywhere the site is not in English. Use `Intl.DateTimeFormat` with the page's
own language. Interface words — "min read", "home", "comments" — must be in the
site's language too. The verifier checks both.

## Images

Decide what they are for. If they are the argument, give them room and let type
recede. If they are decoration, question whether they earn their bytes. Either
way: correct aspect ratios held with `object-fit`, explicit dimensions to stop
layout shift, and never a stock placeholder in front of a client — an unfilled
space is more honest than a picture of nobody.

## Motion

Serve the subject. One orchestrated moment beats scattered effects, and scattered
effects are themselves a tell. Respect `prefers-reduced-motion` — not as a
courtesy, as a correctness requirement.

## Before you call it done

Read the page as a stranger on a phone. Then check the things you cannot see by
looking: contrast ratios, focus states on every interactive element, what
happens at 320px, and what the page is like with the webfont still loading.

## Sources

These are the canonical texts. Where this file and your instinct disagree,
they are why.

- **Robert Bringhurst, *The Elements of Typographic Style*** — the reference
  work on setting type; measure, scale and rhythm as described here come from it.
- **Ellen Lupton, *Thinking with Type*** — letter, text, grid; the most direct
  route from theory to a page.
- **Josef Müller-Brockmann, *Grid Systems in Graphic Design*** — why the
  invisible structure is what makes work feel intentional.
- **Matthew Butterick, *Practical Typography*** (practicaltypography.com) — free,
  online, and unusually actionable on exactly the details above.
- **Richard Rutter, *Web Typography* / betterwebtype.com** — the same craft
  expressed in CSS, for the web's constraints.
- **Erik Spiekermann, *Stop Stealing Sheep & Find Out How Type Works*** — the
  readable introduction if the others feel forbidding.
- **WCAG 2.2** (w3.org/TR/WCAG22) — the contrast and focus requirements, which
  are obligations rather than guidance.
