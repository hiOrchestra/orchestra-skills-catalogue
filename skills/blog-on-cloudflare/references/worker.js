/**
 * A blog on one Cloudflare Worker, backed by one D1 database.
 *
 * Deployed with `scripts/deploy.py`, which PUTs this file to the Workers API
 * with a D1 binding named DB. Read `references/deploying.md` before changing
 * how it is deployed; read `references/schema.sql` for the tables.
 *
 * WHAT IS DELIBERATE HERE
 *
 * - Scheduling has no cron. A scheduled post is a `live` row whose
 *   published_at is in the future, and every public read filters
 *   `published_at <= now`. One mechanism, nothing to break at 3am.
 * - Comments arrive `pending` and are invisible until approved. A blog that
 *   publishes whatever a stranger types is a blog that will publish spam.
 * - Reactions are constrained by the DATABASE (UNIQUE post_id+visitor_id), not
 *   by the cookie. The cookie identifies a returning visitor; it does not
 *   enforce anything, because a cookie is client-side and therefore a wish.
 * - Every string that came from a visitor is escaped at render. There is one
 *   escape function and everything goes through it.
 * - The admin API is bearer-token only and is the ONLY way to write posts. The
 *   agent uses it; the public routes cannot reach it.
 */

const enc = new TextEncoder();

// ── escaping ────────────────────────────────────────────────────────────────
// One function, used for every untrusted value that reaches HTML. If you add a
// second one you will eventually use the wrong one.
const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ESC[c]);
const attr = (v) => esc(v);

// ── tiny markdown ───────────────────────────────────────────────────────────
// Headings, bold, italic, links, images, quotes, lists, rules, paragraphs.
//
// Structure is detected on the RAW line and escaping happens when the text is
// emitted — not the other way round. Escaping first turns `>` into `&gt;`, so
// the blockquote rule silently stops matching and every quote in every post
// renders as a literal "&gt;". Order matters here.
function markdown(src) {
  const lines = String(src ?? '').replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let para = [], list = null;
  const flushPara = () => { if (para.length) { out.push(`<p>${inline(para.join(' '))}</p>`); para = []; } };
  const flushList = () => { if (list) { out.push(`</${list}>`); list = null; } };

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (!line.trim()) { flushPara(); flushList(); continue; }

    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) { flushPara(); flushList(); const n = h[1].length + 1; out.push(`<h${n}>${inline(h[2])}</h${n}>`); continue; }

    const img = line.match(/^!\[(.*?)\]\((\S+?)\)$/);
    if (img) {
      flushPara(); flushList();
      out.push(`<figure><img src="${attr(img[2])}" alt="${attr(img[1])}" loading="lazy">`
             + (img[1] ? `<figcaption>${inline(img[1])}</figcaption>` : '') + `</figure>`);
      continue;
    }

    if (/^>\s?/.test(line)) { flushPara(); flushList(); out.push(`<blockquote>${inline(line.replace(/^>\s?/, ''))}</blockquote>`); continue; }

    const li = line.match(/^\s*([-*]|\d+\.)\s+(.*)$/);
    if (li) {
      flushPara();
      const want = /^\d/.test(li[1]) ? 'ol' : 'ul';
      if (list !== want) { flushList(); out.push(`<${want}>`); list = want; }
      out.push(`<li>${inline(li[2])}</li>`);
      continue;
    }

    if (/^(-{3,}|\*{3,})$/.test(line)) { flushPara(); flushList(); out.push('<hr>'); continue; }
    para.push(line.trim());
  }
  flushPara(); flushList();
  return out.join('\n');
}

/** Inline spans. Escapes FIRST within the fragment, then introduces markup, so
 *  a post can never inject HTML even though its author is trusted. */
function inline(s) {
  return esc(s)
    .replace(/!\[(.*?)\]\((\S+?)\)/g, (_, a, u) => `<img src="${attr(u)}" alt="${attr(a)}" loading="lazy">`)
    // Only http(s) and root-relative links survive; javascript: and data: do not.
    .replace(/\[(.*?)\]\((\S+?)\)/g, (m, tx, u) => (/^(https?:\/\/|\/)/i.test(u) ? `<a href="${attr(u)}">${tx}</a>` : tx))
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|\W)\*(?!\s)(.+?)(?<!\s)\*(?=\W|$)/g, '$1<em>$2</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>');
}

// ── helpers ─────────────────────────────────────────────────────────────────
const json = (data, status = 200, extra = {}) =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json;charset=UTF-8', ...extra } });
const html = (body, status = 200, extra = {}) =>
  new Response(body, { status, headers: { 'content-type': 'text/html;charset=UTF-8', ...extra } });
