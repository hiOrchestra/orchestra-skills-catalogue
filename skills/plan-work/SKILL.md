---
name: plan-work
version: 0.1.0
description: >-
  Break a goal or project into a concrete, sequenced plan — tasks in the right
  order, dependencies, owners, effort, and a realistic timeline someone can
  actually execute. Use when the user says "plan", "break this down", "project
  plan", "roadmap", "how do we get this done", "sequence the work", "who does
  what by when", or hands you a goal and wants steps, "build a timeline". Not
  for choosing between options (that's a decision), and not for researching
  the domain first.
metadata:
  openclaw:
    emoji: "🗂️"
---
# Plan Work — goal → a sequenced, executable plan

Turn a goal into a plan someone can act on today: the tasks, their order and
dependencies, who owns each, rough effort, and a realistic timeline. A good plan
is honest about the critical path and the risks — not a flat wish-list of tasks
with no sequence.

## Related skills
- **decision-brief** — when the real question is *which option* (which vendor,
  which approach, build vs buy), decide that first with decision-brief; you plan
  the work only once the direction is chosen.
- **research-brief** — when you don't yet understand the domain well enough to
  decompose the goal (unfamiliar space, unknown steps), research it first, then
  come back and plan.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The direction is set and the user wants it turned into ordered, ownable work.
- Triggers: "plan X", "break this down", "roadmap for…", "sequence the work",
  "who does what by when", "give me a timeline".
- **Do NOT use** to pick between options (that's **decision-brief**) or to learn
  a domain from scratch (that's **research-brief**). A plan built on the wrong
  choice or a misunderstood domain is wasted work.

## Workflow
1. **Pin the goal and constraints.** State the concrete outcome ("done" looks
   like what?), the hard deadline, the budget/people available, and any fixed
   dependencies or non-negotiables. Vague goals produce vague plans — if these
   are missing, state a reasonable assumption and proceed rather than stalling.
2. **Decompose into milestones, then tasks.** First carve the goal into 3–6
   milestones (meaningful checkpoints that deliver something). Under each, list
   the concrete tasks. Milestones keep a long plan legible and give natural
   review points.
3. **Sequence by dependency.** For each task ask "what must be true before this
   can start?" Order tasks so nothing waits on work scheduled later. Mark tasks
   that can run in parallel — that's where a timeline gets shorter.
4. **Estimate effort.** Give each task a rough size (hours/days, or S/M/L). Be
   honest; padding hides risk and false precision erodes trust. Roll estimates
   up to milestone durations.
5. **Assign owners.** If roles/people are known, name an owner per task so
   nothing is unassigned; otherwise label by role ("designer", "backend"). An
   unowned task is a task that won't happen.
6. **Find the critical path and risks.** Trace the longest chain of dependent
   tasks — that chain sets the real end date. Flag the tasks most likely to
   slip or block others, and note a mitigation for each.
7. **Lay out the timeline.** Place milestones/tasks against real dates working
   back from the deadline (or forward from today). Check it fits the available
   people and effort; if it doesn't, say so and propose what to cut or move.
8. **Deliver** in the structure under Output. Offer to turn recurring or
   time-triggered tasks into scheduled work via `orch-jobs` if the user wants
   the plan to run itself.

## Standards
- Every task has an owner (or role), a rough effort, and a place in the sequence
  — no floating, unordered, unowned work.
- Dependencies are explicit: it's clear what blocks what, and what can go in
  parallel.
- The critical path is named, and the end date follows from it — not from
  optimism.
- Estimates are honest and labeled as estimates; risks are stated with a
  mitigation, not buried.
- Don't invent constraints, resources, or deadlines the user didn't give —
  surface the assumption instead.

## Confidence
Tag the timeline's realism so the user knows how much to trust the dates:
- **High** — scope, effort, and resources are known and the plan fits comfortably.
- **Medium** — some estimates are rough or a dependency is uncertain.
- **Low** — key unknowns, an aggressive deadline, or unconfirmed resourcing —
  call out exactly what would need to be true for the plan to hold.

## Output
Structure the plan:
- **Goal & constraints** — the outcome, deadline, resources, key assumptions.
- **Milestones** — the 3–6 checkpoints with target dates.
- **Task plan** — a table: task · owner/role · depends-on · effort · dates.
- **Critical path** — the chain that sets the end date.
- **Risks** — top risks with a mitigation each, and overall confidence.

A substantial plan → save it as a file via `orch-files` (or a real document via
`orch-docs` if it's a deliverable to share) and post a short summary. A small
plan → answer inline. Match depth to the scale of the goal.

## Defaults
- If no deadline is given, plan forward from today and state the resulting end date.
- If owners are unknown, assign by role and flag that names are needed.
- Prefer fewer, meaningful milestones over a long flat task list.
- When the plan can't fit the deadline, say so and propose the trade-off — don't
  quietly compress estimates to make it look feasible.
- Only schedule tasks via `orch-jobs` when the user asks the plan to run itself.
