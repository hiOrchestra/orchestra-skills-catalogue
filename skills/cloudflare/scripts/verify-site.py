#!/usr/bin/env python3
"""
Check a site you just deployed, and LOOK at it.

WHY THIS EXISTS. An agent cannot see its own work. Every visual defect shipped
so far was invisible from the source and obvious in a browser: a headline
running off the left edge because a `margin` shorthand overwrote `margin:auto`,
a missing favicon, a nav linking to routes that 404, a homepage with no content
on it. The source looked fine in all four cases.

So this does two things a source review cannot: it renders the page in the
headless Chromium already running on the instance and saves screenshots for you
to open, and it asserts the handful of properties that must hold on anything
public.

    python3 verify-site.py https://example.workers.dev
    python3 verify-site.py https://example.workers.dev --admin-path /api/admin/posts

Exit code is 0 only if nothing FAILED. Warnings do not fail the run — they are
things to consider, not rules.

LOOK AT THE SCREENSHOTS. Passing every check below and still looking wrong is
entirely possible; that is what your eyes are for.
"""
import argparse, base64, json, os, re, socket, sys, urllib.error, urllib.request

CDP = os.environ.get("CDP_URL", "http://127.0.0.1:18800")
WIDTHS = [(1440, 900, "desktop"), (390, 844, "phone")]

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results = []


def record(status, name, detail=""):
    results.append((status, name, detail))
    mark = {PASS: "  ok  ", FAIL: " FAIL ", WARN: " warn "}[status]
    print(f"{mark} {name}" + (f" — {detail}" if detail else ""))


# Cloudflare answers urllib's default User-Agent with a 403, which reads as
# "the site is broken" when it means "you look like a bot". Ask like a browser.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/149.0 Safari/537.36")


def fetch(url, method="GET", headers=None):
    h = {"User-Agent": UA, "Accept": "*/*"}
    h.update(headers or {})
    req = urllib.request.Request(url, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), dict(e.headers or {})
    except Exception as e:
        return 0, str(e), {}


# ── rendering, via the Chromium already on the box ──────────────────────────
def default_out_dir():
    """Screenshots go in the Orchestra namespace, never beside the script.

    The obvious place to run this from is the directory it lives in, and "./verify"
    then writes into the SKILL — which the catalogue updater prunes, because a
    file it did not install has no business being there. On the first real run
    that turned into an update that could not complete: the updater tried to
    remove the screenshots, could not, and aborted. Output belongs somewhere the
    skill's own lifecycle does not reach.
    """
    base = os.environ.get("OPENCLAW_DIR") or os.path.join(os.path.expanduser("~"), ".openclaw")
    return os.path.join(base, "orchestra", "site-verify")


