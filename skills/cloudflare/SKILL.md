---
name: cloudflare
description: Build, deploy and operate real software on Cloudflare — Workers, D1 databases, R2 object storage, KV, DNS and domains, Pages, Turnstile and Queues, all through the REST API. Use whenever the user wants a website, web app, API or scheduled service built, deployed, put on their own domain, or changed afterwards; also for storing files, running a database, or moving a domain onto Cloudflare. Not for editing a site hosted elsewhere.
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      env:
        - USR_CLOUDFLARE_API_TOKEN
        - USR_CLOUDFLARE_ACCOUNT_ID
---

# Cloudflare

You can put working software on the internet, on the user's own domain, without
anyone else's help. That is what this skill is for. Workers run the code, D1
stores the data, R2 stores the files, DNS points the domain at it.

Everything is the REST API at `https://api.cloudflare.com/client/v4`, authorised
with `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`. There is no CLI to
install and `wrangler` is not required — do not ask the user to install it.

## A deploy is not done until you have looked

You cannot see what you shipped, and reading your own HTML back is not looking.
Every site built with this skill that went out broken had passed its author's
reading first: a headline sitting outside the column while everything else held
it, no favicon, a homepage linking to routes the worker does not serve.

After every deploy, before you tell anyone it is ready:

```bash
python3 {baseDir}/scripts/verify-site.py <url> [--admin-path /api/admin/...]
```

It renders the page in the browser already running on this instance, saves a
desktop and a phone screenshot, and checks the floor — the page loads, the admin
refuses an unauthenticated caller, no key is being served, the text lines up on
one column, there is a favicon, internal links resolve.

Then **open the screenshots**. The checks are a floor, not a verdict: a site can
pass every one of them and still look wrong, and that is the failure you are
there to catch.

Do not report a site as finished before this has run and you have looked at what
it produced.

**A failing check is not advice.** The first agent to use this ran the checks,
read a FAIL about a headline sitting outside the column, fixed the two easier
findings, left that one, and reported the site as ready to show. Running the
checks and then shipping past them is worse than not running them, because now
there is a record saying the site was verified. Fix what fails. If you genuinely
cannot, say which check is still failing and why, in the same breath as telling
the user where things stand — never a green light with a red check behind it.

`{baseDir}/references/verifying.md` explains what each check means and what to
do when one fails.

## Which reference to open

Load only the one the task needs. Each is generated from Cloudflare's own
schema, so an endpoint listed there exists and one that is absent does not.

| Task | Reference |
|---|---|
| Deploy or change a Worker, secrets, cron, custom domains, **roll back a bad deploy** | `{baseDir}/references/workers.md` |
| SQL database — create, query, export, restore to a point in time | `{baseDir}/references/d1.md` |
| Images, uploads, backups, any file a site serves | `{baseDir}/references/r2.md` |
| Small fast key/value — config, counters, sessions | `{baseDir}/references/kv.md` |
| Put it on the user's domain; add a domain to Cloudflare; DNS records | `{baseDir}/references/dns.md` |
| A purely static site with no server code | `{baseDir}/references/pages.md` |
| Stop spam on a public form, free | `{baseDir}/references/turnstile.md` |
| Background jobs, retries, fan-out | `{baseDir}/references/queues.md` |
| Check a site you just deployed is actually good | `{baseDir}/references/verifying.md` |

Your training data about Cloudflare limits, pricing and payload shapes is
probably out of date. The references are the endpoint list; for request bodies
and current limits, fetch `https://developers.cloudflare.com/` rather than
guessing.

## The one call that is not obvious

Deploying a Worker is a **multipart PUT**, not JSON. This trips up every first
attempt, so it is written out once here:

```bash
curl -sX PUT \
  "https://api.cloudflare.com/client/v4/accounts/$USR_CLOUDFLARE_ACCOUNT_ID/workers/scripts/$NAME" \
  -H "Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN" \
  -F 'metadata={"main_module":"worker.js","compatibility_date":"2026-08-01",
        "bindings":[{"type":"d1","name":"DB","id":"'"$DB_ID"'"},
                    {"type":"secret_text","name":"API_KEY","text":"'"$SECRET"'"}]};type=application/json' \
  -F "worker.js=@orchestra/sites/$NAME/worker.js;type=application/javascript+module"
```