const nowIso = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
const today = () => new Date().toISOString().slice(0, 10);

// ── words ───────────────────────────────────────────────────────────────────
// Every visitor-facing string, in English, overridable per blog. A blog in
// Catalan, German or Portuguese is a settings change, not a fork of this file:
// the agent writes `ui_<key>` into `settings` once and the site speaks that
// language from the next request onward.
const UI = {
  no_posts:        'No posts yet.',
  not_found_title: 'Not found',
  not_found_body:  'This page does not exist.',
  no_comments:     'No comments yet.',
  preview_banner:  'Preview — status {status}. This page is not public.',
  like:            'Like',
  dislike:         'Dislike',
  comments:        'Comments',
  name_ph:         'Your name',
  email_ph:        'Email (not published)',
  comment_ph:      'Your comment',
  submit:          'Send',
  note_review:     'Comments are reviewed before they appear.',
  note_open:       'Your comment will appear straight away.',
  thanks_review:   'Thank you — it will appear once reviewed.',
  thanks_open:     'Thank you for your comment.',
  send_failed:     'Could not send.',
  rate_limited:    'Too many requests.',
  too_many:        'Too many comments today.',
  bad_reaction:    'Invalid reaction.',
  bad_name:        'Invalid name.',
  bad_comment:     'Invalid comment.',
  bad_email:       'Invalid email.',
  post_not_found:  'Article not found.',
  comments_closed: 'Comments are closed.',
};
/** A visitor-facing string: `ui_<key>` from settings, else the English default. */
const t = (cfg, key, vars) => {
  let out = (cfg && cfg[`ui_${key}`]) || UI[key] || key;
  if (vars) for (const [k, v] of Object.entries(vars)) out = out.replaceAll(`{${k}}`, v);
  return out;
};

async function settings(env) {
  const r = await env.DB.prepare('SELECT key, value FROM settings').all();
  const s = Object.fromEntries((r.results || []).map((x) => [x.key, x.value]));
  return {
    title: s.title || 'Blog',
    tagline: s.tagline || '',
    author: s.author || '',
    locale: s.locale || 'en',
    accent: s.accent || '#1f3b2c',
    footer: s.footer || '',
    ...s,
  };
}

function visitorId(request) {
  const c = request.headers.get('cookie') || '';
  const m = c.match(/(?:^|;\s*)vid=([A-Za-z0-9_-]{8,64})/);
  return m ? m[1] : null;
}
const newVisitorId = () => crypto.randomUUID().replace(/-/g, '');

/** Fixed-window limiter in D1. Cheap, and honest about what it is: a ceiling on
 *  abuse, not a security control. */
async function rateLimit(env, key, limit, windowSec) {
  const now = Math.floor(Date.now() / 1000);
  const reset = now + windowSec;
  await env.DB.prepare(
    `INSERT INTO rate_limits (bucket, count, reset_at) VALUES (?1, 1, ?2)
     ON CONFLICT(bucket) DO UPDATE SET
       count = CASE WHEN rate_limits.reset_at < ?3 THEN 1 ELSE rate_limits.count + 1 END,
       reset_at = CASE WHEN rate_limits.reset_at < ?3 THEN ?2 ELSE rate_limits.reset_at END`,
  ).bind(key, reset, now).run();
  const row = await env.DB.prepare('SELECT count FROM rate_limits WHERE bucket = ?1').bind(key).first();
  return (row?.count ?? 0) <= limit;
}

const authorized = (request, env) => {
  const h = request.headers.get('authorization') || '';
  const token = h.startsWith('Bearer ') ? h.slice(7) : '';
  // Constant-time-ish: compare full length, never short-circuit on first byte.
  if (!env.ADMIN_TOKEN || token.length !== env.ADMIN_TOKEN.length) return false;
  let diff = 0;
  const a = enc.encode(token), b = enc.encode(env.ADMIN_TOKEN);
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
};

