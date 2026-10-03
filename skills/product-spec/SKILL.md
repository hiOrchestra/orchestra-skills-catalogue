---
name: product-spec
version: 0.1.0
description: >-
  Turn an idea, a request or a customer problem into a spec a team can build
  from — the problem and who has it, the evidence, the outcome that would
  prove it solved, what is in and explicitly out of scope, the user flows,
  acceptance criteria, risks and open questions — asking before assuming.
  Use when the user says "write a spec", "PRD", "product requirements",
  "spec this feature", "user stories", "acceptance criteria", "what exactly
  should we build", "scope this". Not for choosing between options
  (decision-brief), sequencing the work (plan-work) or the customer research
  itself (feedback-synthesis).
metadata:
  openclaw:
    emoji: "📐"
---
# Product Spec — the problem, the proof, and the line around what we build

A spec exists so that the people building, designing and selling the thing
agree on what it is before anyone builds it. The most valuable part is not
the feature list: it is the problem, the evidence that it is real, the
outcome that would show it is solved, and the explicit list of what is not
being built. This skill writes that document, and asks for what it does not
know rather than filling the gaps with plausible fiction.

## Related skills
- **feedback-synthesis** — the evidence a spec cites.
- **interview-guide** — when the problem needs talking to users first.
- **decision-brief** — when the open question is which of two approaches.
- **plan-work** — sequences the build once the spec is agreed.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Anything someone is about to build that more than one person will touch.
- **Do NOT use** to decide the roadmap, to write marketing copy, or to
  invent technical architecture the engineers have not discussed — name it
  as an open question for them.

## Workflow
1. **The problem first.** Who has it, when, what they do today instead, what
   it costs them. Ask in one round; if the person only has a solution in
   mind, ask what problem it solves and for whom.
2. **The evidence.** Customer quotes, tickets, data, lost deals — with their
   source. If there is none, the spec says so and the first step is to get
   some.
3. **The outcome.** What changes for the user, and the metric that would
   move if it worked, with today's value if known.
4. **Scope.** In: the smallest version that tests the outcome. Out: the
   tempting things that are not in this version, written down so nobody
   assumes them.
5. **Flows and requirements.** The main user flow step by step, the edge
   cases (empty, error, permission, scale), and requirements as "a {user}
   can {do} so that {outcome}", each with acceptance criteria someone can
   test.
6. **Risks and open questions** — what could make it fail, what the team
   must decide, who decides. Hand to the person; revise until they say it is
   agreed, then save it.

## Standards
- Separate what is known from what is assumed; label assumptions.
- Every requirement has acceptance criteria a tester could check without
  asking the author.
- The out-of-scope list is never empty.
- No invented user quotes, numbers or personas. A persona is a real segment
  with evidence, or it is not in the spec.
- Write for the reader who missed every meeting.

## Output
A document (`orch-files`, or `orch-docs` when the team edits it) with:
Summary (3 lines) · Problem · Evidence · Outcome and metric · Scope (in /
out) · Users and flows · Requirements with acceptance criteria · Risks ·
Open questions (owner, by when) · Changelog of the spec itself.

## Defaults
- No metric known → propose one and mark it "to confirm".
- Big idea → spec the first slice and list the rest as later versions.
- A spec revised after agreement → say what changed at the top.
