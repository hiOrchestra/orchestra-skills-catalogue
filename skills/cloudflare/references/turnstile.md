# Turnstile — free CAPTCHA for forms

Generated from Cloudflare's OpenAPI schema — do not hand-edit.
Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`

Paths are relative to `https://api.cloudflare.com/client/v4`, with
`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —
prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.

6 endpoints.

| Method | Path | What it does | Required |
|---|---|---|---|
| GET | `/challenges/widgets` | List Turnstile Widgets | — |
| POST | `/challenges/widgets` | Create a Turnstile Widget | name, mode, domains |
| DELETE | `/challenges/widgets/{sitekey}` | Delete a Turnstile Widget | — |
| GET | `/challenges/widgets/{sitekey}` | Turnstile Widget Details | — |
| PUT | `/challenges/widgets/{sitekey}` | Update a Turnstile Widget | name, mode, domains |
| POST | `/challenges/widgets/{sitekey}/rotate_secret` | Rotate Secret for a Turnstile Widget | — |