// ── layout ──────────────────────────────────────────────────────────────────
// Editorial defaults: one serif, a generous measure, no cards, no shadows.
// The agent restyles this — `settings.accent` and the CSS below are the dials.
const layout = (s, { title, description, image, canonical, body, noindex }) => `<!doctype html>
<html lang="${attr(s.locale)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title>
${description ? `<meta name="description" content="${attr(description)}">` : ''}
${noindex ? '<meta name="robots" content="noindex">' : ''}
${canonical ? `<link rel="canonical" href="${attr(canonical)}">` : ''}
<meta property="og:title" content="${attr(title)}">
${description ? `<meta property="og:description" content="${attr(description)}">` : ''}
${image ? `<meta property="og:image" content="${attr(image)}">` : ''}
<link rel="alternate" type="application/rss+xml" href="/rss.xml" title="${attr(s.title)}">
<style>
:root{--accent:${attr(s.accent)};--ink:#1a1a18;--ink-2:#4a4a45;--ink-3:#767670;--paper:#fbfaf7;--edge:#e4e1d9}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:1.05rem/1.7 Georgia,'Iowan Old Style','Times New Roman',serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:41rem;margin:0 auto;padding:0 1.25rem}
header.site{border-bottom:1px solid var(--edge);margin-bottom:3rem}
header.site .wrap{padding-top:2.5rem;padding-bottom:1.75rem}
header.site a.home{color:var(--accent);text-decoration:none;font-size:1.5rem;letter-spacing:-.01em}
header.site p{margin:.4rem 0 0;color:var(--ink-3);font-size:.92rem;font-style:italic}
nav.sections{margin-top:1rem;display:flex;flex-wrap:wrap;gap:1rem}
nav.sections a{color:var(--ink-2);text-decoration:none;font-size:.82rem;text-transform:uppercase;letter-spacing:.09em}
nav.sections a:hover{color:var(--accent)}
article h1{font-size:2.1rem;line-height:1.2;letter-spacing:-.02em;margin:0 0 .4rem}
article .sub{color:var(--ink-2);font-size:1.15rem;font-style:italic;margin:0 0 1rem}
article .meta{color:var(--ink-3);font-size:.82rem;text-transform:uppercase;letter-spacing:.08em;margin-bottom:2rem}
article img{max-width:100%;height:auto;display:block}
article figure{margin:2rem 0}
article figcaption{color:var(--ink-3);font-size:.84rem;margin-top:.5rem;font-style:italic}
article blockquote{margin:1.8rem 0;padding-left:1.2rem;border-left:2px solid var(--accent);color:var(--ink-2);font-style:italic}
article h2{font-size:1.4rem;margin:2.4rem 0 .6rem;letter-spacing:-.01em}
article h3{font-size:1.15rem;margin:2rem 0 .5rem}
article a{color:var(--accent)}
.index{list-style:none;padding:0;margin:0}
.index li{padding:1.6rem 0;border-bottom:1px solid var(--edge)}
.index h2{font-size:1.35rem;margin:0 0 .3rem;letter-spacing:-.01em}
.index h2 a{color:var(--ink);text-decoration:none}
.index h2 a:hover{color:var(--accent)}
.index p{margin:.3rem 0 0;color:var(--ink-2);font-size:.97rem}
.index .meta{color:var(--ink-3);font-size:.78rem;text-transform:uppercase;letter-spacing:.08em}
.reactions{display:flex;gap:.6rem;align-items:center;margin:3rem 0 1rem}
.reactions button{font:inherit;font-size:.9rem;padding:.5rem 1rem;border:1px solid var(--edge);
  background:#fff;border-radius:2rem;cursor:pointer;color:var(--ink-2)}
.reactions button[aria-pressed=true]{border-color:var(--accent);color:var(--accent)}
.reactions button:disabled{opacity:.55;cursor:default}
.comments{border-top:1px solid var(--edge);margin-top:2.5rem;padding-top:2rem}
.comments h2{font-size:1.05rem;text-transform:uppercase;letter-spacing:.09em;color:var(--ink-3);font-weight:400}
.comment{padding:1.1rem 0;border-bottom:1px solid var(--edge)}
.comment .who{font-size:.86rem;color:var(--ink-3)}
.comment p{margin:.35rem 0 0;white-space:pre-wrap}
form.comment-form{margin-top:1.5rem;display:grid;gap:.7rem}
form.comment-form input,form.comment-form textarea{font:inherit;padding:.7rem .8rem;border:1px solid var(--edge);
  background:#fff;border-radius:3px;width:100%}
form.comment-form textarea{min-height:7rem;resize:vertical}
form.comment-form button{font:inherit;justify-self:start;padding:.6rem 1.3rem;border:0;border-radius:3px;
  background:var(--accent);color:#fff;cursor:pointer}
.note{font-size:.86rem;color:var(--ink-3)}
.banner{background:#fff6e5;border:1px solid #e8d5a8;padding:.7rem 1rem;border-radius:3px;font-size:.88rem;margin-bottom:2rem}
footer.site{border-top:1px solid var(--edge);margin-top:4rem;padding:2rem 0 3rem;color:var(--ink-3);font-size:.85rem}
@media(prefers-color-scheme:dark){
  :root{--ink:#e8e6e1;--ink-2:#b4b1a9;--ink-3:#8a877f;--paper:#161614;--edge:#2e2d29}
  form.comment-form input,form.comment-form textarea,.reactions button{background:#1f1e1b;color:var(--ink)}
  .banner{background:#2a2415;border-color:#4a3f22}
}
</style>
</head>
<body>
<header class="site"><div class="wrap">
  <a class="home" href="/">${esc(s.title)}</a>
  ${s.tagline ? `<p>${esc(s.tagline)}</p>` : ''}
</div></header>
<main class="wrap">${body}</main>
<footer class="site"><div class="wrap">${esc(s.footer || s.title)} · <a href="/rss.xml">RSS</a></div></footer>
</body></html>`;

