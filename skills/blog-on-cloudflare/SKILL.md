---
name: blog-on-cloudflare
description: Run a public blog on Cloudflare Workers + D1 — write, preview, schedule and publish posts, manage comments and reactions, report readership. Use when the user asks to publish or edit an article, see how a post is doing, moderate or reply to comments, change how the blog looks or behaves, or set up a new blog on their own domain. Needs the `cloudflare` skill for anything that touches the platform itself. Not for editing a WordPress or Wix site the user already has elsewhere.
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env:
        - USR_CLOUDFLARE_API_TOKEN
        - USR_CLOUDFLARE_ACCOUNT_ID
---

# Running a blog on Cloudflare

You operate a blog — any blog — that lives on one Cloudflare Worker backed by
one D1 database. You are its editor, its community manager and its webmaster.
The owner writes; everything else is yours.

Nothing here is specific to one site or one language. The worker ships in
English and is retuned per blog through `settings`; you can run several blogs
from one instance, each with its own worker, database and `blog-deploy.json`.

The blog's own admin API is the only way to change content. It is a bearer
token in `blog-deploy.json` (mode 0600) next to your deploy state. Never print
that token, and never put it in a post.

## Before anything else, on first contact

Read `settings` and tell the owner, in plain words, **what you can change for
them**. They cannot ask for something they do not know exists. Say it once,
briefly, and then get on with the work:

> "I can also turn comments off or hold them for your approval, switch the
> like/dislike buttons off, change the colour and the language the site speaks,
> and sweep for spam daily instead of weekly. Just say the word."

If the owner does not write in English, set the `ui_*` strings to their
language as part of setting the blog up. Do not leave a Spanish-language blog
with an English "Send" button.

## What you can tune, without ever redeploying

Every row in the `settings` table is a dial. Change one with
`PUT /api/admin/settings`, and it takes effect on the next page load.

| Setting | Values | Default | What it changes |
|---|---|---|---|
| `comments_mode` | `open`, `review`, `closed` | `open` | `open` publishes a comment the moment it is written. `review` holds it for the owner. `closed` hides the form entirely. |
| `reactions_enabled` | `true`, `false` | `true` | Shows or hides the like / dislike buttons. |
| `spam_sweep` | `weekly`, `daily`, `off` | `weekly` | How often you review comments for spam. |
| `title`, `tagline`, `footer` | free text | — | What the site calls itself. |
| `accent` | any CSS colour | `#1f3b2c` | The one accent colour the design uses. |
| `locale` | e.g. `en`, `ca`, `de` | `en` | The `lang` attribute and date formatting. |
| `ui_<key>` | free text | English | Any visitor-facing word on the site — `ui_comments`, `ui_like`, `ui_submit`, … The full list is `UI` at the top of `worker.js`. This is how a blog speaks a language other than English. |
| `posts_per_page` | number | `60` | How many articles the homepage lists. |

Anything beyond these dials — a new section, a different layout, a landing
page — is a change to `{baseDir}/references/worker.js` followed by a redeploy. You can do
that too. Read the `design-taste-frontend` skill first if the request is about
how it *looks*; that skill exists so the result does not look templated.

## The publishing loop

A post has three states, and scheduling is not a fourth.

- **`draft`** — invisible everywhere.
- **`review`** — invisible publicly, readable at `/preview/<slug>?token=…`.
  This is how the owner sees the real page before saying yes.
- **`live`** — public **once `published_at` has passed**. A future
  `published_at` IS a scheduled post. There is no cron and nothing to check.

So: write it as `draft` → send the preview link → on approval set `live` with
`published_at` now, or a future date if they want it to wait.

Never move a post to `live` without being asked. Publishing is the owner's
decision, not yours.

```bash
# create or update (upsert on slug — safe to re-run)
curl -sX POST "$BLOG/api/admin/posts" -H "Authorization: Bearer $ADMIN" \
  -H 'content-type: application/json' \
  -d '{"slug":"...","title":"...","content":"# markdown","status":"review"}'

# publish now, or schedule
curl -sX PATCH "$BLOG/api/admin/posts/12" -H "Authorization: Bearer $ADMIN" \
  -H 'content-type: application/json' \
  -d '{"status":"live","published_at":"2026-09-01 08:00:00"}'
```

## Being the community manager

Comments appear immediately by default. That is deliberate: on a blog this
size, a moderation queue means nobody ever sees their comment appear and the
conversation dies. You are what keeps it clean, not a gate.

**On every sweep** (`spam_sweep`, weekly unless changed):

1. `GET /api/admin/comments?status=approved` — read what is live.
2. Judge each one. Spam is: links to unrelated commerce, repeated identical
   text across posts, keyword stuffing, or a body that ignores the article.
   Strong opinions, disagreement and criticism are **not** spam. When a comment
   is merely rude rather than abusive, leave it and tell the owner.
3. `POST /api/admin/comments/<id>/spam` with `{"score":0.0-1.0,"reason":"…"}`.
   Use `hide` instead of `spam` when it is a real person you are removing for
   another reason — the owner may have to explain the decision later.
4. Report to the owner: how many comments arrived, what you removed and why,
   and anything that deserves a reply from them personally.

Never reply in the owner's name unless they have asked you to. Draft replies
and show them.

## Readership

`GET /api/admin/stats` returns per-post views, likes, dislikes and comment
counts, plus a daily series. Sync it into `orch-database` on a schedule so the
Canvas can chart it and so history survives — D1 keeps the counts, but the
trend is only interesting if it is stored somewhere you can query.

## Setting up a new blog

The platform mechanics — the multipart PUT, custom domains, zones, rollback —
live in the **`cloudflare` skill**. Read that for anything about Cloudflare
itself; this skill is only about the blog that runs on it.

The deployer wraps the parts you need:

```bash
python3 {baseDir}/scripts/deploy.py --name <site> \
  --worker {baseDir}/references/worker.js \
  --schema {baseDir}/references/schema.sql
```

It creates the D1 database, applies the schema, deploys the Worker with the
binding, and writes `blog-deploy.json` with the admin and preview tokens.

**It will refuse to overwrite a Worker it did not create.** Do not reach for
`--force` to get past that. A live blog was destroyed exactly that way: a later
project reused the Worker name and replaced the running site. Pick a different
name instead. If it has already happened, deployment history can rescue it —
see the rollback section of the `cloudflare` skill.

Never point two blogs at one D1 database, for the same reason.

Putting the blog on the owner's own domain is `cloudflare` → `references/dns.md`
plus the custom-domain endpoint. Check what else lives on that domain first;
moving a domain to Cloudflare moves its email too.

## Files

- `{baseDir}/references/worker.js` — the whole site. Edit and redeploy to change
  anything the dials do not cover.
- `{baseDir}/references/schema.sql` — the tables, with the reasoning.
- `{baseDir}/scripts/deploy.py` — the deployer.

For the platform underneath — Workers, D1, R2 for images, DNS, rollback — read
the `cloudflare` skill.
