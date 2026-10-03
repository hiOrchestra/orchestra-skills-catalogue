---
name: outreach-sequence
version: 0.1.0
description: >-
  Write a short outbound sequence to a prospect — a first message built on a
  real reason to write, two or three follow-ups that each add something new,
  and a polite close — personalised from the account research, in the
  seller's voice, under 120 words each, with one clear ask; for email or
  LinkedIn. Drafts for approval; never sends on its own. Use when the user
  says "write a cold email", "outreach sequence", "follow-ups", "prospecting
  emails", "LinkedIn message to", "how do I reach out to", "sequence for
  these accounts". Not for researching the account (account-research) or
  replying to a customer (support-reply).
metadata:
  openclaw:
    emoji: "✉️"
---
# Outreach Sequence — a reason to write, a reason to reply, and a way out

Cold outreach fails when it is about the seller. This skill writes a short
sequence about the prospect: the specific reason to write now, what is in it
for them, one easy ask — and follow-ups that each bring something new rather
than "just bumping this". It drafts; the person approves and sends.

## Related skills
- **account-research** — the brief this sequence stands on; run it first.
- **voice-guide** — the seller's own voice.
- **proofread-edit** — the last pass before sending.
- **action-tracker** — the follow-up dates become rows.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Outreach to a named person at a researched account, or a template for a
  segment with slots for the specifics.
- **Do NOT use** to send messages, to write to people on a do-not-contact
  list or who have opted out, or to write anything that pretends to a
  relationship, a referral or a conversation that did not happen.

## Workflow
1. **Read the brief.** The reason to write now, the problem signal, the
   person's role. No brief → run `account-research` or ask; no real reason
   → say the account is not ready and stop.
2. **One message, one job.** First touch: the reason (their signal, in one
   line), why it matters to someone in their role, one proof (a similar
   customer's result, with permission), one low-effort ask (a question, a
   resource, 15 minutes).
3. **Follow-ups that add something.** Each follow-up brings a new angle — a
   relevant resource, a different proof, a short insight about their
   situation — never "following up on my last email". Space them (Defaults).
4. **The close.** A last short message that makes it easy to say no or "not
   now", and says you will not write again.
5. **Subject lines** — short, specific, lower case is fine, no tricks
   ("Re:" on a first email is a lie).
6. **Hand over** the sequence with the personalisation highlighted, so the
   person can check every claim, and the send dates as tracker rows.

## Standards
- Under 120 words per email; LinkedIn messages under 60.
- Every personal line is backed by the research; nothing made up, nothing
  creepy (no personal life, no "I saw you were at …" from private sources).
- One ask per message.
- Honest sender, honest subject, a clear way to opt out where the law asks
  for one (and in the EU and UK, only to business contacts with a legitimate
  interest).
- No fake urgency, no false scarcity, no fake "Re:"/"Fwd:".

## Output
For each touch: day · channel · subject · body · word count · what it adds.
Then: the claims to verify before sending, and the follow-up schedule.

## Defaults
- Cadence: day 0, day 3, day 8, day 15 (the close).
- Channel: email; LinkedIn only if the person says they use it.
- Language: the prospect's, if known; otherwise the person's.
