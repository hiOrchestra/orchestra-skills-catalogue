# Workers — deploy, configure, roll back

Generated from Cloudflare's OpenAPI schema — do not hand-edit.
Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`

Paths are relative to `https://api.cloudflare.com/client/v4`, with
`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —
prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.

45 endpoints.

| Method | Path | What it does | Required |
|---|---|---|---|
| GET | `/workers/domains` | List Domains | — |
| PUT | `/workers/domains` | Attach Domain | — |
| DELETE | `/workers/domains/{domain_id}` | Detach Domain | domain_id |
| GET | `/workers/domains/{domain_id}` | Get Domain | domain_id |
| GET | `/workers/routes` | List Routes | — |
| POST | `/workers/routes` | Create Route | — |
| DELETE | `/workers/routes/{route_id}` | Delete Route | route_id |
| GET | `/workers/routes/{route_id}` | Get Route | route_id |
| PUT | `/workers/routes/{route_id}` | Update Route | route_id |
| GET | `/workers/scripts` | List Workers | — |
| GET | `/workers/scripts-search` | Search Workers | — |
| DELETE | `/workers/scripts/{script_name}` | Delete Worker | script_name |
| GET | `/workers/scripts/{script_name}` | Download Worker | script_name |
| PUT | `/workers/scripts/{script_name}` | Upload Worker Module | script_name |
| POST | `/workers/scripts/{script_name}/assets-upload-session` | Create Assets Upload Session | script_name |
| PUT | `/workers/scripts/{script_name}/content` | Put script content | script_name, metadata |
| GET | `/workers/scripts/{script_name}/content/v2` | Get script content | script_name |
| GET | `/workers/scripts/{script_name}/deployments` | List Deployments | script_name |
| POST | `/workers/scripts/{script_name}/deployments` | Create Deployment | script_name |
| DELETE | `/workers/scripts/{script_name}/deployments/{deployment_id}` | Delete Deployment | script_name, deployment_id |
| GET | `/workers/scripts/{script_name}/deployments/{deployment_id}` | Get Deployment | script_name, deployment_id |
| GET | `/workers/scripts/{script_name}/schedules` | Get Cron Triggers | script_name |
| PUT | `/workers/scripts/{script_name}/schedules` | Update Cron Triggers | script_name |
| GET | `/workers/scripts/{script_name}/script-settings` | Get Script Settings | script_name |
| PATCH | `/workers/scripts/{script_name}/script-settings` | Patch Script Settings | script_name |
| GET | `/workers/scripts/{script_name}/secrets` | List script secrets | script_name |
| PUT | `/workers/scripts/{script_name}/secrets` | Add script secret | script_name |
| PATCH | `/workers/scripts/{script_name}/secrets-bulk` | Patch multiple script secrets | script_name |
| DELETE | `/workers/scripts/{script_name}/secrets/{secret_name}` | Delete script secret | script_name, secret_name |
| GET | `/workers/scripts/{script_name}/secrets/{secret_name}` | Get secret binding | script_name, secret_name |
| GET | `/workers/scripts/{script_name}/settings` | Get Settings | script_name |
| PATCH | `/workers/scripts/{script_name}/settings` | Patch Settings | script_name |
| DELETE | `/workers/scripts/{script_name}/subdomain` | Delete Worker subdomain | script_name |
| GET | `/workers/scripts/{script_name}/subdomain` | Get Worker subdomain | script_name |
| POST | `/workers/scripts/{script_name}/subdomain` | Post Worker subdomain | script_name, enabled |
| GET | `/workers/scripts/{script_name}/tails` | List Tails | script_name |
| POST | `/workers/scripts/{script_name}/tails` | Start Tail | script_name |
| DELETE | `/workers/scripts/{script_name}/tails/{id}` | Delete Tail | script_name, id |
| GET | `/workers/scripts/{script_name}/usage-model` | Fetch Usage Model | script_name |
| PUT | `/workers/scripts/{script_name}/usage-model` | Update Usage Model | script_name |
| GET | `/workers/scripts/{script_name}/versions` | List Versions | script_name |
| POST | `/workers/scripts/{script_name}/versions` | Upload Version | script_name |
| DELETE | `/workers/subdomain` | Delete Subdomain | — |
| GET | `/workers/subdomain` | Get Subdomain | — |
| PUT | `/workers/subdomain` | Create Subdomain | — |