// ── public pages ────────────────────────────────────────────────────────────
async function homepage(env, url) {
  const s = await settings(env);
  const section = url.searchParams.get('section');
  const rows = await env.DB.prepare(
    `SELECT slug, title, subtitle, excerpt, section, published_at FROM posts
      WHERE status = 'live' AND published_at IS NOT NULL AND published_at <= ?1
        ${section ? 'AND section = ?2' : ''}
      ORDER BY published_at DESC LIMIT 60`,
  ).bind(...(section ? [nowIso(), section] : [nowIso()])).all();

  const items = (rows.results || []).map((p) => `
    <li>
      <div class="meta">${esc((p.published_at || '').slice(0, 10))}${p.section ? ` · ${esc(p.section)}` : ''}</div>
      <h2><a href="/post/${attr(p.slug)}">${esc(p.title)}</a></h2>
      ${p.subtitle ? `<p>${esc(p.subtitle)}</p>` : p.excerpt ? `<p>${esc(p.excerpt)}</p>` : ''}
    </li>`).join('');

  return html(layout(s, {
    title: s.title,
    description: s.tagline,
    canonical: url.origin + '/',
    body: items ? `<ul class="index">${items}</ul>` : `<p class="note">${esc(t(s, 'no_posts'))}</p>`,
  }));
}

async function postPage(env, url, slug, { preview = false } = {}) {
  const s = await settings(env);
  const post = preview
    ? await env.DB.prepare(`SELECT * FROM posts WHERE slug = ?1`).bind(slug).first()
    : await env.DB.prepare(
        `SELECT * FROM posts WHERE slug = ?1 AND status = 'live'
           AND published_at IS NOT NULL AND published_at <= ?2`,
      ).bind(slug, nowIso()).first();
  if (!post) return html(layout(s, { title: t(s, 'not_found_title'), body: `<p class="note">${esc(t(s, 'not_found_body'))}</p>` }), 404);

  const [reactions, comments] = await Promise.all([
    env.DB.prepare(`SELECT reaction, COUNT(*) n FROM post_reactions WHERE post_id = ?1 GROUP BY reaction`).bind(post.id).all(),
    env.DB.prepare(`SELECT author, body, created_at FROM comments WHERE post_id = ?1 AND status = 'approved' ORDER BY created_at`).bind(post.id).all(),
  ]);
  const count = Object.fromEntries((reactions.results || []).map((r) => [r.reaction, r.n]));

  const commentHtml = (comments.results || []).map((c) => `
    <div class="comment">
      <div class="who">${esc(c.author)} · ${esc((c.created_at || '').slice(0, 10))}</div>
      <p>${esc(c.body)}</p>
    </div>`).join('') || `<p class="note">${esc(t(s, 'no_comments'))}</p>`;

  const body = `
${preview ? `<div class="banner">${esc(t(s, 'preview_banner', { status: post.status }))}</div>` : ''}
<article>
  <h1>${esc(post.title)}</h1>
  ${post.subtitle ? `<p class="sub">${esc(post.subtitle)}</p>` : ''}
  <div class="meta">${esc((post.published_at || '').slice(0, 10))}${post.section ? ` · ${esc(post.section)}` : ''}${post.author ? ` · ${esc(post.author)}` : ''}</div>
  ${post.hero_image ? `<figure><img src="${attr(post.hero_image)}" alt="${attr(post.hero_alt)}"></figure>` : ''}
  ${markdown(post.content)}
</article>

<div class="reactions" data-post="${post.id}"${s.reactions_enabled === 'false' ? ' hidden' : ''}>
  <button data-r="like" aria-pressed="false">${esc(t(s, 'like'))} <span>${count.like || 0}</span></button>
  <button data-r="dislike" aria-pressed="false">${esc(t(s, 'dislike'))} <span>${count.dislike || 0}</span></button>
</div>

<section class="comments"${s.comments_mode === 'closed' ? ' hidden' : ''}>
  <h2>${esc(t(s, 'comments'))}</h2>
  ${commentHtml}
  <form class="comment-form" data-post="${post.id}">
    <input name="author" maxlength="80" required placeholder="${attr(t(s, 'name_ph'))}">
    <input name="email" type="email" maxlength="160" placeholder="${attr(t(s, 'email_ph'))}">
    <textarea name="body" maxlength="4000" required placeholder="${attr(t(s, 'comment_ph'))}"></textarea>
    <button type="submit">${esc(t(s, 'submit'))}</button>
    <p class="note">${s.comments_mode === 'review'
      ? esc(t(s, 'note_review'))
      : esc(t(s, 'note_open'))}</p>
  </form>
</section>

<script>
(() => {
  // Injected server-side so the client speaks whatever language the
  // blog is configured in, without shipping a dictionary to the browser.
  const W = ${JSON.stringify({ thanks_review: t(s, 'thanks_review'), thanks_open: t(s, 'thanks_open'), send_failed: t(s, 'send_failed') })};
  const rx = document.querySelector('.reactions');
  if (rx) rx.addEventListener('click', async (e) => {
    const b = e.target.closest('button[data-r]'); if (!b) return;
    rx.querySelectorAll('button').forEach(x => x.disabled = true);
    try {
      const r = await fetch('/api/posts/' + rx.dataset.post + '/reactions', {
        method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ reaction: b.dataset.r })
      });
      const d = await r.json();
      if (d.counts) {
        rx.querySelector('[data-r=like] span').textContent = d.counts.like || 0;
        rx.querySelector('[data-r=dislike] span').textContent = d.counts.dislike || 0;
        rx.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.r === d.yours)));
      }
    } finally { rx.querySelectorAll('button').forEach(x => x.disabled = false); }
  });
  const f = document.querySelector('form.comment-form');
  if (f) f.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = f.querySelector('button'); btn.disabled = true;
    const r = await fetch('/api/posts/' + f.dataset.post + '/comments', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(f)))
    });
    const d = await r.json();
    const note = f.querySelector('.note');
    note.textContent = d.ok
      ? (d.pending ? W.thanks_review : W.thanks_open)
      : (d.error || W.send_failed);
    if (d.ok && !d.pending) setTimeout(() => location.reload(), 900);
    if (d.ok) f.reset();
    btn.disabled = false;
  });
})();
</script>`;

  const res = html(layout(s, {
    title: `${post.title} · ${s.title}`,
    description: post.subtitle || post.excerpt,
    image: post.hero_image,
    canonical: preview ? null : `${url.origin}/post/${post.slug}`,
    noindex: preview,
    body,
  }));
  if (!preview) {
    await env.DB.prepare(
      `INSERT INTO post_views (post_id, day, views) VALUES (?1, ?2, 1)
       ON CONFLICT(post_id, day) DO UPDATE SET views = post_views.views + 1`,
    ).bind(post.id, today()).run();
  }
  return res;
}

