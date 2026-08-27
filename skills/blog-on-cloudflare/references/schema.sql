-- Blog schema for Cloudflare D1.
--
-- One database per blog. Do NOT share a database between two sites: the second
-- app's tables end up beside the first's, and a later deploy that reuses the
-- worker name silently replaces a live site. That has already happened once.
--
-- Apply with:
--   POST /accounts/{account}/d1/database/{db}/query   {"sql": "<this file>"}

CREATE TABLE IF NOT EXISTS posts (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  slug         TEXT    UNIQUE NOT NULL,
  title        TEXT    NOT NULL,
  subtitle     TEXT    NOT NULL DEFAULT '',
  excerpt      TEXT    NOT NULL DEFAULT '',
  content      TEXT    NOT NULL,              -- markdown
  hero_image   TEXT,
  hero_alt     TEXT    NOT NULL DEFAULT '',
  section      TEXT    NOT NULL DEFAULT '',   -- the blog's own taxonomy
  author       TEXT    NOT NULL DEFAULT '',
  -- draft   → never served, not even by slug
  -- review  → served only at /preview/:slug with the preview token
  -- live    → served publicly ONCE published_at has passed
  --
  -- Scheduling needs no cron and no second mechanism: a scheduled post is a
  -- `live` row whose published_at is in the future, and every public query
  -- filters on published_at <= now.
  status       TEXT    NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','review','live')),
  published_at TEXT,
  created_at   TEXT    NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT    NOT NULL DEFAULT (datetime('now')),
  -- Where this came from, when it was imported rather than written here. Keeps
  -- a migration re-runnable: the same source URL never lands twice.
  source_url   TEXT    UNIQUE
);
CREATE INDEX IF NOT EXISTS posts_public ON posts(status, published_at DESC);
CREATE INDEX IF NOT EXISTS posts_section ON posts(section, published_at DESC);

-- One reaction per visitor per post, enforced by the database rather than by
-- the cookie alone — a cookie is a hint, the UNIQUE constraint is the rule.
CREATE TABLE IF NOT EXISTS post_reactions (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id    INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  visitor_id TEXT    NOT NULL,
  reaction   TEXT    NOT NULL CHECK (reaction IN ('like','dislike')),
  created_at TEXT    NOT NULL DEFAULT (datetime('now')),
  UNIQUE (post_id, visitor_id)
);

-- Comments appear IMMEDIATELY by default. A blog with three readers and a
-- moderation queue is a blog where nobody ever sees their comment appear, and
-- the conversation dies. The agent sweeps for spam on a schedule instead, and
-- the owner can switch to hold-for-approval whenever they want — that is the
-- `comments_mode` setting, not a schema change.
--
-- `hidden` rather than deleting: a removed comment stays readable to the owner
-- so "why did you delete mine" has an answer.
CREATE TABLE IF NOT EXISTS comments (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id    INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  author     TEXT    NOT NULL,
  email      TEXT    NOT NULL DEFAULT '',
  body       TEXT    NOT NULL,
  status     TEXT    NOT NULL DEFAULT 'approved'
             CHECK (status IN ('pending','approved','spam','hidden')),
  -- What the spam sweep concluded, so a judgement can be reviewed rather than
  -- just applied. NULL until the agent has looked at it.
  spam_score REAL,
  spam_reason TEXT,
  reviewed_at TEXT,
  visitor_id TEXT    NOT NULL DEFAULT '',
  created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS comments_post ON comments(post_id, status, created_at);

-- Daily view counts. Rolled up per day rather than one row per hit, so the
-- table stays small enough to sync into the instance for the Canvas.
CREATE TABLE IF NOT EXISTS post_views (
  post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  day     TEXT    NOT NULL,
  views   INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (post_id, day)
);

-- Abuse ceiling for the two public write endpoints, keyed by IP + window.
CREATE TABLE IF NOT EXISTS rate_limits (
  bucket   TEXT    PRIMARY KEY,
  count    INTEGER NOT NULL,
  reset_at INTEGER NOT NULL
);

-- Everything the site says about itself AND every behaviour the owner can
-- change, so the agent can retune the blog without a redeploy.
--
-- This table IS the list of dials. The skill tells the agent to read it and
-- offer these choices, because an owner cannot ask for a setting they have
-- never been told exists.
CREATE TABLE IF NOT EXISTS settings (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
--
-- Any `ui_<key>` row overrides one visitor-facing string (see UI in worker.js).
-- That is how a blog speaks Catalan, German or Portuguese without forking the
-- worker: the agent writes the words once, per blog.
INSERT OR IGNORE INTO settings (key, value) VALUES
  ('comments_mode',     'open'),      -- open | review | closed
  ('reactions_enabled', 'true'),
  ('spam_sweep',        'weekly'),    -- weekly | daily | off
  ('locale',            'en'),
  ('accent',            '#1f3b2c'),
  ('posts_per_page',    '60');
