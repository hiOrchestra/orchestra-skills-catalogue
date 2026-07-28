# Authoring behavioral skills

Most catalogue skills so far are **integrations** — they teach an agent to call
an external API (wordpress, coingecko). A **behavioral skill** is different: it
teaches an agent *how to think through a kind of work* — a methodology / playbook
(research, analysis, planning, review). No external API, usually no `env`.

These are the highest-leverage skills for our users: they make agents reliably
good at a task, the same way every time. This guide is the authoring standard.

## Structure (the grammar)

Behavioral skills follow a consistent section grammar (adapted from the best
public agent skills). A reader should be able to skim the headings and know how
the agent will behave. Use these sections, in this order, omitting any that
don't apply:

```
---
name: <lowercase-hyphen>
version: 0.1.0
description: >-
  What it does + WHEN to use it, in the words a user would say. This is the
  primary trigger — lead with the situation and the literal phrases.
triggers:
  - literal phrase a user would say
  - another one
metadata:
  openclaw:
    emoji: "🔎"
requires:
  bins: []
  env: []      # behavioral skills usually need nothing
  config: []
---

# <Title> — one-line what-this-is

<1–3 sentences: the job this skill does and the bar it holds to.>

## Related skills
Point to sibling skills by name and say WHEN to reach for them instead — this is
how a small library stays coherent (e.g. "use **build-report** when the output
is a document"). If a referenced skill isn't installed, the agent does the
equivalent inline.

## When to use
The concrete triggers, and — just as important — **when NOT to** (so it doesn't
poach work another skill or a native tool owns).

## Workflow
Numbered steps, imperative. The actual method. Name the tools to use
(`web_search`, `orch-files`, etc.). This is the core.

## Standards
The quality bar — non-negotiables that make the output trustworthy (sourcing,
fact-vs-inference, no fabrication, …).

## Confidence / Severity   (when the skill makes judgments)
A small labeled scale (High/Medium/Low, or Critical/High/Medium/Low) so the
agent communicates certainty instead of asserting flatly.

## Output
The exact shape of the deliverable. Say when to save a file (`orch-files`) vs
answer inline. Match depth to the ask.

## Defaults
Tie-breakers and sensible behaviors when the prompt is silent — so the agent
doesn't stall or over-ask.
```

## Principles
- **Description is the trigger.** Write it as *when to use it* + the literal
  phrases, slightly pushy. Include a `triggers:` list. Add a "not for X" so it
  doesn't collide with a neighbour or a native tool.
- **One focused capability** per skill. If it sprawls, split it and cross-link
  via "Related skills."
- **Reference native tools/skills, don't reinvent.** If OpenClaw already has a
  native tool for something (image generation, document extraction, sending a
  message), say to use it rather than describing a worse version.
- **Explain *why* a step matters** instead of piling on "MUST"s — the agent
  follows reasoning better than rules.
- Keep the body tight (aim < ~200 lines); push exhaustive reference into a
  separate section or file only if truly needed.

## Worked example
See **`skills/research-brief/SKILL.md`** — a complete behavioral skill in this
grammar (Related skills / When to use / Workflow / Standards / Confidence /
Output / Defaults).

## Registering
Add the skill to `catalog.json` like any other (slug, name, description,
category — use `methodology` for behavioral skills — tags, path, version,
`requires.env: []`).
