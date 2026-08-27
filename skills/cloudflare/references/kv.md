# Workers KV — key/value

Generated from Cloudflare's OpenAPI schema — do not hand-edit.
Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`

Paths are relative to `https://api.cloudflare.com/client/v4`, with
`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —
prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.

14 endpoints.

| Method | Path | What it does | Required |
|---|---|---|---|
| GET | `/storage/kv/namespaces` | List Namespaces | — |
| POST | `/storage/kv/namespaces` | Create a Namespace | — |
| DELETE | `/storage/kv/namespaces/{namespace_id}` | Remove a Namespace | namespace_id |
| GET | `/storage/kv/namespaces/{namespace_id}` | Get a Namespace | namespace_id |
| PUT | `/storage/kv/namespaces/{namespace_id}` | Rename a Namespace | namespace_id |
| DELETE | `/storage/kv/namespaces/{namespace_id}/bulk` | Delete multiple key-value pairs | namespace_id |
| PUT | `/storage/kv/namespaces/{namespace_id}/bulk` | Write multiple key-value pairs | namespace_id |
| POST | `/storage/kv/namespaces/{namespace_id}/bulk/delete` | Delete multiple key-value pairs | namespace_id |
| POST | `/storage/kv/namespaces/{namespace_id}/bulk/get` | Get multiple key-value pairs | namespace_id, keys |
| GET | `/storage/kv/namespaces/{namespace_id}/keys` | List a Namespace's Keys | namespace_id |
| GET | `/storage/kv/namespaces/{namespace_id}/metadata/{key_name}` | Read the metadata for a key | key_name, namespace_id |
| DELETE | `/storage/kv/namespaces/{namespace_id}/values/{key_name}` | Delete key-value pair | key_name, namespace_id |
| GET | `/storage/kv/namespaces/{namespace_id}/values/{key_name}` | Read key-value pair | key_name, namespace_id |
| PUT | `/storage/kv/namespaces/{namespace_id}/values/{key_name}` | Write key-value pair with optional metadata | key_name, namespace_id |
