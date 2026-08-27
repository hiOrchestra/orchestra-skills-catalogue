# Queues — background work

Generated from Cloudflare's OpenAPI schema — do not hand-edit.
Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`

Paths are relative to `https://api.cloudflare.com/client/v4`, with
`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —
prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.

23 endpoints.

| Method | Path | What it does | Required |
|---|---|---|---|
| GET | `/queues` | List Queues | — |
| POST | `/queues` | Create Queue | queue_name |
| DELETE | `/queues/{queue_id}` | Delete Queue | queue_id |
| GET | `/queues/{queue_id}` | Get Queue | queue_id |
| PATCH | `/queues/{queue_id}` | Update Queue | queue_id |
| PUT | `/queues/{queue_id}` | Update Queue | queue_id |
| GET | `/queues/{queue_id}/consumers` | List Queue Consumers | queue_id |
| POST | `/queues/{queue_id}/consumers` | Create a Queue Consumer | queue_id |
| DELETE | `/queues/{queue_id}/consumers/{consumer_id}` | Delete Queue Consumer | consumer_id, queue_id |
| GET | `/queues/{queue_id}/consumers/{consumer_id}` | Get Queue Consumer | consumer_id, queue_id |
| PUT | `/queues/{queue_id}/consumers/{consumer_id}` | Update Queue Consumer | consumer_id, queue_id |
| POST | `/queues/{queue_id}/messages` | Push Message | queue_id |
| POST | `/queues/{queue_id}/messages/ack` | Acknowledge + Retry Queue Messages | queue_id |
| POST | `/queues/{queue_id}/messages/batch` | Push Message Batch | queue_id |
| POST | `/queues/{queue_id}/messages/extend` | Extend Message Leases | queue_id |
| POST | `/queues/{queue_id}/messages/peek` | Peek Queue Messages | queue_id |
| POST | `/queues/{queue_id}/messages/preview` | Preview Queue Messages | queue_id |
| POST | `/queues/{queue_id}/messages/preview/ack` | Delete Previewed Queue Messages | queue_id |
| POST | `/queues/{queue_id}/messages/pull` | Pull Queue Messages | queue_id |
| POST | `/queues/{queue_id}/messages/purge` | Purge Peeked Queue Messages | queue_id, refs |
| GET | `/queues/{queue_id}/metrics` | Get Queue Metrics | queue_id |
| GET | `/queues/{queue_id}/purge` | Get Queue Purge Status | queue_id |
| POST | `/queues/{queue_id}/purge` | Purge Queue | queue_id |
