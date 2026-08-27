#!/usr/bin/env python3
"""
Deploy the blog Worker + its D1 database to Cloudflare.

Reusable on purpose. The first version of this in the wild was a one-off script
per project with the site's HTML pasted into a Python string, which meant every
edit regenerated the whole worker and nothing was reusable. This takes the
worker as a FILE and the site as DATA.

    python3 deploy.py --name my-blog --worker ../references/worker.js \
                      --schema ../references/schema.sql

Reads USR_CLOUDFLARE_API_TOKEN and USR_CLOUDFLARE_ACCOUNT_ID from the
environment. Writes nothing outside Cloudflare except --state.

SAFETY. It refuses to overwrite a worker it did not create, unless you pass
--force. A blog was lost that way: a later project reused the worker name and
replaced a live site. The state file is what remembers.
"""
import argparse, json, os, pathlib, secrets, sys, urllib.error, urllib.request

API = "https://api.cloudflare.com/client/v4"


def call(method, path, token, *, body=None, ctype="application/json", raw=False):
    data = body if raw else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Authorization": "Bearer " + token,
                                          **({"Content-Type": ctype} if data else {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:600]
        raise SystemExit(f"Cloudflare {method} {path} -> HTTP {e.code}\n{detail}")


def multipart(parts):
    """parts: list of (name, filename|None, content_type, bytes)."""
    boundary = "----orchestra" + secrets.token_hex(12)
    out = bytearray()
    for name, filename, ctype, payload in parts:
        out += f"--{boundary}\r\n".encode()
        disp = f'form-data; name="{name}"'
        if filename:
            disp += f'; filename="{filename}"'
        out += f"Content-Disposition: {disp}\r\nContent-Type: {ctype}\r\n\r\n".encode()
        out += payload + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def ensure_bucket(token, account, name):
    """R2 bucket for the blog's images. Created only if asked for: a blog whose
    author never posts a picture should not carry an empty bucket."""
    try:
        listing = call("GET", f"/accounts/{account}/r2/buckets", token)
    except SystemExit as e:
        # R2 is opt-in per account and the API says so with a 403, which reads
        # like a permissions problem and is not one.
        if "10042" in str(e) or "enable R2" in str(e):
            raise SystemExit(
                "R2 is not enabled on this Cloudflare account yet.\n"
                "Enable it once at https://dash.cloudflare.com/?to=/:account/r2 "
                "(no card needed for the free tier), then re-run with --media.\n"
                "Everything else deployed fine — images are the only thing waiting on this.")
        raise
    for b in (listing.get("result") or {}).get("buckets", []) or []:
        if b.get("name") == name:
            return False
    call("POST", f"/accounts/{account}/r2/buckets", token, body={"name": name})
    return True


def ensure_database(token, account, db_name):
    listing = call("GET", f"/accounts/{account}/d1/database?per_page=100", token)
    for db in listing.get("result") or []:
        if db.get("name") == db_name:
            return db["uuid"], False
    created = call("POST", f"/accounts/{account}/d1/database", token,
                   body={"name": db_name})
    return created["result"]["uuid"], True


def apply_schema(token, account, db_id, sql_path):
    sql = pathlib.Path(sql_path).read_text()
    call("POST", f"/accounts/{account}/d1/database/{db_id}/query", token, body={"sql": sql})


def deploy_worker(token, account, name, worker_path, db_id, admin_token, preview_token, compat_date, bucket=None):
    source = pathlib.Path(worker_path).read_bytes()
    metadata = {
        "main_module": "worker.js",
        # Pinned by the caller, not hardcoded to the day this script was written.
        "compatibility_date": compat_date,
        "bindings": [
            {"type": "d1", "name": "DB", "id": db_id},
            {"type": "secret_text", "name": "ADMIN_TOKEN", "text": admin_token},
            {"type": "secret_text", "name": "PREVIEW_TOKEN", "text": preview_token},
            # A binding the worker checks for rather than assumes: no bucket
            # means /media 404s, not that the blog breaks.
            *([{"type": "r2_bucket", "name": "MEDIA", "bucket_name": bucket}] if bucket else []),
        ],
    }
    body, ctype = multipart([
        ("metadata", None, "application/json", json.dumps(metadata).encode()),
        ("worker.js", "worker.js", "application/javascript+module", source),
    ])
    call("PUT", f"/accounts/{account}/workers/scripts/{name}", token,
         body=body, ctype=ctype, raw=True)
    # workers.dev is off by default on new scripts; turn it on so there is a
    # working URL before DNS exists. An account that has never opened the
    # Workers dashboard has no workers.dev subdomain at all — that is a
    # one-time manual step and NOT a reason to fail a good deploy.
    try:
        call("POST", f"/accounts/{account}/workers/scripts/{name}/subdomain", token,
             body={"enabled": True})
    except SystemExit:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="worker script name — becomes <name>.<subdomain>.workers.dev")
    ap.add_argument("--worker", required=True)
    ap.add_argument("--schema")
    ap.add_argument("--database", help="D1 name (default: <name>-blog)")
    ap.add_argument("--compat-date", default="2026-08-01")
    ap.add_argument("--media", nargs="?", const="", default=None,
                    help="create/bind an R2 bucket for images (default <name>-media)")
    ap.add_argument("--state", default="blog-deploy.json",
                    help="records what this script created, so it never clobbers someone else's worker")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    token = os.environ.get("USR_CLOUDFLARE_API_TOKEN")
    account = os.environ.get("USR_CLOUDFLARE_ACCOUNT_ID")
    if not token or not account:
        raise SystemExit("Set USR_CLOUDFLARE_API_TOKEN and USR_CLOUDFLARE_ACCOUNT_ID "
                         "(portal → Skills → cloudflare-blog → Set the keys).")

    state_path = pathlib.Path(a.state)
    state = json.loads(state_path.read_text()) if state_path.exists() else {}

    existing = [w["id"] for w in (call("GET", f"/accounts/{account}/workers/scripts", token).get("result") or [])]
    if a.name in existing and state.get("worker") != a.name and not a.force:
        raise SystemExit(
            f'A worker called "{a.name}" already exists and this state file did not create it.\n'
            f"Reusing a worker name REPLACES whatever is live at that name — a blog was lost this way.\n"
            f"Pick another --name, or pass --force if you are certain.")

    db_name = a.database or f"{a.name}-blog"
    db_id, created = ensure_database(token, account, db_name)
    print(f"D1 {db_name}: {'created' if created else 'exists'} ({db_id})")

    if a.schema:
        apply_schema(token, account, db_id, a.schema)
        print("schema applied")

    bucket = None
    if a.media is not None:
        bucket = a.media or f"{a.name}-media"
        made = ensure_bucket(token, account, bucket)
        print(f"R2 {bucket}: {'created' if made else 'exists'}")

    admin_token = state.get("admin_token") or secrets.token_urlsafe(32)
    preview_token = state.get("preview_token") or secrets.token_urlsafe(16)

    deploy_worker(token, account, a.name, a.worker, db_id, admin_token, preview_token, a.compat_date, bucket)
    print(f"worker {a.name}: deployed")

    state.update({"worker": a.name, "database": db_name, "database_id": db_id, "media_bucket": bucket,
                  "admin_token": admin_token, "preview_token": preview_token,
                  "account_id": account})
    state_path.write_text(json.dumps(state, indent=2))
    # 0600: the file holds the admin token that can write posts.
    os.chmod(state_path, 0o600)

    try:
        sub = (call("GET", f"/accounts/{account}/workers/subdomain", token).get("result") or {}).get("subdomain")
    except SystemExit:
        sub = None
    out = {
        "url": f"https://{a.name}.{sub}.workers.dev" if sub else None,
        "preview_path": f"/preview/<slug>?token={preview_token}",
        "state_file": str(state_path),
    }
    if not sub:
        out["next"] = ("This account has no workers.dev subdomain yet. Either open "
                       "Workers & Pages once in the Cloudflare dashboard to create one, "
                       "or attach a custom domain — see the cloudflare skill, references/dns.md.")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
