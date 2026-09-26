#!/usr/bin/env python3
"""
Post to X as the account that owns the keys, through X's official API v2.

WHY A SCRIPT AND NOT CURL. X signs every call with OAuth 1.0a: an HMAC-SHA1
over the method, the URL and the oauth parameters, keyed by the two secrets.
That is also why the four keys are plain variables and not secret-store
sentinels: the egress proxy can swap a sentinel into a header, but it cannot
re-sign a request.

NOTHING HERE RETRIES A WRITE. A post that failed was not published, and a
retried POST that did get through would publish twice.

    python3 x.py status                   are the four keys set? (free, sends nothing)
    python3 x.py whoami                   the account they post as (one paid read, <= US$0.01)
    python3 x.py check  --file draft.txt  length as X counts it, links, cost (free, sends nothing)
    python3 x.py post   --file draft.txt  [--quote ID|URL] [--reply-to ID|URL] [--long]
    python3 x.py thread --file thread.txt [--long]
    python3 x.py delete ID|URL

Text comes from --file (`-` reads stdin) or from the arguments. In a file, a
line holding only `---` separates the posts of a thread. Every command prints
one JSON object on stdout. Exit 0 = done, 1 = X refused or could not be
reached, 2 = nothing was sent (bad input or missing keys).
"""
import argparse, base64, hashlib, hmac, json, os, re, secrets, sys, time, unicodedata
import urllib.error, urllib.parse, urllib.request

API = "https://api.x.com"
KEYS = ("X_API_KEY", "X_API_KEY_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")

# X's pay-per-use prices, docs.x.com/x-api/getting-started/pricing (2026-09).
PRICE_POST = 0.015
PRICE_POST_WITH_LINK = 0.20
PRICE_SUMMONED_REPLY = 0.010

MAX_WEIGHTED = 280          # per post, as X counts; X Premium accounts may go longer
LINK_WEIGHT = 23            # every link counts 23, whatever its length


class XError(Exception):
    def __init__(self, status, message, hint=None):
        super().__init__(message)
        self.status, self.message, self.hint = status, message, hint


def out(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    sys.exit(code)


# ── OAuth 1.0a ────────────────────────────────────────────────────────────────

def pct(s):
    """RFC 3986 percent-encoding, the only encoding OAuth 1.0a signs."""
    return urllib.parse.quote(str(s), safe="-._~")


def signature_base(method, url, params):
    """The text OAuth 1.0a signs. `params` = oauth params + a form body; the
    query string is read from the URL. A JSON body is not part of it."""
    parts = urllib.parse.urlsplit(url)
    host = parts.hostname.lower()
    if parts.port and (parts.scheme, parts.port) not in (("https", 443), ("http", 80)):
        host = f"{host}:{parts.port}"
    base_url = f"{parts.scheme.lower()}://{host}{parts.path}"
    pairs = [(pct(k), pct(v)) for k, v in params]
    pairs += [(pct(k), pct(v)) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)]
    normalized = "&".join(f"{k}={v}" for k, v in sorted(pairs))
    return "&".join((method.upper(), pct(base_url), pct(normalized)))


def sign(base, consumer_secret, token_secret):
    key = f"{pct(consumer_secret)}&{pct(token_secret)}".encode()
    return base64.b64encode(hmac.new(key, base.encode(), hashlib.sha1).digest()).decode()


def authorization(method, url, keys, form=(), nonce=None, timestamp=None):
    oauth = {
        "oauth_consumer_key": keys["X_API_KEY"],
        "oauth_nonce": nonce or secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(timestamp or int(time.time())),
        "oauth_token": keys["X_ACCESS_TOKEN"],
        "oauth_version": "1.0",
    }
    base = signature_base(method, url, list(oauth.items()) + list(form))
    oauth["oauth_signature"] = sign(base, keys["X_API_KEY_SECRET"], keys["X_ACCESS_TOKEN_SECRET"])
    return "OAuth " + ", ".join(f'{pct(k)}="{pct(v)}"' for k, v in sorted(oauth.items()))


# ── keys ──────────────────────────────────────────────────────────────────────