/**
 * Serve an image from R2, through the Worker.
 *
 * Going through the Worker rather than a public bucket means one hostname, no
 * second DNS record and no CORS, and the blog keeps working if the bucket is
 * later made private. `MEDIA` is an r2_bucket binding; when it is absent the
 * route simply 404s, so a blog with no bucket is not a broken blog.
 *
 * Immutable caching is safe because the agent writes content-addressed keys
 * (`2026/08/slug-a1b2c3.jpg`) — a changed image is a new key, never a new
 * version of an old one.
 */
async function media(env, key, request) {
  if (!env.MEDIA) return new Response('Not found', { status: 404 });
  const object = await env.MEDIA.get(key);
  if (!object) return new Response('Not found', { status: 404 });

  const etag = object.httpEtag;
  if (request.headers.get('if-none-match') === etag) {
    return new Response(null, { status: 304, headers: { etag } });
  }
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('etag', etag);
  headers.set('cache-control', 'public, max-age=31536000, immutable');
  return new Response(object.body, { headers });
}

async function rss(env, url) {
  const s = await settings(env);
  const rows = await env.DB.prepare(
    `SELECT slug, title, subtitle, excerpt, published_at FROM posts
      WHERE status='live' AND published_at IS NOT NULL AND published_at <= ?1
      ORDER BY published_at DESC LIMIT 40`,
  ).bind(nowIso()).all();
  const items = (rows.results || []).map((p) => `<item>
  <title>${esc(p.title)}</title>
  <link>${attr(url.origin)}/post/${attr(p.slug)}</link>
  <guid>${attr(url.origin)}/post/${attr(p.slug)}</guid>
  <pubDate>${new Date((p.published_at || '').replace(' ', 'T') + 'Z').toUTCString()}</pubDate>
  <description>${esc(p.subtitle || p.excerpt)}</description>
</item>`).join('\n');
  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>
<title>${esc(s.title)}</title><link>${attr(url.origin)}</link><description>${esc(s.tagline)}</description>
${items}</channel></rss>`,
    { headers: { 'content-type': 'application/rss+xml;charset=UTF-8' } });
}

async function sitemap(env, url) {
  const rows = await env.DB.prepare(
    `SELECT slug, updated_at FROM posts WHERE status='live' AND published_at IS NOT NULL AND published_at <= ?1`,
  ).bind(nowIso()).all();
  const urls = [`<url><loc>${attr(url.origin)}/</loc></url>`]
    .concat((rows.results || []).map((p) => `<url><loc>${attr(url.origin)}/post/${attr(p.slug)}</loc><lastmod>${attr((p.updated_at || '').slice(0, 10))}</lastmod></url>`));
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.join('')}</urlset>`,
    { headers: { 'content-type': 'application/xml;charset=UTF-8' } });
}

