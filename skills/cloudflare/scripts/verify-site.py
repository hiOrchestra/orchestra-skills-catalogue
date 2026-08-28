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



# ── the palette a page is actually painted in ───────────────────────────────
def _rgb(css):
    m = re.match(r"rgba?\(([^)]+)\)", (css or "").strip())
    if not m:
        return None
    parts = [q.strip() for q in m.group(1).replace("/", ",").split(",")]
    try:
        r, g, b = (int(float(q)) for q in parts[:3])
    except ValueError:
        return None
    if len(parts) > 3:
        try:
            if float(parts[3]) < 0.5:
                return None      # too transparent to count as paint
        except ValueError:
            pass
    return r, g, b


def _hsl(rgb):
    import colorsys
    r, g, b = (c / 255 for c in rgb)
    h, lum, sat = colorsys.rgb_to_hls(r, g, b)
    return h * 360, sat, lum


def default_palette_tells(ground, palette):
    """Is this the palette every generated site arrives at?

    Not a style opinion — a repetition detector. The same cream ground and the
    same terracotta accent came out of this stack for a carpentry studio and a
    municipal swimming pool on one night, declared as #f5f1e8 / #ff6b4a both
    times. A palette that does not change when the subject changes was not
    chosen for the subject.

    Deliberately narrow: it names the two clusters we have actually watched
    appear, and stays quiet about everything else rather than refereeing taste.
    """
    tells = []
    g = _rgb(ground)
    if g:
        r, gr, b = g
        # warm off-white: bright, and measurably warmer than it is blue
        if r > 238 and gr > 232 and b > 215 and 6 <= r - b <= 30:
            tells.append(f"a warm cream ground ({ground})")
        # The other cluster's ground: near-black, near-neutral. Paired with one
        # loud accent it is the second look this stack reaches for unprompted.
        elif max(r, gr, b) < 34 and max(r, gr, b) - min(r, gr, b) < 14:
            tells.append(f"a near-black ground ({ground})")
    for entry in palette or []:
        c = _rgb(entry.get("color"))
        if not c:
            continue
        h, sat, lum = _hsl(c)
        if 4 <= h <= 26 and sat >= 0.5 and 0.42 <= lum <= 0.70:
            tells.append(f"a terracotta/coral accent ({entry['color']})")
            break
    for entry in palette or []:
        c = _rgb(entry.get("color"))
        if not c:
            continue
        h, sat, lum = _hsl(c)
        if 80 <= h <= 165 and sat >= 0.45 and 0.40 <= lum <= 0.62:
            tells.append(f"an acid-green accent ({entry['color']})")
            break
    return tells



# ── things that are wrong without being broken ──────────────────────────────
# Faces that ship with one operating system and nowhere else. A stack that
# leads with one of these, and ships no @font-face, is a different design on
# every platform: the author sees their choice, everyone else sees the
# fallback. Found on a live site whose whole identity was Iowan Old Style —
# a macOS-only face — silently rendering as Georgia for most of its readers.
PLATFORM_ONLY_FACES = {
    "iowan old style", "baskerville", "hoefler text", "palatino", "avenir",
    "avenir next", "optima", "gill sans", "futura", "didot", "athelas",
    "charter", "seravek", "skia", "chalkboard", "american typewriter",
    "sf pro", "sf pro text", "sf pro display", "-apple-system",
    "segoe ui", "calibri", "cambria", "constantia", "corbel", "candara",
}

# UI words a site in another language should not be showing its readers.
ENGLISH_UI = [
    "min read", "read more", "read time", "posted on", "published on",
    "continue reading", "search", "home", "next page", "previous page",
    "comments", "leave a comment", "submit", "loading", "subscribe",
]


def first_family(stack):
    return (stack or "").split(",")[0].strip().strip("\"'").lower()


def us_dates(text):
    """M/D/YYYY, which is ambiguous everywhere it is not the local habit."""
    return re.findall(r"\b(?:0?[1-9]|1[0-2])/(?:0?[1-9]|[12]\d|3[01])/(?:19|20)\d\d\b", text)


