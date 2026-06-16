---
name: wordpress
version: 0.1.0
description: >-
  Create and manage content on a WordPress site via the WordPress REST API (v2):
  draft/publish/update posts and pages, upload images to the media library and
  set featured images, manage categories & tags, and moderate comments.
  Authenticates with an Application Password using Basic auth — site URL in
  USR_WORDPRESS_URL, username in USR_WORDPRESS_USER, app password in
  USR_WORDPRESS_PWD.
triggers:
  - wordpress
  - wp
  - blog post
  - publish post
  - draft post
  - cms
  - article
  - featured image
  - wp media
  - categories
  - tags
  - moderate comments
metadata:
  openclaw:
    emoji: "📝"
requires:
  bins: []
  env:
    - USR_WORDPRESS_URL
    - USR_WORDPRESS_USER
    - USR_WORDPRESS_PWD
  config: []
---

# WordPress — create & manage content

Manage a WordPress site by calling its REST API (v2) directly with `exec curl`.
You can create/update posts and pages, upload media, manage categories & tags,
and moderate comments.

## Auth — Application Password via Basic auth

Three values are stored in config and available as env vars in `exec`:

- `USR_WORDPRESS_URL` — the site root, e.g. `https://myblog.com` (no trailing slash)
- `USR_WORDPRESS_USER` — the WordPress username
- `USR_WORDPRESS_PWD` — an **Application Password** (WordPress 5.6+, generated under
  Users → Profile → Application Passwords). It looks like `abcd EFGH ijkl 1234`;
  the spaces are fine.

Authenticate with curl's `-u` flag on **every** request — this sends an
`Authorization: Basic` header and keeps the password out of the URL. **Never
print or echo `USR_WORDPRESS_PWD`** in your reply or in command output.

API base: `$USR_WORDPRESS_URL/wp-json/wp/v2`

### Verify auth first (once)

```bash
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/users/me?context=edit"
```

Returns the current user JSON on success. `401`/`403` with code
`rest_not_logged_in` / `incorrect_password` means the credentials are wrong or
Application Passwords are disabled — tell the user to check
`USR_WORDPRESS_URL`, `USR_WORDPRESS_USER`, and `USR_WORDPRESS_PWD` in config.

## Posts

Posts take a JSON body. `status` is `draft` (default — safest), `publish`,
`pending`, `private`, or `future` (with a `date`). Content is HTML; the Gutenberg
block markup is optional — plain HTML paragraphs render fine.

```bash
# Create a draft post
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Type: application/json" \
  -d '{"title":"My title","content":"<p>Body in HTML.</p>","status":"draft","excerpt":"Short summary"}' \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/posts"

# Publish immediately: set "status":"publish" instead.

# Update an existing post (id from the create response)
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Type: application/json" \
  -d '{"content":"<p>Edited body.</p>","status":"publish"}' \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/posts/123"

# List recent posts (any status needs context=edit + auth)
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/posts?per_page=10&status=any&context=edit&orderby=date&order=desc"

# Search posts by keyword
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/posts?search=keyword&context=edit"

# Delete a post (move to trash; add &force=true to permanently delete)
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" -X DELETE \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/posts/123"
```

Useful post fields: `title`, `content`, `excerpt`, `status`, `slug`, `date`
(ISO 8601, for scheduling with `status:"future"`), `categories` (array of ids),
`tags` (array of ids), `featured_media` (media id), `author` (user id).

The response includes the new/updated post `id` and `link` — report the link to
the user.

## Pages

Pages use the same shape as posts at `/wp/v2/pages`. Extra fields: `parent`
(parent page id) and `menu_order`.

```bash
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Type: application/json" \
  -d '{"title":"About","content":"<p>About us.</p>","status":"publish"}' \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/pages"
```

## Media (images)

Upload binary file data with `--data-binary` and a `Content-Disposition` header
giving the filename. The response `id` is the attachment id; the response
`source_url` is the public image URL.

```bash
# Upload an image to the media library
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Disposition: attachment; filename=hero.jpg" \
  -H "Content-Type: image/jpeg" \
  --data-binary @/path/to/hero.jpg \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/media"
```

Use the returned media `id` as a post's `featured_media` to set the featured
image, e.g. update the post with `-d '{"featured_media": 456}'`. To add a
caption/alt text, PATCH the media item: `-d '{"alt_text":"...","caption":"..."}'`
against `/wp/v2/media/456`. Match `Content-Type` to the file (`image/png`,
`image/webp`, etc.).

## Categories & tags

Posts reference categories and tags by **numeric id**, not by name. Resolve a
name to an id first; create it if it doesn't exist.

```bash
# Find a category by name (search), or list all
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/categories?search=News"

# Create a category (returns its id)
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Type: application/json" \
  -d '{"name":"News"}' \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/categories"
```

Tags work identically at `/wp/v2/tags`. Then attach to a post with
`-d '{"categories":[3],"tags":[7,9]}'`.

## Comments (moderation)

```bash
# List comments awaiting moderation
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/comments?status=hold&context=edit"

# Approve / hold / spam / trash a comment by setting status
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Type: application/json" \
  -d '{"status":"approved"}' \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/comments/55"

# Reply to a comment: POST with post + parent ids
exec curl -s -u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD" \
  -H "Content-Type: application/json" \
  -d '{"post":123,"parent":55,"content":"Thanks for your comment!"}' \
  "$USR_WORDPRESS_URL/wp-json/wp/v2/comments"
```

Comment `status` values: `approved`, `hold`, `spam`, `trash`.

## Rules

- **Always authenticate with `-u "$USR_WORDPRESS_USER:$USR_WORDPRESS_PWD"`.**
  Never print or echo the password, and never put it in the URL.
- **Default new posts/pages to `status:"draft"`** unless the user clearly asks to
  publish. Confirm before publishing or deleting content.
- Categories/tags are referenced by id — resolve names to ids (search, then
  create if missing) before attaching them to a post.
- Send a `Content-Type: application/json` header on every POST/PATCH with a JSON
  body, or WordPress ignores the body.
- Parse the JSON response and report the resulting post/page `link` (or media
  `source_url`) to the user. On error, read the `code` and `message` fields and
  report them succinctly — don't invent success.
- Treat the site root from `USR_WORDPRESS_URL` as having **no trailing slash** and
  build paths as `$USR_WORDPRESS_URL/wp-json/wp/v2/...`.
- If you get `404 rest_no_route`, the REST API path is wrong or pretty permalinks
  are off — try `"$USR_WORDPRESS_URL/?rest_route=/wp/v2/posts"` form as a fallback.
