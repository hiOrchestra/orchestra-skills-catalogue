---
name: site-operations
description: Run a live site or web app the way an operator would — every change backed up first, deployed to a preview before it is public, verified from the outside after every deploy, and reported in the three states that matter (uploaded, active, public) so "fixed" is never said early. Use whenever you change, deploy, migrate, restore or troubleshoot something people are already using — a blog, a landing page, a tool — and whenever you report on it. Not for building something new from a brief (that is brief-before-build), and not for the platform calls themselves (that is cloudflare).
metadata:
  openclaw:
    emoji: "🛠️"
---

# Site operations

Building a site is one afternoon. Running it is every day after. This skill
is the every-day-after: the habits that keep a live site from breaking under
a change, and the honesty that keeps the owner trusting what you tell them.

Every rule below was paid for. A publisher watched their site go down during a
change and described the agent's behaviour as *erratic* — not because the fix
was hard, but because the agent kept saying "fixed" about a version that was
uploaded and not yet live, then about one that was live and not yet public.
Three different things were being called by one word.

## The three states

A change is in one of three states, and you say which:

1. **Uploaded** — the new version exists on the platform. Nobody sees it.
2. **Active** — the platform serves it. A request would hit it.
3. **Public and verified** — you fetched the real pages from the outside, as a
   reader would, and they are right.

"Fixed", "deployed", "done" mean the third state only. Until then, say the
state you are actually in: "uploaded, activating now", "active, verifying".
A person who hears "fixed" and refreshes to a broken page stops believing the
next twenty things you say.

When the person reports something you cannot reproduce — "the site was down
on my phone yesterday" — say what you checked and what you found, and do not
claim a cause you have not shown. An unproven incident stays open.

## Before every change

**Back up what the change can touch.** A database export before a schema
change or a bulk edit; the current worker version noted before a deploy (the
platform keeps deployment history — know the previous version's id before you
replace it). "Before" means before, not after the mistake. Put the backup in
Files with a name that says what and when (`<site>-d1-backup-<date>.sql`).

**Know what is live on that name.** Never deploy over a script, database or
domain you did not create in this project. A working site was destroyed
because a later project reused its worker name.

**Preview before public** when readers are using it. A change to a live site
goes to a preview URL or a review state first, gets looked at there, and only
then becomes the active version. The owner sees the real page before saying
yes.

## After every deploy

**Verify from the outside.** Fetch the real, public URLs — not the source you
just wrote. At minimum: the home page, one item page (an article, a record —
the page a reader actually spends time on), the archive or list, the sitemap,
the feed if there is one, and a route that should be refused (the admin
without a token). Each returns what it should, with the status code it should.

Where the `cloudflare` skill is installed, its `scripts/verify-site.py` does
this and takes screenshots. Run it, then **look at the screenshots** — the
checks are a floor. A page can pass every one and still be wrong, and that is
what you are there to catch.

**A failing check is not advice.** Fix what fails. If you cannot, say which
check fails and why, in the same sentence as the status — never a green light
with a red check behind it.

**Verify the thing you changed, not the thing you always look at.** A renderer
that lost bold and italic shipped because the home page — which has no bold —
looked perfect. Open the page that exercises the change.

## Defensive by default

Public pages fail in public. The habits that stop a small data problem from
becoming a site-wide outage:

- **Never let one bad row take down a page.** A malformed field in one item
  (`images` that was not valid JSON) threw inside the home-page render and
  returned 500 for every visitor — and looked, from outside, like a scheduling
  bug. Parse defensively (`safeJson`), render the item as degraded, log it,
  and keep the page up.
- **One escape function, used at render, everywhere.** Escaping before
  parsing markdown turns every `>` into a literal and every blockquote into
  text.
- **Scheduled visibility is a filter on every public query**, not a switch
  somewhere else. If an item is meant to be invisible until 08:00, it is
  invisible on the front page, in the archive, in its section, in the feed and
  in the sitemap — the same predicate in all five places, or one of them
  leaks.
- **Secrets are bindings, never source.** The source is readable back through
  the platform's API.
- **Rate-limit public writes** (comments, reactions, contact forms) — they are
  the calls a stranger can make as often as they like.

## Reporting

Every report says three things, separately: **validated** (what you checked
and found right), **done** (what changed, in which state), **pending** (what
is not done and why — missing material, a failing check, a decision that is
theirs). Never fold pending into done to make the message shorter.

Scheduled reports (a daily "comments and messages", a weekly "what is due")
are routines; keep them to the facts the person asked for, and say "nothing"
when there is nothing rather than skipping the day — a missing report reads
as a broken routine.

## When something is wrong

1. Say what the person is seeing, in the state vocabulary, and what you are
   doing about it — before you start.
2. Roll back if a rollback exists and the previous version was good. The
   platform keeps history; the previous version is very likely one call away.
   A rollback is not a failure, it is the fastest fix.
3. Find the cause on the preview, not on the live site.
4. Fix, deploy, verify from the outside, then say "fixed" — once.
5. Write the cause and the fix into your memory in one line, so the next
   incident starts further along.

## Before you say it is done

You can name the state (public and verified), you fetched the pages a reader
would and they were right, the check that was failing is now passing or you
have said which one is not, the backup you took before the change is in Files,
and the report separates validated, done and pending. If any of these is
missing, you are in an earlier state — say that one.
