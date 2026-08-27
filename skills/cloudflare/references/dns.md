# Zones and DNS — putting a site on a domain

Generated from Cloudflare's OpenAPI schema — do not hand-edit.
Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`

Paths are relative to `https://api.cloudflare.com/client/v4`, with
`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —
prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.

16 endpoints.

| Method | Path | What it does | Required |
|---|---|---|---|
| DELETE | `/` | Delete Zone | — |
| GET | `/` | Zone Details | — |
| PATCH | `/` | Edit Zone | — |
| GET | `/dns_records` | List DNS Records | — |
| POST | `/dns_records` | Create DNS Record | — |
| POST | `/dns_records/batch` | Batch DNS Records | — |
| GET | `/dns_records/usage` | Get DNS Record Usage | — |
| DELETE | `/dns_records/{dns_record_id}` | Delete DNS Record | dns_record_id |
| GET | `/dns_records/{dns_record_id}` | DNS Record Details | dns_record_id |
| PATCH | `/dns_records/{dns_record_id}` | Update DNS Record | dns_record_id |
| PUT | `/dns_records/{dns_record_id}` | Overwrite DNS Record | dns_record_id |
| GET | `/registrar/domains` | List domains | — |
| GET | `/registrar/domains/{domain_name}` | Get domain | domain_name |
| PUT | `/registrar/domains/{domain_name}` | Update domain | domain_name |
| GET | `/zones` | List Zones | — |
| POST | `/zones` | Create Zone | name, account |
