<!-- Part of the `cloudflare` skill. Opened on demand — see SKILL.md. -->

# Checking a site you just deployed

You cannot see your own work. Every visual defect shipped from this skill so
far was invisible in the source and obvious in a browser:

- a headline running off the left edge, because a `margin` shorthand overwrote
  `margin: auto` on one section
- no favicon, so the browser tab showed a blank page icon
- a nav linking to routes that returned 404
- a homepage with no content on it, saying "coming soon"

None of those are catchable by reading code. So after every deploy, run:

```bash
python3 {baseDir}/scripts/verify-site.py https://your-site.example \
  --admin-path /api/admin/whatever --out ./verify
```

It renders the page in the headless Chromium already running on this instance,
saves screenshots at desktop and phone widths, and asserts:

| Check | Why it exists |
|---|---|
| homepage returns 200 | nothing else matters if it does not |
| no raw `<script>` in the served page | escaping actually applied |
| admin path 401s without a token, and with a wrong one | the write path is closed |
| no `sk-` / `cfat_` / `ghp_` strings served | the worker's source reads back through the API |
| no sideways scroll at either width | the commonest mobile break |
| a favicon exists | a blank tab icon reads as unfinished |
| the page has visible text | catches a shell with no content seeded |
| top-level blocks share a left edge | catches the margin-shorthand bug |
| every internal link resolves | catches a nav built before the routes |

Exit code is 0 only if nothing failed. Warnings are things to consider.

## Then open the screenshots

The checks are a floor, not a verdict. A page can pass every one of them and
still look wrong — bad rhythm, a headline that does not land, three type sizes
where one would do. Look at the images before you tell anyone it is finished.