def cdp_render(url, out_dir):
    """Screenshot at each width and pull back geometry, by shelling out to the
    Node renderer beside this file — Node has `ws`, the instance Python does
    not. Returns None if the browser is unreachable; a missing browser is a
    warning, not a failure."""
    import subprocess
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render-and-measure.js")
    try:
        r = subprocess.run(["node", script, url, out_dir], capture_output=True, text=True, timeout=180)
    except Exception as e:
        record(WARN, "headless browser", f"could not run the renderer ({e}); skipping the visual checks")
        return None
    if r.returncode != 0 or not r.stdout.strip():
        record(WARN, "headless browser", (r.stderr or "renderer produced nothing").strip()[:160])
        return None
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        record(WARN, "headless browser", "renderer output was not JSON")
        return None
    if data.get("error"):
        record(WARN, "headless browser", data["error"] + "; skipping the visual checks")
        return None
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--admin-path", default="/api/admin", help="a path that must require a token")
    ap.add_argument("--out", default=default_out_dir(),
                    help="where screenshots go (default: the Orchestra namespace, never the skill)")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    os.makedirs(a.out, exist_ok=True)

    print(f"\nverifying {base}\n" + "-" * 60)

    # ── it is up, and it has something on it ────────────────────────────────
    status, body, headers = fetch(base + "/")
    if status == 200:
        record(PASS, "homepage responds", "200")
    else:
        record(FAIL, "homepage responds", f"HTTP {status}")
        print("\nnothing else is worth checking until the homepage loads.")
        sys.exit(1)

    # ── a stranger's input must not become HTML ─────────────────────────────
    payload = '<script>alert(1)</script>'
    if payload in body:
        record(FAIL, "no unescaped markup on the homepage", "a raw <script> tag is being served")
    else:
        record(PASS, "no unescaped markup on the homepage")

    # ── admin is closed ─────────────────────────────────────────────────────
    st_noauth, _, _ = fetch(base + a.admin_path)
    st_bad, _, _ = fetch(base + a.admin_path, headers={"Authorization": "Bearer definitely-not-the-token"})
    if st_noauth in (401, 403) and st_bad in (401, 403):
        record(PASS, "admin requires a token", f"{st_noauth} / {st_bad}")
    elif st_noauth == 404 and st_bad == 404:
        record(WARN, "admin path not found", f"{a.admin_path} 404s — pass --admin-path if it lives elsewhere")
    else:
        record(FAIL, "admin requires a token", f"no-auth {st_noauth}, wrong-token {st_bad}")

    # ── no secrets in what is served ────────────────────────────────────────
    leaked = re.findall(r"(?:sk-|cfat_|ghp_|xox[baprs]-)[A-Za-z0-9_-]{16,}", body)
    record(FAIL if leaked else PASS, "no secrets in the served page",
           f"{len(leaked)} token-like strings" if leaked else "")

    # ── render and look ─────────────────────────────────────────────────────
    geo = cdp_render(base + "/", a.out)
    if geo:
        for label, g in geo.items():
            if g["scrollWidth"] > g["innerWidth"] + 1:
                record(FAIL, f"no sideways scroll ({label})",
                       f"page is {g['scrollWidth']}px in a {g['innerWidth']}px window")
            else:
                record(PASS, f"no sideways scroll ({label})")

        d = geo.get("desktop")
        if d:
            record(PASS if d["favicon"] else FAIL, "has a favicon",
                   d["favicon"] or "no <link rel=icon> — the tab shows a blank page icon")
            record(PASS if d["title"].strip() else FAIL, "has a title", d["title"][:60])
            if d["textLen"] < 200:
                record(WARN, "the page has content", f"only {d['textLen']} characters of visible text — is it seeded?")
            else:
                record(PASS, "the page has content", f"{d['textLen']} characters")

            # The bug that shipped: one section lost its centring and its
            # headline ran to the viewport edge while everything else stayed on
            # the column. Judged on where the TEXT starts, because a full-bleed
            # header or footer spans from 0 by design and comparing boxes marks
            # every such page as broken — it did exactly that on its first run,
            # naming the correctly-built sections as the strays.
            edges = [(b["textLeft"], f"{b['tag']}.{b['cls']}")
                     for b in d["blocks"] if b.get("textLeft") is not None]
            if len(edges) < 3:
                record(PASS, "text lines up on a column", "too few blocks to judge")
            else:
                tally = {}
                for e, _ in edges:
                    tally.setdefault(e, []).append(_)
                column = max(tally, key=lambda k: len(tally[k]))
                # A deliberate offset is small — an indented pull-quote, a hanging
                # bullet. A container that lost `margin: auto` is off by the whole
                # gutter, so the tolerance sits well below a gutter and well above
                # a nudge.
                strays = sorted({(e, n) for e, n in edges if abs(e - column) > 24})
                if strays:
                    record(FAIL, "text lines up on a column",
                           f"most text starts at {column}px; these do not: " +
                           "; ".join(f"{e}px {n}" for e, n in strays[:4]))
                else:
                    record(PASS, "text lines up on a column", f"{column}px")

            # Every internal link must resolve AND land on a page.
            #
            # Resolving is not enough, and a real site proved it: a "See all"
            # link in the footer pointed at /api/pieces, which answers 200 with
            # {"pieces":[]}. Status-only checking passed it, and a visitor
            # clicking it got raw JSON in their browser. A link in a page is a
            # promise of a page — an endpoint, a feed or a file behind one is a
            # bug whatever it returns.
            broken, not_pages = [], []
            for href in sorted(set(d["links"]))[:25]:
                st, _, hdrs = fetch(base + href)
                if st >= 400:
                    broken.append(f"{href} → {st}")
                    continue
                ctype = (hdrs.get("Content-Type") or hdrs.get("content-type") or "").split(";")[0].strip()
                if ctype and not ctype.startswith("text/html"):
                    not_pages.append(f"{href} → {ctype}")
            record(FAIL if broken else PASS, "internal links resolve",
                   "; ".join(broken) if broken else f"{len(set(d['links']))} checked")
            if not_pages:
                record(FAIL, "every link leads to a page",
                       "these serve a file, not a page: " + "; ".join(not_pages[:4]))
            else:
                record(PASS, "every link leads to a page")

        print("\nscreenshots:")
        for label, g in geo.items():
            print(f"  {label:8} {g['screenshot']}")
        print("\n  OPEN THEM. Passing every check above and still looking wrong is entirely possible.")

    failed = [r for r in results if r[0] == FAIL]
    warned = [r for r in results if r[0] == WARN]
    print("-" * 60)
    print(f"{len(results) - len(failed) - len(warned)} passed, {len(failed)} failed, {len(warned)} warnings")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
