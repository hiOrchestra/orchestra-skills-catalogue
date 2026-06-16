# orchestra-skills-catalogue

First-party catalogue of OpenClaw **skills** for Orchestra — the place where we
(admins) grow a library of agent capabilities and install them, per-instance,
from GitHub. Mirrors the `orchestra-jobs-catalogue` pattern.

A "skill" teaches an agent how to use a tool or external API via a `SKILL.md`
(YAML frontmatter + markdown instructions). The agent follows it and runs the
needed `exec curl` / commands. Progressive disclosure: only each skill's
name+description sits in context; the body loads when triggered.

## Structure

```
catalog.json                 # index of every skill (slug, description, requires.env, path)
skills/
  <slug>/SKILL.md            # the skill itself
```

`catalog.json` entry:

```json
{
  "slug": "coingecko",
  "name": "CoinGecko",
  "description": "Live crypto prices & market data.",
  "category": "data",
  "path": "skills/coingecko/SKILL.md",
  "version": "0.2.0",
  "requires": { "env": ["USR_COINGECKO_API_KEY"] }
}
```

## Adding a skill

1. Create `skills/<slug>/SKILL.md` (frontmatter `name`, `version`, `description`,
   `triggers`, and `requires.env` for any API keys it needs).
2. Add an entry to `catalog.json`.
3. Open a PR. Once merged, it's installable on any instance.

## Installing onto an instance (admin)

Skills install into a tenant's native skills dir: `~/.openclaw/workspace/skills/<slug>/`.
This catalogue uses subfolders, so installs fetch the raw `SKILL.md` (the native
`openclaw skills install git:owner/repo` only reads a `SKILL.md` at the repo root).

Quick manual install (until the portal admin action lands) — have an agent on the
target instance run:

```bash
exec sh -c 'mkdir -p ~/.openclaw/workspace/skills/coingecko && \
  curl -fsSL https://raw.githubusercontent.com/hiOrchestra/orchestra-skills-catalogue/main/skills/coingecko/SKILL.md \
  -o ~/.openclaw/workspace/skills/coingecko/SKILL.md && echo installed'
```

Then set any required env (e.g. `USR_COINGECKO_API_KEY`) in the instance config,
and the skill triggers on matching prompts.

## Secrets

Skills never contain secrets. API keys live per-tenant in the instance
`config.env` (e.g. `USR_COINGECKO_API_KEY`), surfaced via each skill's
`requires.env` so the portal can prompt for them.
