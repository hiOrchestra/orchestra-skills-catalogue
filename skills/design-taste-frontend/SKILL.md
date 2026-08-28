---
name: design-taste-frontend
description: Design and build frontends that do not look AI-generated — landing pages, marketing sites, portfolios, blogs and redesigns. Reads the brief, commits to a design direction, picks a real design system when one fits, and checks its own work against a list of the tells that give machine-made pages away. Use whenever you are writing HTML/CSS, restyling something, or the user says a page looks generic, templated or "like AI made it". Not for dashboards, data tables or multi-step product UI.
metadata:
  openclaw:
    emoji: "\U0001F3A8"
---

# Designing something that does not look generated

Most machine-made design is bad for one reason: the model skips reading the
brief and reaches for a default aesthetic. This skill exists to stop that.

Two things always happen, in this order:

1. **Read the room, then say what you read.** Output a one-line Design Read
   before writing any code. It commits you to a direction and makes a wrong
   direction correctable in one sentence instead of one rewrite.
2. **Check your work before you hand it over.** Run the pre-flight in
   `{baseDir}/references/preflight.md`. Most of what makes a page look
   generated is on that list, and you put it there yourself ten minutes ago.

Everything else is contextual. Nothing below fires automatically — pull only
what the brief calls for.

## What to open, and when

| The task | Read |
|---|---|
| **Choosing a direction — what this page should BE** | `{baseDir}/references/aesthetics.md` |
| **The craft under any direction — measure, scale, rhythm, grid, colour, locale** | `{baseDir}/references/craft.md` |
| Choosing between Tailwind, shadcn, Material, GOV.UK, Carbon…; install commands | `{baseDir}/references/design-systems.md` |
| Actually writing the page — type, colour, space, motion, layout decisions | `{baseDir}/references/directives.md` |
| "It looks AI-generated" — the specific tells, and what to do instead | `{baseDir}/references/ai-tells.md` |
| File/CSS structure, tokens, dark mode, performance and accessibility floors | `{baseDir}/references/architecture.md` |
| What to volunteer without being asked (empty states, errors, loading, meta) | `{baseDir}/references/proactivity.md` |
| Redesigning something that already exists | `{baseDir}/references/redesign.md` |
| Naming a pattern you can see but cannot name | `{baseDir}/references/vocabulary.md` |
| Standard page sections and what each one owes the reader | `{baseDir}/references/block-library.md` |
| Frosted-glass / translucent-material effects, done honestly | `{baseDir}/references/liquid-glass.md` |
| Before you say it is finished | `{baseDir}/references/preflight.md` |

Open `aesthetics.md` before you write anything and `craft.md` while you write.
Between them they answer the two different questions — what this should be, and
whether it is any good. `directives.md` and `ai-tells.md` go deeper on fixing a
page that came out bland.

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

Before touching code or tweaking dials, **infer what the user actually wants**. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

### 0.A Read these signals first
1. **Page kind** - landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** the user used - "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** - URLs they linked, screenshots they pasted, products they named, brands they're competing with.
4. **Audience** - B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** - logo, color, type, photography. For redesigns, these are starting material, not optional input (see Section 11).
6. **Quiet constraints** - accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These constraints OVERRIDE aesthetic preference.

### 0.B Output a one-line "Design Read" before generating
Before any code, state in one line: **"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

Example reads:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend or USWDS."*

### 0.C If the brief is ambiguous, ask one question, do not guess
Ask exactly **one** clarifying question - never a multi-question dump - and only when the design read genuinely diverges. Example: *"Should this feel closer to Linear-clean or Awwwards-experimental?"*

If you can confidently infer from context, **do not ask**. Just declare the design read and proceed.

### 0.D Anti-Default Discipline
Two generations of default, and the older list is the more dangerous one to
trust, because following it lands you squarely on the newer.

**Still true:** no AI-purple gradients, no centred hero over a dark mesh, no
three equal feature cards, no glassmorphism as a default surface, no
infinite-loop micro-animation, no Inter + slate-900.

**And now, the look those corrections produce:** warm cream ground near
#F4F1EA, high-contrast display serif, a single desaturated terracotta or coral
accent, mono uppercase eyebrow labels above every section. This is a NAMED
family — "Warm Editorial" in awesome-claude-design, "Warm Humanist" in SDesign
— and it is where models in this family land by default. It arrived unprompted
for a carpentry studio and a municipal swimming pool on the same day, in the
same hexes. The sibling default is near-black with one acid-green or vermilion
accent.

Both are legitimate when the subject genuinely calls for them, and a tell when
it does not. If your palette is cream + terracotta and you did not derive it
from the subject, you have not made a decision — and the `cloudflare` skill's
verifier now says so out loud.

Reach past all of it deliberately, from the design read. `{baseDir}/references/aesthetics.md`
is the vocabulary for doing that.

---

---

## 1. THE THREE DIALS (Core Configuration)

After the design read, set three dials. Every layout, motion, and density decision below is gated by these.

* **`DESIGN_VARIANCE: 8`** - 1 = Perfect Symmetry, 10 = Artsy Chaos
* **`MOTION_INTENSITY: 6`** - 1 = Static, 10 = Cinematic / Physics
* **`VISUAL_DENSITY: 4`** - 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4`. Use these unless the design read overrides them. Do not ask the user to edit this file - overrides happen conversationally.

### 1.A Dial Inference (design read → dial values)
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

### 1.C How the Dials Drive Output
Use these (or user-overridden values) as global variables. Cross-references throughout this document refer to these exact variable names - never invent aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

---

---

## 13. OUT OF SCOPE

This skill is NOT for:
* Dashboards / dense product UI / admin panels (use Fluent, Carbon, Atlassian, or Polaris from Section 2.A).
* Data tables (use TanStack Table or AG Grid).
* Multi-step forms / wizards (use Form-specific patterns; this skill won't make them better).
* Code editors (use Monaco / CodeMirror with their official skinning).
* Native mobile (use Apple HIG / Material directly).
* Realtime collab UIs (presence, cursors, OT-aware - different problem class).

If the brief is one of the above, **say so explicitly**, point to the right tool, and only apply this skill's marketing-page / about-page / landing-page parts to the surfaces where they apply.

---

---

## Where this came from

The rules here are the accumulated corrections of a lot of generated pages that
came out looking the same. They are opinions with reasons attached, not style
preferences — each one exists because its absence produced something worse.
Where a reference and the user's brief disagree, the brief wins.
