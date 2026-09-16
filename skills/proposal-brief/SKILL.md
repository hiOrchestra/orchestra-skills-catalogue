---
name: proposal-brief
version: 0.1.0
description: >-
  Read a call, tender, RFP or grant announcement the way a proposal writer
  does — eligibility, deadlines, what is scored and how, every requirement
  as a checklist — and turn it into a go/no-go, a compliance matrix and the
  outline the response must follow before a word is written. Use when the
  user says "RFP", "tender", "call for proposals", "grant", "bid", "should we
  apply", "what do they ask for", "compliance matrix", or sends the document
  of a call. Not for writing the sections (write-article), the final
  document (build-report), or researching the funder (research-brief).
metadata:
  openclaw:
    emoji: "📑"
---
# Proposal Brief — the call, read like an evaluator

Proposals lose on what the evaluator could not find, not on what was badly
written. This skill reads the call first as a set of rules — who may apply,
by when, in what format, scored on what — and produces the three things every
response starts from: whether to go, a compliance matrix nobody can miss a
line of, and an outline in the evaluator's order.

## Related skills
- **research-brief** — the funder or buyer: what they funded before, what
  they say they want.
- **decision-brief** — the go/no-go, when it is close.
- **write-article** — writes each section to this outline; **fact-check**
  checks every claim in it; **build-report** produces the document.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A call has arrived and someone has to decide whether and how to answer.
- **Do NOT use** to write the proposal before the matrix exists. Do not
  soften a hard requirement ("must have three years of audited accounts")
  into a maybe — an ineligible bid costs the whole effort.

## Workflow
1. **Get the whole call.** The announcement, the annexes, the questions and
   answers, the template if there is one — ask for what is missing. Read it
   all, with `web_fetch` for links.
2. **Extract the rules**: eligibility (who, where, size, legal form),
   deadlines (submission, questions, clarifications, decision), format
   (pages, language, sections, files, portal), budget (limits, co-funding,
   eligible costs), and the evaluation grid — criteria, weights, thresholds,
   in the call's exact words.
3. **The compliance matrix.** One row per requirement, verbatim reference
   (section, page), what it asks, mandatory or scored, weight, where the
   response will answer it, and a status column (have it / can get it /
   do not have it).
4. **Go/no-go.** Against what the person has told you they can offer (their
   capabilities, past work, budget, capacity): the requirements they cannot
   meet, the effort, the fit with what the evaluator scores. A
   recommendation in one line, and the two or three facts that would flip it.
   Hand it to `decision-brief` when the call is close.
5. **The outline.** Sections in the order the grid scores them, each with
   the requirements it must cover (from the matrix), the page budget, the
   evidence needed (a reference, a CV, a figure) and who provides it.
6. **Deliver** under Output; save the matrix as a table people will fill in.

## Standards
- Requirements are quoted, with their reference. A paraphrase is where lines
  get lost.
- Mandatory and scored are never mixed: a mandatory item is pass/fail, and
  one fail ends the bid.
- Deadlines carry the timezone and the exact hour when the call states one.
- What the person cannot prove is a gap, listed, not a sentence to write
  around.
- Nothing about the funder's intentions is asserted beyond what the call and
  `research-brief` support.

## Output
- **Call** — name, issuer, deadline (date, hour, timezone), submission
  channel.
- **Go / no-go** — one line, the reasons, what would flip it.
- **Eligibility** — each rule, met / not met / unknown.
- **Compliance matrix** — the table (`orch-files`, `proposals/<call>/
  matrix.md` or `.xlsx` on request).
- **Outline** — sections in scoring order, with requirements, page budget,
  evidence, owner.
- **Questions to ask the issuer** — before the clarification deadline.

## Defaults
- No evaluation grid published → outline in the order of the call's
  requirements, and say the weights are unknown.
- Page budget unknown → proportional to the weights, stated as assumed.
- Multiple lots → one matrix per lot, one go/no-go each.
