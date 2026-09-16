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
  "version": "0.2.1",
  "requires": { "env": ["COINGECKO_API_KEY"] },
  "secrets": { "COINGECKO_API_KEY": { "kind": "secret", "hosts": ["api.coingecko.com", "pro-api.coingecko.com"], "label": { "en": "CoinGecko API key", "es": "…" }, "where": { "en": "…", "es": "…" } } }
}
```

## Adding a skill

1. Create `skills/<slug>/SKILL.md` (frontmatter `name`, `version`, `description`,
   `metadata.openclaw.requires.env` for any keys it needs, and one
   `metadata.orchestra.secrets` entry per key — see "Secrets").
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

Then add any required key in the instance's secret store (the Skills page, or
the agent asks with the secure prompt), and the skill triggers on matching prompts.

## Secrets

Skills never contain secrets, and a person never types one into a chat. A key
lives in the tenant instance's **secret store** (the gateway's, one per
instance), entered through the masked prompt — by the agent when it needs it,
or on the Skills page. A skill process never sees the plaintext: it gets a
sealed sentinel in its environment, and the gateway's egress proxy swaps the
real value in only for requests to the hosts the key is bound to.

So a skill declares, per key, the contract the platform needs to store it
correctly and to explain it to the person:

```yaml
metadata:
  openclaw:
    requires:
      env: [SERVICE_API_KEY]          # bare names — the gateway gates on these
  orchestra:
    secrets:
      SERVICE_API_KEY:
        kind: secret                  # secret (default for *_TOKEN/*_KEY/*_SECRET/*_PASSWORD) | env
        hosts: [api.service.com]      # the ONLY hosts the value may reach (secret kind)
        label: { en: "Service API key", es: "Clave de API de Service" }
        where: { en: "Where to get it.", es: "Dónde conseguirla." }
```

`kind: env` is a plain variable the process can read (an id, a URL, a
username — or a real credential when the skill genuinely cannot send it
through an HTTP header to a fixed host: HTTP Basic auth base64-encodes it,
so `wordpress`'s app password is `env`, with a `why:`). Say why in `why:`;
`check-schema.py` requires a `secret` to name at least one host and every
key in `requires.env` to have an entry. Names carry no `USR_` prefix any
more (the prefix marked the old `config.env` path, retired 2026-09-16).

## What a skill requires

A requirement is true in exactly one place, the SKILL.md frontmatter, and
`catalog.json` copies it so the index can be read alone — `check-schema.py`
fails when the two disagree.

```yaml
metadata:
  openclaw:
    requires:
      env: [SERVICE_API_KEY]          # the gateway gates on these
  orchestra:
    requires:
      skills: [cloudflare]            # another catalogue skill this one builds on
      integrations: [gmail]           # Composio toolkit slugs — a bundle cannot be
                                      # hired until the tenant has connected them
```

Bundled agents (orchestra-agents-catalogue) never repeat any of this: what a
bundle needs from the person is derived from its skills at read time.
