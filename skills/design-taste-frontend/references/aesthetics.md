# Named directions

Vocabulary, not a menu. Picking a row off this page and implementing it is the
same mistake as having no direction at all — every model's "cyberpunk" is the
same cyberpunk. What this page is for is naming what you are doing, so you can
tell whether you chose it or fell into it.

**How to use it.** Read the subject first: what the thing IS, who reads it, what
its own world looks like — its materials, instruments, vernacular. Let that
suggest a direction. Then find it here, take the structural habits, and derive
the actual colours and faces from the subject rather than from this page. Write
down which direction you took and which one you refused, before any CSS.

## The defaults, so you can recognise them

Three directions arrive on their own, regardless of brief. They are legitimate
answers when the subject genuinely calls for them, and a tell when it does not.

| The look | How it shows up | Documented as |
|---|---|---|
| **Warm Editorial** | cream ground near #F4F1EA, high-contrast display serif, terracotta or coral accent, mono uppercase eyebrow labels | a named family in awesome-claude-design ("Warm Editorial", after Claude and Notion) and in SDesign ("Warm Humanist") |
| **Terminal / Tech Dark** | near-black ground, one acid green or vermilion accent, monospace everywhere | SDesign "Tech Dark", awesome-claude-design "Terminal-Core" |
| **Broadsheet** | hairline rules, zero radius, dense justified columns, small caps | the newspaper pastiche every model reaches for when told "editorial" |

If your palette is cream and terracotta, or near-black and acid green, you have
not yet made a decision. That is the thing the palette check in the `cloudflare`
skill's verifier looks for.

## Directions

Each entry: the world it belongs to · what carries it · where it fails.

**Swiss / International**
Objective, gridded, unornamented. Ground stays neutral and the grid does the
talking; one accent, used as signal rather than decoration. Type is a single
grotesque at several weights, set tight, ranged left, never centred. Structure
is the design — columns you can count, a baseline everything sits on.
*Fails when* the content is emotional or narrative; rigour reads as coldness.

**Editorial / Magazine**
For things that are read at length. An asymmetric grid, a real measure
(45–75 characters), a display face used at genuinely large sizes against small
body text, and pull-quotes that break the column deliberately. Whitespace is
structural, not padding.
*Fails when* applied to a tool — a dashboard set like an essay is unusable.

**Archival / Institutional**
Libraries, journals, public records. Muted paper grounds, one ink, tables and
indexes treated as first-class objects rather than afterthoughts, numbering that
means something. Restraint reads as trustworthiness.
*Fails when* the subject wants warmth or personality.

**Brutalist / Neo-brutalist**
Raw structure on display: thick borders, hard offset shadows, flat saturated
blocks, right angles, system or monospace type. Nothing is softened; the
construction is the ornament.
*Fails when* the audience needs reassurance — it reads as unfinished to anyone
not already in on it.

**Technical / Instrument**
Software that measures things. Dense but not cramped, tabular numerals, state
carried in form as well as colour, charts as the hero rather than an
illustration. Colour is semantic first (good/warn/critical) and decorative last.
*Fails when* there is no data — the density has nothing to hold.

**Industrial**
Workshops, logistics, machinery. Materials and wear: concrete, steel, tape,
stencil type, high-contrast safety colours used functionally. Grids are heavy
and visible.
*Fails when* the subject is delicate or personal.

**Civic / Wayfinding**
Public services, transit, timetables. Signage typography, strong colour coding
that survives being glanced at, legibility over subtlety, big touch targets,
information ordered by what someone needs first at seven in the morning.
*Fails when* used for something that wants to be admired rather than used.

**Documentary / Photographic**
When the images are the argument. Type recedes to captions and credits; the
grid exists to give pictures room; ground is chosen to sit under the photographs
rather than compete. Full-bleed used sparingly, for the one image that earns it.
*Fails when* the imagery is stock — the whole direction collapses.

**Craft / Material**
Makers, food, small manufacture. Texture and irregularity, colours drawn from
the actual material, hand-set details, generous product photography.
*Fails when* it slides into Warm Editorial, which it neighbours closely — the
distinguishing move is that the palette comes from the material, not from paper.

**Cinematic**
Trailers, launches, single-message pages. Oversized type, deep grounds,
gradients with real depth, motion that is choreographed rather than scattered.
One moment carries the page.
*Fails when* there is more than one thing to say.

**Playful / Illustrated**
Consumer products, children, education. High saturation used confidently, custom
illustration, rounded forms, motion with personality.
*Fails when* the illustration is generic — then it is just noise in colour.

**Soft-futurism / Glass**
Layered translucency, blur, light. Depends entirely on execution quality and on
having something behind the glass worth blurring.
*Fails when* applied flat — glassmorphism over a solid background is decoration
with no idea behind it. Provide a solid fallback for `prefers-reduced-transparency`.

**Period work** (Art Deco, Bauhaus, Memphis, Y2K, Victorian…)
Only when the subject has an actual claim on the period. Borrow the structural
logic — Deco's symmetry and metallic rules, Bauhaus's primary geometry, Memphis's
clashing pattern — not a pastiche of its clichés.
*Fails when* it is costume: a period look on an unrelated subject reads as a
theme, not a design.

## Where these came from

The families and their descriptors are drawn from published catalogues rather
than invented here, so the names mean the same thing outside this skill:

- **DESIGN.md** — the format specification for describing a visual identity to
  coding agents, open-sourced by Google Labs (Apache-2.0),
  `github.com/google-labs-code/design.md`
- **awesome-claude-design** — 68 brands grouped into nine aesthetic families,
  `github.com/rohitg00/awesome-claude-design`
- **SDesign** — 64 systems across six families, with tokens per system,
  `github.com/simonlin1212/SDesign`
- **DESIGN.md Library** — 562 documented systems spanning Bauhaus and Art Deco
  through Y2K and Vaporwave, `designmd.app/library`

Those catalogues also ship copy-paste reference pages. Deliberately not mirrored
here: a template is the fastest route to a site that looks like every other site
built from the same template, which is the failure this skill exists to prevent.
Take the tokens and the reasoning; write the page yourself.

For the craft underneath any of these directions, see `{baseDir}/references/craft.md`.
