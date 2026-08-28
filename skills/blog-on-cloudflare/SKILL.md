---
name: blog-on-cloudflare
description: Everything worth knowing before building someone a blog or publication on Cloudflare — the content model, publishing states, comments and moderation, reactions, images, feeds, and the traps that only show up in production. Use when the user wants a blog, magazine, newsletter archive or any site where they publish over time. Needs the `cloudflare` skill for the platform itself and `design-taste-frontend` for how it looks. Contains no template: you design and write the site.
metadata:
  openclaw:
    emoji: "📝"
---

# Building someone a blog

**There is no starter worker in this skill, on purpose.** An earlier version
shipped one and every blog built from it came out looking identical — same
type, same column, same page, whoever it was for. A working file beats good
advice every time, so the file is gone.

What is here is the part that is genuinely hard: the decisions that are easy to
get wrong and expensive to discover later. The site itself is yours to design.

Read `design-taste-frontend` **before** you write markup, and `cloudflare` for
the platform. Then build whatever the brief actually calls for. A furniture
maker's site and a political columnist's site should not resemble each other.

## Decide these before you write anything

**What is a post, for this person?** Not "title, body, date" by default. A
woodworker's piece has wood, dimensions, whether it was commissioned. A
restaurant's has a season. A researcher's has citations. Ask, or infer from the
brief, and model *that*. You own the schema.

**How is the front page organised?** Reverse-chronological is a default, not an
answer. Work is often better as a gallery. A columnist may want sections.
Someone with forty pieces needs a way in that is not scrolling.

**What does the reader do here?** Read and leave? Subscribe? Comment? Browse
by material, place, year? That decides the routes, and therefore the shape.

## Publishing states

Three states carry almost every publication:

- **draft** — invisible everywhere, including by direct URL
- **review** — invisible publicly, visible on a secret preview URL so the owner
  sees the real page before saying yes
- **live** — public

**Scheduling is not a fourth state and needs no cron.** A scheduled post is a
live row with a future publish timestamp, and every public query filters on
`timestamp <= now`. One mechanism, nothing to run at 3am, nothing to break.

Never move something to public without being asked. Publishing is the owner's
decision.

## Comments

Default to publishing them immediately. On a small site a moderation queue
means nobody ever sees their comment appear and the conversation dies. Sweep
for spam on a schedule instead, and offer to switch to hold-for-approval — but
let the owner choose it rather than imposing it.

Strong opinions and disagreement are not spam. Removing a real person is a
different act from deleting spam; keep them distinguishable, because the owner
may have to explain the decision.

Never reply in the owner's name unless asked. Draft, and show them.

## Reactions

If you offer like/dislike, **one per visitor must be a database constraint**, a
`UNIQUE(post, visitor)`. A cookie identifies a returning visitor; it enforces
nothing, because it lives on their machine.

## Images

Someone publishing weekly will have a picture every week. Put them in R2 and
serve them through the worker: one hostname, no CORS, and it keeps working if
the bucket is later made private.

Name keys by content (`2026/08/slug-a1b2c3.jpg`). That is what makes
`immutable` caching safe — a changed image becomes a new key rather than a new
version of an old one, so no reader ever sees a stale picture.

## Being found

A feed, a sitemap, and `robots.txt` cost almost nothing and are the difference
between a site that can be followed and one that can only be visited.

If you offer a feed, do not label it "RSS" and leave a link to raw XML. Most
people have never heard of it. Explain it in a sentence — it works like
subscribing to a podcast — and give them the address to copy.

And give the site a **favicon**. A tab with a blank page icon reads as
unfinished, and it is the one piece of the design people see every day.

## Traps that only appear in production

- **Escape everything a visitor typed, at render.** One escape function, used
  everywhere. If you write a second one you will eventually use the wrong one.
- **Escaping before parsing markdown breaks it.** `>` becomes `&gt;` and every
  blockquote renders as a literal. Detect structure on the raw line, escape
  when emitting.
- **A `margin` shorthand overwrites `margin: auto`.** `margin: 4rem 0` on a
  centred block silently pins it to the left edge. This has already shipped
  once.
- **Admin writes go behind a bearer token**, compared in full. The worker's
  source is readable back through the API, so never inline a secret.
- **Rate-limit the public write endpoints.** Comments and reactions are the two
  things a stranger can call as often as they like.

## Before you say it is done

Run the `cloudflare` skill's `scripts/verify-site.py` against the URL you just
deployed. Do not guess at its path from here — the two skills can be installed
into different roots, so a relative path between them resolves on one instance
and not on another. Find it in that skill's own directory.

**Look at the screenshots it takes.** You cannot see the page otherwise, and
every visual defect this skill has caused so far was invisible from the source:
type running off the edge, a missing favicon, a nav pointing at routes that do
not exist.

**Check an article page too, not only the homepage.** The homepage is the one
page you have looked at a hundred times while building; the article template is
where a reader actually spends their time, and it is where the routing bugs
live — one blog shipped with a homepage linking to `/piece/<slug>` while the
worker only served `/peça/<slug>`, so every post 404'd and the homepage looked
perfect throughout.

**A failing check is not advice.** Fix what fails. If you genuinely cannot, say
which check is still failing and why, in the same breath as telling the owner
where things stand — never a green light with a red check behind it.

A blog with no posts in it is not finished either. If you are migrating, seed
the content. If you are starting fresh, ask what should go up first.
