#!/usr/bin/env node
/**
 * Render a URL in the headless Chromium on this instance, screenshot it, and
 * report the geometry that matters.
 *
 * Node rather than Python because `ws` is installed here and the Python
 * websocket client is not — a check that cannot run is worse than no check.
 *
 *   node render-and-measure.js <url> <outDir>   →  JSON on stdout
 */
const fs = require('fs');
const path = require('path');
const http = require('http');

const CDP = process.env.CDP_URL || 'http://127.0.0.1:18800';
const WIDTHS = [[1440, 900, 'desktop'], [390, 844, 'phone']];

const MEASURE = `(() => {
  // Where the INK starts, not where the box starts. A full-bleed header or
  // footer legitimately spans from 0 while its text sits on the page's column,
  // so measuring boxes reports every such site as misaligned and names the
  // correctly-built sections as the offenders. Walking to the first text node
  // asks the question a reader actually asks: does the writing line up?
  const textLeft = (el) => {
    let min = Infinity;
    const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walk.nextNode())) {
      if (!n.nodeValue || !n.nodeValue.trim()) continue;
      const rng = document.createRange();
      rng.selectNodeContents(n);
      const r = rng.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) min = Math.min(min, r.left);
    }
    return Number.isFinite(min) ? Math.round(min) : null;
  };
  const blocks = [...document.querySelectorAll('body > *, main > *, body > * > section')]
    .map(el => { const r = el.getBoundingClientRect();
      return { tag: el.tagName.toLowerCase(), cls: String(el.className || '').split(' ')[0],
               left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width),
               textLeft: textLeft(el) }; })
    .filter(b => b.w > 40);
  const icon = document.querySelector('link[rel~="icon"],link[rel="shortcut icon"]');
  return {
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth,
    favicon: icon ? icon.getAttribute('href') : null,
    title: document.title,
    textLen: (document.body.innerText || '').trim().length,
    links: [...document.querySelectorAll('a[href^="/"]')].map(a => a.getAttribute('href')),
    blocks,
  };
})()`;

const getJson = (url) => new Promise((ok, ko) => {
  http.get(url, (r) => { let b = ''; r.on('data', (c) => b += c); r.on('end', () => { try { ok(JSON.parse(b)); } catch (e) { ko(e); } }); })
    .on('error', ko);
});

(async () => {
  const [, , url, outDir] = process.argv;
  if (!url) { console.error('usage: render-and-measure.js <url> <outDir>'); process.exit(2); }
  fs.mkdirSync(outDir || '.', { recursive: true });

  // `ws` lives in the gateway's own node_modules, not on the default resolution
  // path for a script in /tmp. Look there before giving up.
  let WebSocket;
  for (const spec of ['ws', '/app/node_modules/ws', '/usr/local/lib/node_modules/ws']) {
    try { WebSocket = require(spec); break; } catch { /* keep looking */ }
  }
  if (!WebSocket) { console.log(JSON.stringify({ error: 'the ws module is not available' })); return; }

  let version;
  try { version = await getJson(`${CDP}/json/version`); }
  catch (e) { console.log(JSON.stringify({ error: `no browser at ${CDP}: ${e.message}` })); return; }

  const out = {};
  for (const [w, h, label] of WIDTHS) {
    const ws = new WebSocket(version.webSocketDebuggerUrl, { perMessageDeflate: false, maxPayload: 256 * 1024 * 1024 });
    await new Promise((ok, ko) => { ws.once('open', ok); ws.once('error', ko); });
    let id = 0;
    const pending = new Map();
    ws.on('message', (raw) => {
      const m = JSON.parse(raw);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || {}); pending.delete(m.id); }
    });
    const call = (method, params = {}, sessionId) => new Promise((ok) => {
      const mid = ++id;
      pending.set(mid, ok);
      ws.send(JSON.stringify({ id: mid, method, params, ...(sessionId ? { sessionId } : {}) }));
    });

    try {
      const { targetId } = await call('Target.createTarget', { url: 'about:blank' });
      const { sessionId } = await call('Target.attachToTarget', { targetId, flatten: true });
      const s = (m, p) => call(m, p, sessionId);

      await s('Page.enable');
      await s('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: label === 'phone' });
      await s('Page.navigate', { url });
      // Poll readyState rather than sleeping blind — a fixed wait is either
      // wasted time or too short on a cold worker.
      for (let i = 0; i < 80; i++) {
        const r = await s('Runtime.evaluate', { expression: 'document.readyState', returnByValue: true });
        if (r?.result?.value === 'complete') break;
        await new Promise((r2) => setTimeout(r2, 250));
      }
      const shot = await s('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
      const file = path.join(outDir || '.', `${label}.png`);
      fs.writeFileSync(file, Buffer.from(shot.data, 'base64'));

      const geo = await s('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
      out[label] = { ...(geo?.result?.value || {}), screenshot: file };
      await s('Page.close');
    } catch (e) {
      out[label] = { error: e.message };
    } finally {
      ws.close();
    }
  }
  console.log(JSON.stringify(out));
})();
