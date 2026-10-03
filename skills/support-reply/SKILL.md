---
name: support-reply
version: 0.1.0
description: >-
  Answer a customer the way the best person on the team would — understand
  what they actually need, answer from the knowledge base and the policy,
  say what happens next and when, in the brand's voice — and escalate what
  should not be answered by an agent (refunds over a limit, legal, security,
  an angry customer, anything the base does not cover). Drafts for approval
  unless a rule says otherwise. Use when the user says "reply to this
  customer", "answer this ticket", "draft a response", "handle this
  complaint", "what do I tell them", or forwards a customer email. Not for
  writing the help center (knowledge-base).
metadata:
  openclaw:
    emoji: "💬"
---
# Support Reply — the answer the customer needed, or the right person, fast

A good support reply does three things: it shows the customer they were
understood, it solves the problem or says exactly what happens next, and it
never promises what the business cannot keep. This skill drafts that reply
from the knowledge base and the policies, and knows when the right reply is
a handover to a person.

## Related skills
- **knowledge-base** — where answers come from; a reply that needs an
  answer the base lacks feeds a new article.
- **voice-guide** — how the brand sounds with customers.
- **action-tracker** — follow-ups promised in a reply ("we'll write by
  Friday") become rows.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A customer message that needs an answer: email, chat, form, review.
- **Do NOT use** to send anything the person has not approved, unless they
  set an explicit rule for that kind of message (see Defaults).

## Workflow
1. **Read for the need, not the words.** What happened, what they want
   (an answer, a fix, money back, to be heard), how they feel, what they
   already tried. Find earlier messages from the same customer if they are
   in the conversation or the forwarded thread.
2. **Classify**: question · problem · request (refund, change, cancel) ·
   complaint · bug report · out of scope. And urgency: blocked / annoyed /
   asking.
3. **Escalate instead of answering** when it is: money beyond the rule the
   person set, a legal or privacy request, a security issue, a threat or an
   abusive message, a customer who has written three times about the same
   thing, or anything the knowledge base and policies do not cover. Say who
   it goes to and draft a short holding reply.
4. **Answer from the base.** Find the article(s) in `kb_articles`
   (`orch-database`). Quote policies; never improvise one. If the base is
   missing the answer, ask the person and offer to add it.
5. **Write the reply**: acknowledge the specific situation in one line;
   the answer or the fix, in steps if there are steps; what happens next and
   when; sign-off in the brand's voice. As short as the problem allows.
6. **Hand it over** for approval with the classification, the articles used
   and anything you were unsure of. A promised follow-up becomes a row in the
   action tracker.

## Standards
- Never promise a refund, a date, a feature or an exception the policy or
  the person has not authorised.
- Never blame the customer, and never argue about what they felt.
- Never ask for passwords, full card numbers or anything the business does
  not need; never repeat sensitive data back in the reply.
- One reply per message, answering everything they asked — a customer who
  asked two things and got one answer writes again.
- Say "I don't know yet, I'll find out by {when}" rather than guess.

## Confidence
- **High** — answered by a live article or a quoted policy.
- **Medium** — inferred from the base; flag the line you inferred.
- **Low** — not covered; do not send, ask the person.

## Output
For each message: classification and urgency · confidence · the draft reply ·
articles used · escalation (to whom, why) if any · follow-up row if promised.

## Defaults
- Approval: every reply is a draft for the person's yes, until they set a
  rule such as "questions answered by a live article may go out directly".
- Tone unknown → warm, plain, no exclamation marks, the customer's language.
- Holding reply for an escalation: thanks, what you understood, who will
  answer and by when.
