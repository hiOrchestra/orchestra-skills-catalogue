---
name: retention-play
version: 0.1.0
description: >-
  Decide and prepare what to do for one customer account at risk or up for
  renewal — what is really going wrong, who to talk to, what to offer within
  what the business allows, the message or the call plan, and how to know it
  worked — and prepare a renewal or business review with the value delivered.
  Use when the user says "save this account", "they want to cancel", "prepare
  the renewal", "QBR", "business review", "what do I say to them", "win back",
  "they're unhappy". Not for scoring the whole base (account-health).
metadata:
  openclaw:
    emoji: "🛟"
---
# Retention Play — the right move for this account, prepared

Saving an account is rarely about a discount. It is about finding what
actually went wrong — a missing feature, a champion who left, a bad month of
support, value nobody showed them — and doing the one thing that addresses
it. This skill reads the account, names the cause it can see, and prepares
the conversation, the message and the follow-up.

## Related skills
- **account-health** — where the risk signal comes from.
- **feedback-synthesis** — when the cause looks like a pattern across accounts.
- **meeting-notes** — the call itself, written up.
- **action-tracker** — the promises made in the call, followed up.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- One account: at risk, asking to cancel, or with a renewal coming.
- **Do NOT use** to offer a discount, credit or exception the person has
  not authorised, or to contact the customer without their yes.

## Workflow
1. **Read the account.** Health signals, recent tickets, last conversations,
   what they bought it for, who the champion and the decision-maker are, the
   renewal date and value.
2. **Name the likely cause** — with the evidence — and what you cannot see.
   Typical causes: never onboarded, champion left, a missing capability, a
   bad support experience, price vs value, budget cuts.
3. **Choose the play** that fits the cause: re-onboarding, an executive
   check-in, a fix or workaround, a plan change, showing the value delivered,
   or a graceful exit that keeps the door open. Offers only from what the
   person allows (their procedure says the limits).
4. **Prepare it**: the email or call plan in the person's voice, the three
   questions to ask, what to listen for, the offer if any, the fallback.
5. **For a renewal or business review**: the outcomes they got (with
   numbers where the data has them), what changed since last review, what is
   next, the risks to raise before the customer does.
6. **After**: what was agreed goes to the tracker; the health status is
   updated with what was learned.

## Standards
- The cause is a hypothesis until the customer confirms it; say which.
- No offer beyond the limits the person set, ever.
- Value claims use the customer's own data, not the brochure.
- A customer who wants to leave is treated with respect: the exit path is
  easy and the door stays open.

## Output
Account summary (5 lines) · likely cause and evidence · the play and why ·
the message or call plan · offer and limit · how we will know it worked ·
follow-up dates.

## Defaults
- No limits set → no discounts or credits; propose and wait for the yes.
- Channel → a short email asking for a call, from the account owner.
- Renewal prep → three weeks before the date.
