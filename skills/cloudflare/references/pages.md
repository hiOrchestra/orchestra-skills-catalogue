# Pages — static sites

Generated from Cloudflare's OpenAPI schema — do not hand-edit.
Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`

Paths are relative to `https://api.cloudflare.com/client/v4`, with
`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —
prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.

23 endpoints.

| Method | Path | What it does | Required |
|---|---|---|---|
| GET | `/pages/projects` | Get projects | — |
| POST | `/pages/projects` | Create project | name, production_branch |
| DELETE | `/pages/projects/{project_name}` | Delete project | project_name |
| GET | `/pages/projects/{project_name}` | Get project | project_name |
| PATCH | `/pages/projects/{project_name}` | Update project | project_name |
| GET | `/pages/projects/{project_name}/deployments` | Get deployments | project_name |
| POST | `/pages/projects/{project_name}/deployments` | Create deployment | project_name |
| DELETE | `/pages/projects/{project_name}/deployments/{deployment_id}` | Delete deployment | deployment_id, project_name |
| GET | `/pages/projects/{project_name}/deployments/{deployment_id}` | Get deployment info | deployment_id, project_name |
| GET | `/pages/projects/{project_name}/deployments/{deployment_id}/history/logs` | Get deployment logs | deployment_id, project_name |
| POST | `/pages/projects/{project_name}/deployments/{deployment_id}/retry` | Retry deployment | deployment_id, project_name |
| POST | `/pages/projects/{project_name}/deployments/{deployment_id}/rollback` | Rollback deployment | deployment_id, project_name |
| POST | `/pages/projects/{project_name}/deployments/{deployment_id}/tails` | Create deployment tail | deployment_id, project_name |
| DELETE | `/pages/projects/{project_name}/deployments/{deployment_id}/tails/{tail_id}` | Delete deployment tail | tail_id, deployment_id, project_name |
| GET | `/pages/projects/{project_name}/domains` | Get domains | project_name |
| POST | `/pages/projects/{project_name}/domains` | Add domain | project_name, name |
| DELETE | `/pages/projects/{project_name}/domains/{domain_name}` | Delete domain | domain_name, project_name |
| GET | `/pages/projects/{project_name}/domains/{domain_name}` | Get domain | domain_name, project_name |
| PATCH | `/pages/projects/{project_name}/domains/{domain_name}` | Patch domain | domain_name, project_name |
| POST | `/pages/projects/{project_name}/purge_build_cache` | Purge build cache | project_name |
| DELETE | `/pages/projects/{project_name}/source` | Disconnect project source | project_name |
| POST | `/pages/projects/{project_name}/source` | Connect project source | project_name |
| GET | `/pages/projects/{project_name}/upload-token` | Get upload token | project_name |
