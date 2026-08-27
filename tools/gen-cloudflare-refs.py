#!/usr/bin/env python3
"""
Generate the `cloudflare` skill's reference files from Cloudflare's OpenAPI spec.

WHY GENERATED. A hand-written API reference is wrong the day after it is
written, and an agent that reads a hallucinated endpoint fails in a way that
looks like the agent's fault. Everything in references/ is derived from the
published schema, so the skill cannot claim an endpoint that does not exist.

WEEKLY MAINTENANCE (developer side, from a terminal):
    python3 tools/gen-cloudflare-refs.py --fetch
    git diff skills/cloudflare/references
A non-empty diff is Cloudflare changing its API. Read it, adjust the SKILL.md
prose if the change is semantic, bump the version in catalog.json, push. Every
tenant then sees "update available" through the normal path.

    --fetch   re-download the spec (24MB) before generating
"""
import argparse, json, os, pathlib, re, sys, urllib.request

SPEC_URL = "https://raw.githubusercontent.com/cloudflare/api-schemas/main/openapi.json"
SPEC_PATH = pathlib.Path(os.environ.get("CF_SPEC", "/tmp/cfapi.json"))
OUT = pathlib.Path(__file__).resolve().parent.parent / "skills" / "cloudflare" / "references"

# Each reference file is one product area. `include` is matched against the
# path; `exclude` removes the long tail that would drown the useful calls.
SECTIONS = [
    ("workers.md", "Workers — deploy, configure, roll back", [
        r"/accounts/\{[^}]+\}/workers/scripts",
        r"/accounts/\{[^}]+\}/workers/subdomain",
        r"/accounts/\{[^}]+\}/workers/domains",
        r"/zones/\{[^}]+\}/workers/routes",
        r"/accounts/\{[^}]+\}/workers/deployments",
    ], [r"/dispatch/", r"/versions/\{", r"/assets/", r"/observability/"]),
    ("d1.md", "D1 — SQLite databases", [r"/accounts/\{[^}]+\}/d1/"], []),
    ("r2.md", "R2 — object storage for images, files and backups", [r"/accounts/\{[^}]+\}/r2/"], [r"/sippy", r"/metrics"]),
    ("kv.md", "Workers KV — key/value", [r"/accounts/\{[^}]+\}/storage/kv/"], []),
    ("dns.md", "Zones and DNS — putting a site on a domain", [
        r"^/zones(/\{[^}]+\})?$",
        r"/zones/\{[^}]+\}/dns_records",
        r"^/accounts/\{[^}]+\}/registrar/domains",
    ], [r"/scan", r"/export", r"/import"]),
    ("pages.md", "Pages — static sites", [r"/accounts/\{[^}]+\}/pages/"], []),
    ("turnstile.md", "Turnstile — free CAPTCHA for forms", [r"/accounts/\{[^}]+\}/challenges/widgets"], []),
    ("queues.md", "Queues — background work", [r"/accounts/\{[^}]+\}/queues"], []),
]


def load_spec():
    if not SPEC_PATH.exists():
        raise SystemExit(f"No spec at {SPEC_PATH}. Run with --fetch.")
    return json.loads(SPEC_PATH.read_text())


def fetch_spec():
    print(f"downloading {SPEC_URL} …", file=sys.stderr)
    urllib.request.urlretrieve(SPEC_URL, SPEC_PATH)
    print(f"saved {SPEC_PATH} ({SPEC_PATH.stat().st_size // 1024 // 1024} MB)", file=sys.stderr)


def clean(text, limit=180):
    """One line, no markdown tables inside a table cell."""
    t = re.sub(r"\s+", " ", (text or "").strip())
    t = t.replace("|", "/").replace("`", "")
    return (t[:limit] + "…") if len(t) > limit else t


def params_for(op, spec):
    req = []
    for p in op.get("parameters", []) or []:
        if "$ref" in p:
            continue
        if p.get("required") and p.get("in") in ("query", "path"):
            if p["name"] not in ("account_id", "zone_id"):
                req.append(p["name"])
    body = op.get("requestBody") or {}
    content = (body.get("content") or {})
    for ctype, media in content.items():
        sch = media.get("schema") or {}
        for r in (sch.get("required") or [])[:6]:
            req.append(r)
        break
    return ", ".join(dict.fromkeys(req)) or "—"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch_spec()
    spec = load_spec()
    paths = spec["paths"]
    OUT.mkdir(parents=True, exist_ok=True)

    index = []
    for filename, title, includes, excludes in SECTIONS:
        rows = []
        for path, ops in sorted(paths.items()):
            if not any(re.search(p, path) for p in includes):
                continue
            if any(re.search(x, path) for x in excludes):
                continue
            for method, op in ops.items():
                if method not in ("get", "post", "put", "patch", "delete"):
                    continue
                short = (path.replace("/accounts/{account_id}", "")
                             .replace("/zones/{zone_id}", "")
                             .replace("/accounts/{accountId}", ""))
                rows.append((method.upper(), short or "/", clean(op.get("summary") or op.get("operationId")), params_for(op, spec)))
        rows.sort(key=lambda r: (r[1], r[0]))
        body = [f"# {title}", "",
                "Generated from Cloudflare's OpenAPI schema — do not hand-edit.",
                "Regenerate: `python3 tools/gen-cloudflare-refs.py --fetch`", "",
                "Paths are relative to `https://api.cloudflare.com/client/v4`, with",
                "`/accounts/{account_id}` or `/zones/{zone_id}` omitted for brevity —",
                "prefix them back on. Auth is `Authorization: Bearer $USR_CLOUDFLARE_API_TOKEN`.",
                "", f"{len(rows)} endpoints.", "",
                "| Method | Path | What it does | Required |",
                "|---|---|---|---|"]
        for m, p, s, req in rows:
            body.append(f"| {m} | `{p}` | {s} | {req} |")
        (OUT / filename).write_text("\n".join(body) + "\n")
        index.append((filename, title, len(rows)))
        print(f"{filename:16} {len(rows):4} endpoints")

    print(f"\ntotal: {sum(n for _, _, n in index)} endpoints across {len(index)} references")


if __name__ == "__main__":
    main()