# What X's keys look like. A mismatch is a warning, not a refusal: X is the judge.
SHAPES = {
    "X_API_KEY": (re.compile(r"^[A-Za-z0-9]{15,60}$"), "about 25 letters and digits"),
    "X_API_KEY_SECRET": (re.compile(r"^[A-Za-z0-9]{30,80}$"), "about 50 letters and digits"),
    "X_ACCESS_TOKEN": (re.compile(r"^\d+-[A-Za-z0-9]{10,80}$"), "digits, a dash, then letters and digits"),
    "X_ACCESS_TOKEN_SECRET": (re.compile(r"^[A-Za-z0-9]{30,80}$"), "about 45 letters and digits"),
}


def read_keys():
    """(keys, problems, warnings). Both lists name a key, never show its value."""
    keys, problems, warnings = {}, [], []
    for name in KEYS:
        v = (os.environ.get(name) or "").strip()
        keys[name] = v
        if not v or v.startswith("orchestra://secret-store/"):
            problems.append(f"{name} is not set")
        elif v.startswith("oc-sent-"):
            problems.append(f"{name} reaches this script sealed, because it was stored as a secret. X signs "
                            f"each request with it, so it must be stored as a plain variable: re-enter it on "
                            f"the skill's page")
        elif not SHAPES[name][0].match(v):
            warnings.append(f"{name} does not look like an X key (expected {SHAPES[name][1]})")
    return keys, problems, warnings


def require_keys():
    keys, problems, warnings = read_keys()
    if problems:
        out({"ok": False, "sent": False, "problems": problems, "warnings": warnings,
             "fix": "Add the four keys on this skill's page in the Orchestra portal. Never ask for them in the chat."}, 2)
    return keys, ({"warnings": warnings} if warnings else {})


# ── counting as X does ────────────────────────────────────────────────────────

# Code points X counts as ONE character; everything else counts two
# (twitter-text v3: Latin, Greek, Cyrillic, Hebrew, Arabic… and some punctuation).
LIGHT = ((0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037))
TLDS = ("com|net|org|io|ai|co|dev|app|me|tv|ly|gg|so|sh|to|xyz|info|biz|news|blog|shop|"
        "es|ar|mx|cl|uy|pe|br|uk|de|fr|it|pt|nl|eu|us|ca|au|in|jp")
LINK_RE = re.compile(
    r"(?<![@\w.])(?:https?://[^\s<>\"]+|www\.[^\s<>\"]+|(?:[a-z0-9-]+\.)+(?:" + TLDS + r")\b(?:/[^\s<>\"]*)?)",
    re.I)
TRAILING = ".,;:!?)]}'\"…"


def _light(cp):
    return any(a <= cp <= b for a, b in LIGHT)


def _emoji(cp):
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF or 0x2B00 <= cp <= 0x2BFF
            or 0x2190 <= cp <= 0x21FF or 0x2300 <= cp <= 0x23FF or 0x25A0 <= cp <= 0x25FF)


def _weigh(text):
    """Weight of plain text in hundredths: an emoji sequence = 200, a flag = 200."""
    cps = [ord(c) for c in text]
    w, i = 0, 0
    while i < len(cps):
        cp = cps[i]
        if 0x1F1E6 <= cp <= 0x1F1FF and i + 1 < len(cps) and 0x1F1E6 <= cps[i + 1] <= 0x1F1FF:
            w, i = w + 200, i + 2                          # a flag is two regional indicators
            continue
        if _emoji(cp):
            w, i = w + 200, i + 1
            while i < len(cps):                           # modifiers and joined emoji are the same glyph
                c = cps[i]
                if c in (0xFE0E, 0xFE0F) or 0x1F3FB <= c <= 0x1F3FF or 0xE0020 <= c <= 0xE007F:
                    i += 1
                elif c == 0x200D and i + 1 < len(cps):
                    i += 2
                else:
                    break
            continue
        if cp in (0xFE0E, 0xFE0F):                        # a variation selector adds nothing
            i += 1
            continue
        if cp == 0x20E3:                                  # keycap: its digit already counted one
            w, i = w + 100, i + 1
            continue
        w, i = w + (100 if _light(cp) else 200), i + 1
    return w