- `main_module` + `application/javascript+module` means an ES-module Worker
  (`export default { fetch }`). Omit both only for the old
  `addEventListener('fetch')` style.
- **Bindings are declared here, not in code.** A binding you forget is
  `undefined` at runtime, and the failure looks like a logic bug.
- A PUT **replaces the whole script**. There is no partial update.
- New scripts have no public URL until you enable it:
  `POST /workers/scripts/{name}/subdomain {"enabled":true}`.

## Where the project lives

One folder per site or app, under the workspace:

```
orchestra/sites/<name>/
  worker.js        the code you deploy
  schema.sql       the database, as created — kept current with every migration
  DESIGN.md        the design commitment (design-taste-frontend writes it)
  deploy.json      worker name, D1 id, R2 bucket, account id, custom domain,
                   and the site's admin / preview tokens
  README.md        one paragraph: what this is, whose it is, where it is live
```

`<name>` is the worker name. The next change to this site — yours or another
agent's, weeks later — starts by reading this folder, so it must be complete
enough to rebuild from. A site whose files sit loose in the workspace root
next to unrelated work has already been lost once.

**Write the folder first, then deploy from it.** Code that lives in `/tmp` or
only in your turn is not a project; it is gone when the turn ends. The first
site built after this rule was written was deployed from `/tmp` and only
moved into its folder when the person asked where it was. The deploy command
below reads `orchestra/sites/$NAME/worker.js` for that reason — if the file
is not there yet, put it there before you run it. And the record is
`deploy.json`, that name exactly, so the next reader finds it.

**`deploy.json` is a secret.** It holds tokens next to ids. It stays in this
folder; it is never uploaded to Files, quoted in chat, or pasted into a
report. When you need to tell the person where something is, tell them the
URL, not the record.

## Rules that exist because something broke

**Never deploy over a name you did not create.** A PUT to an existing script
replaces whatever is live there. A working blog was destroyed exactly this way:
a later project reused the worker name. Before deploying to a name you have not
used in this project, `GET /workers/scripts` and check. If it exists and is not
yours, pick another name.

**A deploy is recoverable — check before you panic.** Cloudflare keeps
deployment history: `GET /workers/scripts/{name}/deployments`. If you or the
user has just replaced something by accident, the previous version is very
likely still there.

**One database per application.** Do not point a second app at an existing D1
database "because it is already there". Two apps' tables in one database is how
a schema change for one silently breaks the other.

**Back up before destructive SQL.** D1 has `POST /d1/database/{id}/export` and
time-travel restore. Use them before a migration, not after a mistake.

**Secrets go in bindings, never in the script.** The source is readable via
`GET /workers/scripts/{name}/content/v2`. Anything you inline is disclosed.

## Putting it on the user's own domain

Cheapest correct path, in order:

1. The domain must be a zone on this Cloudflare account. `GET /zones?name=…` to
   check; `POST /zones` to add it. Adding a zone gives you **nameservers** the
   user must set at their registrar — that step is theirs, it is not automatic,
   and nothing works until it propagates.
2. Attach the Worker: `PUT /accounts/{account_id}/workers/domains` with the
   hostname, the zone id and the script name. Cloudflare creates the DNS record
   and the certificate for you.
3. Only use `POST /zones/{zone_id}/workers/routes` when you need a path pattern
   (`example.com/api/*`) rather than a whole hostname.

Do not hand-create a DNS record pointing at a Worker. The custom-domain endpoint
exists precisely so you do not have to, and it manages the certificate too.

## Before you touch a live site

Ask what is already running on that hostname. Moving a domain onto Cloudflare
moves **all** of it — if the user has email on that domain, the MX and TXT
records must be carried across or their mail stops. `GET /zones/{id}/dns_records`
after a zone is added, and compare against what their old provider had.

## Costs

Workers, D1, R2 and KV all have free tiers generous enough for a personal site
or a small business tool. Say so plainly when the user asks. Do not promise a
specific limit from memory — fetch the pricing page.