// ── public write endpoints ──────────────────────────────────────────────────
async function react(request, env, postId) {
  const ip = request.headers.get('cf-connecting-ip') || '0';
  if (!await rateLimit(env, `react:${ip}:${today()}`, 200, 86400)) return json({ error: t(await settings(env), 'rate_limited') }, 429);
  const { reaction } = await request.json().catch(() => ({}));
  if (reaction !== 'like' && reaction !== 'dislike') return json({ error: t(await settings(env), 'bad_reaction') }, 400);

  let vid = visitorId(request), setCookie = null;
  if (!vid) {
    vid = newVisitorId();
    setCookie = `vid=${vid}; Path=/; Max-Age=63072000; HttpOnly; Secure; SameSite=Lax`;
  }
  // Second press of the same button removes it; the other button switches.
  const existing = await env.DB.prepare(`SELECT reaction FROM post_reactions WHERE post_id=?1 AND visitor_id=?2`).bind(postId, vid).first();
  if (existing?.reaction === reaction) {
    await env.DB.prepare(`DELETE FROM post_reactions WHERE post_id=?1 AND visitor_id=?2`).bind(postId, vid).run();
  } else {
    await env.DB.prepare(
      `INSERT INTO post_reactions (post_id, visitor_id, reaction) VALUES (?1,?2,?3)
       ON CONFLICT(post_id, visitor_id) DO UPDATE SET reaction = ?3`,
    ).bind(postId, vid, reaction).run();
  }
  const rows = await env.DB.prepare(`SELECT reaction, COUNT(*) n FROM post_reactions WHERE post_id=?1 GROUP BY reaction`).bind(postId).all();
  const counts = Object.fromEntries((rows.results || []).map((r) => [r.reaction, r.n]));
  const mine = await env.DB.prepare(`SELECT reaction FROM post_reactions WHERE post_id=?1 AND visitor_id=?2`).bind(postId, vid).first();
  return json({ ok: true, counts, yours: mine?.reaction || null }, 200, setCookie ? { 'set-cookie': setCookie } : {});
}

async function comment(request, env, postId) {
  const ip = request.headers.get('cf-connecting-ip') || '0';
  if (!await rateLimit(env, `comment:${ip}:${today()}`, 20, 86400)) return json({ error: t(await settings(env), 'too_many') }, 429);
  const b = await request.json().catch(() => ({}));
  const author = String(b.author || '').trim(), body = String(b.body || '').trim();
  const email = String(b.email || '').trim();
  if (author.length < 2 || author.length > 80) return json({ error: t(await settings(env), 'bad_name') }, 400);
  if (body.length < 2 || body.length > 4000) return json({ error: t(await settings(env), 'bad_comment') }, 400);
  if (email && (email.length > 160 || !/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email))) return json({ error: t(await settings(env), 'bad_email') }, 400);
  const post = await env.DB.prepare(`SELECT id FROM posts WHERE id=?1 AND status='live'`).bind(postId).first();
  if (!post) return json({ error: t(await settings(env), 'post_not_found') }, 404);

  // `comments_mode` decides whether a comment is live on submit. Default is
  // open: on a blog this size a moderation queue means nobody ever sees their
  // comment appear, and the conversation dies. The agent sweeps for spam on a
  // schedule; the owner can switch this to `review` by asking.
  const cfg = await settings(env);
  if (cfg.comments_mode === 'closed') return json({ error: t(cfg, 'comments_closed') }, 403);
  const status = cfg.comments_mode === 'review' ? 'pending' : 'approved';

  await env.DB.prepare(
    `INSERT INTO comments (post_id, author, email, body, visitor_id, status) VALUES (?1,?2,?3,?4,?5,?6)`,
  ).bind(postId, author, email, body, visitorId(request) || '', status).run();
  return json({ ok: true, pending: status === 'pending' });
}

