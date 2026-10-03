---
name: account-health
version: 0.1.0
description: >-
  Score how healthy each customer account is from the signals the business
  already has — product usage, logins, seats used, support tickets and their
  tone, payments, contract dates, the last real conversation — and list the
  accounts at risk with the evidence and the date that makes it urgent. Use
  when the user says "account health", "who is at risk", "churn risk",
  "which customers might leave", "health score", "renewals coming up",
  "customer health dashboard". Not for what to do about a risky account
  (retention-play) or for reading feedback themes (feedback-synthesis).
metadata:
  openclaw:
    emoji: "🩻"
---
# Account Health — who might leave, why we think so, and by when it matters

A health score is useful only if a person would agree with it after reading
the evidence. This skill builds the score from signals the business already
records, shows every signal behind it, and turns it into a short list: the
accounts at risk, ranked by what is at stake and how soon.

## Related skills
- **retention-play** — what to do for an account this skill flags.
- **analyze-data-quality** — when the exports look incomplete or inconsistent.
- **build-dashboard** — the health view as a Canvas page the team opens.
- **action-tracker** — renewal dates and promised check-ins become rows.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A recurring look at the customer base, or before renewals.
- **Do NOT use** to rank individual people inside a customer, or to infer
  anything about a customer from data the business does not hold.

## Workflow
1. **The signals that exist.** Ask what they can export: usage (logins,
   active users, key actions), seats bought vs used, plan and revenue,
   support tickets, payment history, contract start/renewal dates, notes
   from the last calls. Use what arrives; do not wait for a perfect set.
2. **Agree the definition** with the person once: which signals matter for
   this product and what "bad" looks like for each (e.g. active users down
   30% over 30 days, two failed payments, no login in 21 days, renewal in
   under 60 days with no contact).
3. **Score** each account per signal (healthy / watch / risk) and overall,
   keeping the reasons. Store it in the instance database
   (`orch-database`, table `account_health`: account, signal values,
   status, reasons, renewal_date, revenue, updated_at).
4. **Rank the at-risk list** by revenue at stake × time to renewal. The top
   of the list is what a person should look at this week.
5. **Re-run** on the cadence agreed and lead with what changed since last
   time — who moved into risk, who recovered.

## Standards
- Every status shows the signals behind it. A score with no reasons is noise.
- Say which signals were missing for an account instead of scoring it as
  healthy by default.
- Correlation is not cause: "usage dropped" is a fact; "they are unhappy" is
  an inference to check in a conversation.
- Customer data stays in the instance.

## Output
- **At risk this week** (top 5–10): account · revenue · renewal · status ·
  the two signals that matter most · suggested next step.
- **Moved since last time**: into risk, out of risk.
- **Coverage**: accounts scored, signals missing.
- The full table in `account_health`, or a Canvas view if they asked.

## Defaults
- No definition agreed yet → propose one from the signals that exist and
  mark it provisional.
- No revenue figures → rank by time to renewal, then by number of risk signals.
- Cadence → weekly, the day before their team meeting.
