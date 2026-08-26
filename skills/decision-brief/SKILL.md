---
name: decision-brief
version: 0.1.0
description: >-
  Weigh options against explicit criteria and recommend one, with the
  tradeoffs, risks, and reasoning laid out. Use when the user says "should
  we", "which option", "help me decide", "A vs B", "make the case for", "what
  should I choose", or "recommend one" — a defensible call, not a pros/cons
  dump, "which one should we pick", "make a recommendation", "build vs buy".
  Not for executing an already-made decision, and not for open research with
  no choice attached.
metadata:
  openclaw:
    emoji: "⚖️"
---
# Decision Brief — options → a defensible recommendation

Turn a choice into a defensible decision: frame what is being decided, lay out
the realistic options against explicit criteria, weigh the tradeoffs and risks,
and recommend one with your reasoning and confidence. The value is the reasoning
that survives scrutiny — not just picking a winner.

## Related skills
- **research-brief** — when you first need to *learn the landscape* (what the
  options even are, market facts, competitor moves) before any decision is on
  the table, do that first and feed its findings in here.
- **plan-work** — once the decision is made and the question becomes *how do we
  execute it*, hand the chosen option to plan-work to break into sequenced
  tasks. This skill stops at the recommendation.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user faces a choice and wants a reasoned recommendation with tradeoffs.
- Triggers: "should we X or Y", "which option", "help me decide", "build vs
  buy", "make the case for", "what should I choose".
- **Do NOT use** for executing a decision already made (that is plan-work), or
  for open-ended research with no decision attached (that is research-brief).

## Workflow
1. **Frame the decision + owner.** State in one sentence exactly what is being
   decided, who owns the call, and by when. A fuzzy question produces a fuzzy
   recommendation, so pin the scope before anything else. If it is ambiguous,
   state a reasonable framing and proceed.
2. **Define criteria + weights.** List the 3–6 factors that actually decide this
   (cost, speed, risk, fit, reversibility, …) and roughly how much each matters.
   Naming the criteria up front is what keeps the choice honest and stops the
   recommendation from being a gut call dressed up after the fact.
3. **Enumerate real options — including do-nothing.** List the genuinely viable
   options, not strawmen. Always include the status-quo / do-nothing baseline;
   it is often the right answer and is the yardstick for the rest.
4. **Evaluate each against the criteria, with evidence.** Score or rate every
   option on every criterion, citing what backs each judgment. Use `web_search`
   / `web_fetch` for external facts and `orch-database` for the tenant's own
   numbers. Separate fact from your inference.
5. **Surface tradeoffs, risks & reversibility.** For the leading options, name
   what you give up, the top failure modes, and how hard the choice is to
   reverse. A cheap-to-reverse option deserves a lower bar than a one-way door.
6. **Recommend one.** Pick a single option, give the reasoning in plain terms,
   attach a confidence level, and state what new information would change the
   call. Deliver in the structure under Output.

## Standards
- The criteria are stated **before** the recommendation, not reverse-engineered
  to justify a favourite.
- Every option is evaluated against the *same* criteria — no moving goalposts.
- Each material judgment carries evidence; distinguish **fact** (sourced) from
  **inference** (your reasoning) from **assumption** (flag it).
- Steelman the option you do *not* pick — a brief that only argues one side is
  not trustworthy.
- Never fabricate a number, source, or quote to make a case. If a criterion
  can't be evidenced, say so and lower confidence.

## Recommendation confidence
State one overall level, and say what would move it:
- **High** — criteria clear, evidence solid, the winner leads on the factors
  that matter most; new information is unlikely to flip it.
- **Medium** — a defensible call, but sensitive to assumptions or thin evidence
  on a key criterion.
- **Low** — options are close, evidence is weak or contested, or the decision
  hinges on an unknown; name what to resolve before committing.

## Output
Structure the brief:
- **Decision** — the one-sentence question, owner, and deadline.
- **Recommendation** — the chosen option + confidence + one-line why.
- **Criteria** — the factors and their weights.
- **Options compared** — a compact table or bullets: each option scored against
  each criterion, with evidence.
- **Tradeoffs & risks** — what the recommendation costs, its failure modes, and
  reversibility.
- **What would change the call** — the assumption or fact that, if wrong, flips
  the decision.

Substantial or multi-option comparison → save it as a file via `orch-files`
(consider a real document via `orch-docs` if it's a deliverable for others) and
post a short summary. Quick two-way call → deliver inline. Match depth to stakes.

## Defaults
- Always include the do-nothing baseline, even when unasked.
- If criteria are unstated, propose a sensible set, say you're assuming them, and
  proceed — don't stall waiting for perfect inputs.
- Recommend exactly one option; note a runner-up only if it's genuinely close.
- Weight reversibility: bias toward cheaply-reversible options when evidence is
  thin, and hold one-way doors to a higher bar.
- A clear recommendation on 4 well-evidenced criteria beats a hedge across 12.