def duplicated_title(title):
    """`Civis et Homo · Civis et Homo` — a template joining two fields that
    hold the same value."""
    parts = [p.strip() for p in re.split(r"[·|—–\-]", title or "") if p.strip()]
    seen, dupes = set(), []
    for p in parts:
        k = p.lower()
        if k in seen and len(k) > 3:
            dupes.append(p)
        seen.add(k)
    return dupes


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
        # One viewport can come back without measurements — the render timed out,
        # the page never settled, the tab died. That used to be a KeyError on the
        # first geometry read, which killed the whole run and threw away every
        # check that had already passed. A failed measurement is a thing to
        # report, not a reason to stop verifying.
        for label in [k for k, g in geo.items() if "scrollWidth" not in g]:
            record(WARN, f"could not measure the page ({label})",
                   geo[label].get("error") or "the render returned no geometry — rerun, or check the browser on :18800")
        geo = {k: g for k, g in geo.items() if "scrollWidth" in g}
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

            # ── nothing may sit on top of anything else ─────────────────
            ov = d.get("overlaps") or []
            if ov:
                record(FAIL, "nothing overlaps",
                       "; ".join(f"{o['a']} over {o['b']} by {o['x']}x{o['y']}px" for o in ov[:3]))
            else:
                record(PASS, "nothing overlaps")

            # ── the type has to exist on the reader's machine ───────────
            stack, faces = d.get("bodyFont", ""), d.get("fontFaces", 0)
            lead = first_family(stack)
            if faces == 0 and lead in PLATFORM_ONLY_FACES:
                record(FAIL, "the typeface reaches the reader",
                       f"'{lead}' ships with one operating system and the page loads no webfont — "
                       f"everyone else falls back through {stack}")
            elif faces == 0:
                record(WARN, "the typeface reaches the reader",
                       f"no webfont is loaded; the design depends on {stack} already being installed")
            else:
                record(PASS, "the typeface reaches the reader", f"{faces} face(s) shipped")

            # ── the interface speaks the site's language ────────────────
            lang = (d.get("lang") or "").lower()
            if lang and not lang.startswith("en"):
                text = re.sub(r"<[^>]+>", " ", body)
                found = [w for w in ENGLISH_UI if re.search(r"\b" + re.escape(w) + r"\b", text, re.I)]
                dates = us_dates(text)
                bad = []
                if found:
                    bad.append("English interface text: " + ", ".join(repr(w) for w in found[:4]))
                if dates:
                    bad.append(f"{len(dates)} US-format date(s) like {dates[0]}")
                if bad:
                    record(FAIL, f"the interface speaks {lang}", "; ".join(bad))
                else:
                    record(PASS, f"the interface speaks {lang}")

            # ── a title that says it twice ──────────────────────────────
            dup = duplicated_title(d.get("title") or "")
            if dup:
                record(FAIL, "the title says each thing once",
                       f"repeats {dup[0]!r} — {d.get('title')!r}")
            else:
                record(PASS, "the title says each thing once")

            # ── markup that became words ────────────────────────────────
            # The escaping check above tests one payload against the SOURCE.
            # This asks the browser what a reader actually sees, which is a
            # different question and the one that caught a real bug: a favicon
            # data: URI carrying raw <svg …> inside its href closed the <link>
            # early, and a stray glyph plus `">` rendered on every page of the
            # site. Status was 200, the title existed, a <link rel=icon> existed
            # — every structural check passed.
            stray = d.get("strayMarkup") or []
            if stray:
                record(FAIL, "no markup showing as text",
                       "these appear in the visible text of the page: "
                       + ", ".join(repr(x) for x in stray[:5])
                       + " — something is escaping its attribute or being double-encoded")
            else:
                record(PASS, "no markup showing as text")

            # ── is this the palette every generated site lands on? ──────
            tells = default_palette_tells(d.get("ground"), d.get("palette"))
            if len(tells) >= 2:
                record(WARN, "the palette was chosen for this subject",
                       "this is the look that arrives by default — " + " and ".join(tells)
                       + ". It has come out of this stack for unrelated businesses. "
                         "If it was not derived from what this site is about, change it.")
            else:
                record(PASS, "the palette was chosen for this subject")

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