def measure(text):
    """{length, links} as X counts: NFC, each link 23, emoji and CJK 2."""
    text = unicodedata.normalize("NFC", text)
    links, weight, pos = [], 0, 0
    for m in LINK_RE.finditer(text):
        link = m.group(0).rstrip(TRAILING)
        if "." not in link:
            continue
        weight += _weigh(text[pos:m.start()]) + LINK_WEIGHT * 100
        links.append(link)
        pos = m.start() + len(link)
    weight += _weigh(text[pos:])
    return {"length": (weight + 99) // 100, "links": links}


def price(links, reply_to=None):
    if links:
        return PRICE_POST_WITH_LINK
    return PRICE_SUMMONED_REPLY if reply_to else PRICE_POST


def review(posts, long_ok=False, reply_to=None):
    """Per-post report, and whether all of it may be sent. Sends nothing."""
    report, ok = [], True
    for n, text in enumerate(posts, 1):
        m = measure(text)
        issues = []
        if not text.strip():
            issues.append("empty")
        if m["length"] > MAX_WEIGHTED and not long_ok:
            issues.append(f"{m['length']} characters as X counts them; the limit is {MAX_WEIGHTED} "
                          f"(longer only on X Premium accounts, with --long)")
        ok = ok and not issues
        report.append({"n": n, "length": m["length"], "links": m["links"],
                       "cost_usd": price(m["links"], reply_to if n == 1 else None),
                       "issues": issues, "text": text})
    return ok, report


# ── input ─────────────────────────────────────────────────────────────────────

def read_posts(args, each_arg_is_a_post=False):
    if args.file:
        with (sys.stdin if args.file == "-" else open(args.file, encoding="utf-8")) as f:
            chunks = re.split(r"(?m)^[ \t]*---[ \t]*$", f.read())
    elif each_arg_is_a_post:
        chunks = list(args.text or [])
    else:
        chunks = [" ".join(args.text or [])]
    return [p for p in (c.strip() for c in chunks) if p] or [""]


def post_id(ref):
    """An id from an id or a post URL (x.com/<user>/status/<id>, twitter.com too)."""
    ref = str(ref or "").strip()
    m = re.search(r"/status(?:es)?/(\d+)", ref) or re.fullmatch(r"(\d+)", ref)
    if not m:
        out({"ok": False, "sent": False, "error": f"not a post id or post URL: {ref!r}"}, 2)
    return m.group(1)


def post_url(pid):
    return f"https://x.com/i/web/status/{pid}"


# ── the API ───────────────────────────────────────────────────────────────────

def explain(status, payload):
    """X's refusal, and what the person can do about it."""
    msg = str(payload.get("detail") or payload.get("title") or "")
    errs = payload.get("errors")
    if isinstance(errs, list):
        more = [str(e.get("message") or e.get("detail") or "") for e in errs if isinstance(e, dict)]
        msg = "; ".join(x for x in [msg] + more if x)
    msg = msg or f"HTTP {status}"
    low = (msg + " " + json.dumps(payload)).lower()
    hint = None
    if status == 401:
        hint = ("X rejected the keys: one of the four is wrong, or was regenerated in console.x.com "
                "(regenerating invalidates the old one at once). Re-enter all four on the skill's page.")
    elif "oauth1" in low and "permission" in low:
        hint = ("The X app is read-only. In console.x.com → the app → User authentication settings, set "
                "App permissions to 'Read and write', then REGENERATE the Access Token and Secret (a token "
                "made before the change stays read-only) and re-enter those two.")
    elif "duplicate" in low:
        hint = "X refuses a post identical to one the account published recently. Change the text."
    elif "reply" in low and ("mention" in low or "not allowed" in low or "engaged" in low):
        hint = ("Since February 2026 X lets an app reply to someone else's post only when that post's author "
                "@mentioned this account or quoted it. Offer a quote post instead, or the person replies by hand.")
    elif status == 402 or "credit" in low or "spend" in low or "billing" in low:
        hint = "No API credit left, or the spending limit was reached: add credit at console.x.com."
    elif status == 429:
        hint = "Too many requests. Wait a few minutes; nothing in this call was published."
    return msg, hint


def call(method, path, keys, body=None):
    url = API + path
    headers = {"Authorization": authorization(method, url, keys), "User-Agent": "orchestra-x-skill/0.1"}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = {"detail": raw.decode("utf-8", "replace")[:300]}
        raise XError(e.code, *explain(e.code, payload if isinstance(payload, dict) else {}))
    except urllib.error.URLError as e:
        raise XError(0, f"could not reach api.x.com: {e.reason}")


def create(keys, text, reply_to=None, quote=None):
    body = {"text": text}
    if reply_to:
        body["reply"] = {"in_reply_to_tweet_id": reply_to}
    if quote:
        body["quote_tweet_id"] = quote
    data = call("POST", "/2/tweets", keys, body).get("data") or {}
    if not data.get("id"):
        raise XError(0, "X answered without a post id: look at the account before posting again")
    return data["id"]


def failed(e, **extra):
    res = {"ok": False, "error": e.message}
    if e.status:
        res["status"] = e.status
    if e.hint:
        res["fix"] = e.hint
    res.update(extra)
    out(res, 1)


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_status(_args):
    keys, problems, warnings = read_keys()
    out({"ok": not problems, "keys": {k: bool(keys[k]) for k in KEYS}, "problems": problems,
         "warnings": warnings,
         "note": "Checks that the keys are there, sends nothing. `whoami` asks X which account they belong to."},
        0 if not problems else 2)


def cmd_whoami(_args):
    keys, extra = require_keys()
    try:
        data = call("GET", "/2/users/me", keys).get("data") or {}
    except XError as e:
        failed(e, **extra)
    user = data.get("username")
    out({"ok": True, "id": data.get("id"), "username": user, "name": data.get("name"),
         "url": f"https://x.com/{user}" if user else None})


def cmd_check(args):
    ok, report = review(read_posts(args), args.long, args.reply_to)
    out({"ok": ok, "sent": False, "posts": report,
         "total_cost_usd": round(sum(p["cost_usd"] for p in report), 3)}, 0 if ok else 2)


def cmd_post(args):
    posts = read_posts(args)
    if len(posts) > 1:
        out({"ok": False, "sent": False, "error": "the text holds several posts (--- lines); use `thread`"}, 2)
    reply_to = post_id(args.reply_to) if args.reply_to else None
    quote = post_id(args.quote) if args.quote else None
    ok, report = review(posts, args.long, reply_to)
    if not ok:
        out({"ok": False, "sent": False, "posts": report}, 2)
    keys, extra = require_keys()
    try:
        pid = create(keys, posts[0], reply_to=reply_to, quote=quote)
    except XError as e:
        failed(e, sent=False, **extra)
    out({"ok": True, "id": pid, "url": post_url(pid), "cost_usd": report[0]["cost_usd"]})


def cmd_thread(args):
    posts = read_posts(args, each_arg_is_a_post=True)
    ok, report = review(posts, args.long)
    if not ok:
        out({"ok": False, "sent": False, "posts": report}, 2)
    keys, extra = require_keys()
    published, parent = [], None
    for n, text in enumerate(posts, 1):
        try:
            parent = create(keys, text, reply_to=parent)
        except XError as e:
            failed(e, failed_at=n, published=published, **extra,
                   note="Posts under `published` are live. Do not publish them again: continue from "
                        "`failed_at` as a reply to the last one, or delete them.")
        published.append({"n": n, "id": parent, "url": post_url(parent)})
    out({"ok": True, "url": published[0]["url"], "posts": published,
         "cost_usd": round(sum(p["cost_usd"] for p in report), 3)})


def cmd_delete(args):
    pid = post_id(args.ref)
    keys, extra = require_keys()
    try:
        data = call("DELETE", f"/2/tweets/{pid}", keys).get("data") or {}
    except XError as e:
        failed(e, **extra)
    deleted = bool(data.get("deleted"))
    out({"ok": deleted, "id": pid, "deleted": deleted}, 0 if deleted else 1)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(prog="x.py", description="Post to X with the account's own API keys.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="are the four keys set (free)").set_defaults(fn=cmd_status)
    sub.add_parser("whoami", help="the account the keys post as (one paid read)").set_defaults(fn=cmd_whoami)
    for name, fn, helptext in (("check", cmd_check, "length, links and cost; sends nothing"),
                               ("post", cmd_post, "publish one post"),
                               ("thread", cmd_thread, "publish several posts as a thread")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("text", nargs="*", help="the text (thread: one argument per post); prefer --file")
        p.add_argument("--file", help="read the text from this file (- for stdin); --- lines separate posts")
        p.add_argument("--long", action="store_true", help="allow over 280 (X Premium accounts only)")
        if name in ("check", "post"):
            p.add_argument("--reply-to", help="id or URL of the post this replies to")
        if name == "post":
            p.add_argument("--quote", help="id or URL of the post this quotes")
        p.set_defaults(fn=fn)
    d = sub.add_parser("delete", help="delete one of the account's posts")
    d.add_argument("ref", help="post id or URL")
    d.set_defaults(fn=cmd_delete)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
