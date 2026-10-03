---
name: contract-review
version: 0.1.0
description: >-
  Read a contract against the business's own playbook — the positions it
  wants, accepts and refuses on each clause (liability, indemnity, payment,
  term and renewal, termination, IP, confidentiality, data protection,
  governing law) — and return what deviates, how much it matters, the
  wording to propose instead, and the dates and obligations to track; always
  as preparation for a decision, never as legal advice. Use when the user
  says "review this contract", "check this NDA", "redline", "what should I
  push back on", "is this MSA ok", "terms to negotiate", "when does this
  renew". Not for drafting a contract from scratch or for any dispute or
  litigation matter — those go to counsel.
metadata:
  openclaw:
    emoji: "⚖️"
---
# Contract Review — what this contract asks of you, against what you accept

Most contract review is not law, it is comparison: what does this document
say on the clauses that matter, and how far is that from what the business
already decided it accepts. This skill does that comparison clause by
clause, ranks the gaps, proposes wording from the playbook, and pulls out
the dates and obligations someone has to remember. It prepares the decision;
a qualified lawyer makes the legal one.

## Related skills
- **action-tracker** — renewal, notice and payment dates become rows.
- **distill** — a plain-language summary of a long agreement.
- **decision-brief** — sign, negotiate or walk away, when the call is close.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A contract or terms the business is asked to sign, or one it already
  signed whose obligations need tracking.
- **Do NOT use** for disputes, litigation, regulatory investigations,
  employment terminations, or any question of what the law requires in a
  jurisdiction — say it needs counsel and offer the summary to send them.

## Workflow
1. **Read the playbook.** The business's positions per clause: preferred,
   acceptable fallback, walk-away. It lives in the agent's procedure; if
   there is none, use the defaults below and label them as such.
2. **Identify the document.** Type (NDA, MSA, SaaS terms, DPA, SOW, lease),
   parties, which side the business is on, governing law, version and date.
   Note missing schedules or documents it incorporates by reference.
3. **Map every clause that matters** to the playbook: liability cap and
   exclusions, indemnities, payment and late fees, price changes, term,
   auto-renewal and notice period, termination rights, IP ownership and
   licences, confidentiality and its duration, data protection and
   sub-processors, warranties, assignment, non-compete or exclusivity,
   governing law and venue.
4. **Rate each deviation** (Severity) and propose the playbook wording or a
   compromise, quoting the clause number and the exact current text.
5. **Extract obligations and dates**: effective date, renewal date, notice
   deadline (counted back), payment schedule, deliverables, reporting duties.
   Offer to add them to the tracker.
6. **Summarise** for the person: sign as is / sign with these changes /
   do not sign without counsel — as a recommendation with its reasons.

## Standards
- Quote the contract exactly with the clause number; never paraphrase a
  clause in a way that changes its meaning.
- Separate what the contract says from what you infer it means.
- Say "this needs a lawyer" whenever a clause is unusual, a liability is
  uncapped, the law is unfamiliar, or the stakes are high — every time, not
  once.
- Never state that a clause is legal, enforceable or compliant.
- Contracts are confidential: nothing from them leaves the conversation or
  the instance unless the person asks.

## Severity
- **Critical** — walk-away territory: uncapped liability, broad indemnity,
  IP assigned away, auto-renewal with a long notice the person cannot meet.
- **High** — outside the acceptable fallback; negotiate.
- **Medium** — worse than preferred but acceptable.
- **Low** — drafting or clarity.

## Output
- **Verdict** in three lines, with the critical items named.
- **Deviation table**: clause · current text · playbook position · severity ·
  proposed wording.
- **Dates and obligations** with the notice deadlines computed.
- **For counsel** — the questions to put to a lawyer, if any.
- Saved with `orch-files` next to the contract.

## Defaults (when there is no playbook yet)
- Liability capped at 12 months of fees, mutual; no cap only for
  confidentiality and data breaches the business caused.
- Mutual indemnities limited to third-party IP claims.
- Notice of non-renewal ≥ 30 days, flagged 30 days before the deadline.
- Payment 30 days net; price increases capped and announced 60 days ahead.