// ── admin API (bearer token; the agent's only write path) ───────────────────
async function admin(request, env, url) {
  if (!authorized(request, env)) return json({ error: 'unauthorized' }, 401);
  const parts = url.pathname.replace(/^\/api\/admin\/?/, '').split('/').filter(Boolean);
  const [resource, id, action] = parts;

  if (resource === 'posts' && request.method === 'GET' && !id) {
    const r = await env.DB.prepare(
      `SELECT id, slug, title, section, status, published_at, updated_at FROM posts ORDER BY COALESCE(published_at, created_at) DESC`).all();
    return json({ posts: r.results || [] });
  }
  if (resource === 'posts' && request.method === 'POST' && !id) {
    const p = await request.json();
    if (!p.slug || !p.title || !p.content) return json({ error: 'slug, title and content are required' }, 400);
    // Upsert on slug so an interrupted migration can simply be re-run.
    await env.DB.prepare(
      `INSERT INTO posts (slug,title,subtitle,excerpt,content,hero_image,hero_alt,section,author,status,published_at,source_url,updated_at)
       VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,datetime('now'))
       ON CONFLICT(slug) DO UPDATE SET title=?2,subtitle=?3,excerpt=?4,content=?5,hero_image=?6,hero_alt=?7,
         section=?8,author=?9,status=?10,published_at=?11,updated_at=datetime('now')`,
    ).bind(p.slug, p.title, p.subtitle || '', p.excerpt || '', p.content, p.hero_image || null, p.hero_alt || '',
      p.section || '', p.author || '', p.status || 'draft', p.published_at || null, p.source_url || null).run();
    const row = await env.DB.prepare(`SELECT id, slug, status, published_at FROM posts WHERE slug=?1`).bind(p.slug).first();
    return json({ ok: true, post: row });
  }
  if (resource === 'posts' && id && request.method === 'PATCH') {
    const p = await request.json();
    const allowed = ['title','subtitle','excerpt','content','hero_image','hero_alt','section','author','status','published_at','slug'];
    const sets = [], vals = [];
    for (const k of allowed) if (k in p) { sets.push(`${k} = ?${sets.length + 1}`); vals.push(p[k]); }
    if (!sets.length) return json({ error: 'nothing to update' }, 400);
    vals.push(id);
    await env.DB.prepare(`UPDATE posts SET ${sets.join(', ')}, updated_at = datetime('now') WHERE id = ?${vals.length}`).bind(...vals).run();
    return json({ ok: true });
  }
  if (resource === 'posts' && id && request.method === 'DELETE') {
    await env.DB.prepare(`DELETE FROM posts WHERE id = ?1`).bind(id).run();
    return json({ ok: true });
  }
  if (resource === 'comments' && request.method === 'GET') {
    const status = url.searchParams.get('status') || 'pending';
    const r = await env.DB.prepare(
      `SELECT c.id, c.post_id, p.slug, c.author, c.email, c.body, c.status, c.created_at
         FROM comments c JOIN posts p ON p.id = c.post_id WHERE c.status = ?1 ORDER BY c.created_at DESC`).bind(status).all();
    return json({ comments: r.results || [] });
  }
  if (resource === 'comments' && id && action && request.method === 'POST') {
    if (!['approve','spam','pending','hide'].includes(action)) return json({ error: 'unknown action' }, 400);
    const map = { approve: 'approved', spam: 'spam', pending: 'pending', hide: 'hidden' };
    // Record WHY, so a judgement can be reviewed rather than only applied.
    const b = await request.json().catch(() => ({}));
    await env.DB.prepare(
      `UPDATE comments SET status = ?1, spam_score = ?2, spam_reason = ?3, reviewed_at = datetime('now') WHERE id = ?4`,
    ).bind(map[action], b.score ?? null, b.reason ?? null, id).run();
    return json({ ok: true });
  }
  // Upload the week's image. Raw bytes in the body; the key comes from the
  // path, so the agent controls naming and can keep it content-addressed.
  if (resource === 'media' && request.method === 'PUT') {
    if (!env.MEDIA) return json({ error: 'No MEDIA bucket bound to this worker' }, 501);
    const key = decodeURIComponent(parts.slice(1).join('/'));
    if (!key || key.includes('..')) return json({ error: 'bad key' }, 400);
    const ct = request.headers.get('content-type') || 'application/octet-stream';
    if (!/^image\//.test(ct)) return json({ error: 'only images' }, 415);
    await env.MEDIA.put(key, request.body, { httpMetadata: { contentType: ct } });
    return json({ ok: true, key, url: `/media/${key}` });
  }
  if (resource === 'media' && request.method === 'GET') {
    if (!env.MEDIA) return json({ objects: [] });
    const listed = await env.MEDIA.list({ limit: 200, prefix: url.searchParams.get('prefix') || undefined });
    return json({ objects: listed.objects.map((o) => ({ key: o.key, size: o.size, uploaded: o.uploaded, url: `/media/${o.key}` })) });
  }
  if (resource === 'media' && id && request.method === 'DELETE') {
    if (!env.MEDIA) return json({ error: 'No MEDIA bucket' }, 501);
    await env.MEDIA.delete(decodeURIComponent(parts.slice(1).join('/')));
    return json({ ok: true });
  }
  if (resource === 'settings' && request.method === 'PUT') {
    const p = await request.json();
    for (const [k, v] of Object.entries(p)) {
      await env.DB.prepare(`INSERT INTO settings (key,value) VALUES (?1,?2) ON CONFLICT(key) DO UPDATE SET value=?2`).bind(k, String(v)).run();
    }
    return json({ ok: true });
  }
  // Everything the Canvas needs, in one call the agent can sync on a cron.
  if (resource === 'stats' && request.method === 'GET') {
    const since = url.searchParams.get('since') || '1970-01-01';
    const [views, totals, pending] = await Promise.all([
      env.DB.prepare(`SELECT p.slug, v.day, v.views FROM post_views v JOIN posts p ON p.id = v.post_id WHERE v.day >= ?1 ORDER BY v.day`).bind(since).all(),
      env.DB.prepare(`SELECT p.slug, p.title, p.status, p.published_at,
          COALESCE((SELECT SUM(views) FROM post_views WHERE post_id=p.id),0) views,
          COALESCE((SELECT COUNT(*) FROM post_reactions WHERE post_id=p.id AND reaction='like'),0) likes,
          COALESCE((SELECT COUNT(*) FROM post_reactions WHERE post_id=p.id AND reaction='dislike'),0) dislikes,
          COALESCE((SELECT COUNT(*) FROM comments WHERE post_id=p.id AND status='approved'),0) comments
        FROM posts p ORDER BY p.published_at DESC`).all(),
      env.DB.prepare(`SELECT COUNT(*) n FROM comments WHERE status='pending'`).first(),
    ]);
    return json({ daily: views.results || [], posts: totals.results || [], pendingComments: pending?.n || 0 });
  }
  return json({ error: 'not found' }, 404);
}

// ── router ──────────────────────────────────────────────────────────────────
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const p = url.pathname;
    try {
      if (p.startsWith('/api/admin')) return await admin(request, env, url);

      if (request.method === 'POST') {
        const react_ = p.match(/^\/api\/posts\/(\d+)\/reactions$/);
        if (react_) return await react(request, env, Number(react_[1]));
        const cm = p.match(/^\/api\/posts\/(\d+)\/comments$/);
        if (cm) return await comment(request, env, Number(cm[1]));
      }

      if (p === '/' ) return await homepage(env, url);
      if (p === '/rss.xml') return await rss(env, url);
      if (p === '/sitemap.xml') return await sitemap(env, url);
      if (p === '/robots.txt') return new Response(`User-agent: *\nAllow: /\nSitemap: ${url.origin}/sitemap.xml\n`, { headers: { 'content-type': 'text/plain' } });

      if (p.startsWith('/media/')) return await media(env, decodeURIComponent(p.slice('/media/'.length)), request);

      const post = p.match(/^\/post\/([A-Za-z0-9-]+)\/?$/);
      if (post) return await postPage(env, url, post[1]);

      // Preview is gated by a shared secret, and every preview page is noindex.
      const prev = p.match(/^\/preview\/([A-Za-z0-9-]+)\/?$/);
      if (prev) {
        if (!env.PREVIEW_TOKEN || url.searchParams.get('token') !== env.PREVIEW_TOKEN) {
          return new Response('Not found', { status: 404 });
        }
        return await postPage(env, url, prev[1], { preview: true });
      }

      if (p === '/api/posts') {
        const r = await env.DB.prepare(
          `SELECT slug,title,subtitle,excerpt,section,published_at FROM posts
            WHERE status='live' AND published_at IS NOT NULL AND published_at <= ?1
            ORDER BY published_at DESC`).bind(nowIso()).all();
        return json({ posts: r.results || [] });
      }

      const s = await settings(env);
      return html(layout(s, { title: `${t(s, 'not_found_title')} · ${s.title}`, noindex: true, body: `<p class="note">${esc(t(s, 'not_found_body'))}</p>` }), 404);
    } catch (err) {
      // Never leak a stack to a visitor; the message still reaches wrangler tail.
      console.error('worker error', p, err && err.message);
      return new Response('Error', { status: 500 });
    }
  },
};
