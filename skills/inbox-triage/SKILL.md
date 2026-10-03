---
name: inbox-triage
version: 0.1.0
description: >-
  Go through the person's Gmail inbox and sort it: what needs them today,
  what can wait, what is waiting on someone else, what is noise — with a
  one-line summary of each that matters, replies drafted for their yes, and
  commitments pulled out to track. Never sends, archives or deletes without
  the rule or the yes. Use when the user says "go through my inbox", "what
  needs me", "triage my email", "summarise my emails", "draft replies",
  "inbox zero", "what did I miss". Needs Gmail connected. Not for customer
  support queues (support-reply).
metadata:
  openclaw:
    emoji: "📥"
  orchestra:
    requires:
      integrations:
        - gmail
---
# Inbox Triage — what needs you, in five minutes instead of fifty

An executive assistant's first job is to make the inbox small: the few
messages that need the person today on top, each summarised in one line, a
reply already drafted where one is due, and everything else sorted where it
belongs. This skill does that through the person's connected Gmail, and
touches nothing they have not allowed.

## Related skills
- **calendar-management** — when an email is really a meeting request.
- **action-tracker** — commitments found in email become rows.
- **distill** — a long thread compressed to its decision.
- **orch-composio** — how Gmail is read (`orch-composio execute GMAIL_…`).
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A regular pass over the inbox, or "what did I miss" after time away.
- **Do NOT use** to send, archive, label, delete or unsubscribe without
  either the person's yes or an explicit standing rule from their procedure.

## Workflow
1. **Check the connection**: `orch-composio connections` — if Gmail is not
   connected, say so and stop. If more than one Gmail account is connected,
   use the one their procedure names.
2. **Fetch** the messages since the last triage (`GMAIL_FETCH_EMAILS` with a
   query such as `in:inbox newer_than:1d`); read threads, not single
   messages, so a reply already sent is seen.
3. **Sort** each thread: **Needs you today** (a question to them, a
   decision, a deadline within 48 h, someone important waiting), **This
   week**, **Waiting on others**, **FYI**, **Noise** (newsletters,
   notifications, promotions).
4. **Summarise** each thread that is not noise in one line: who, what they
   want, by when.
5. **Draft replies** for the threads that need one, in the person's voice,
   saved as Gmail drafts only if their procedure allows drafts; otherwise
   shown in the conversation.
6. **Extract commitments** — what they promised, what others promised them —
   into the action tracker, with the thread as source.
7. **Apply standing rules** only as written (e.g. "label newsletters",
   "archive notifications from X"), and report what was done.

## Standards
- Nothing is sent, ever, without the person's yes on that exact text.
- A sender is "important" because the person said so, not because of a title.
- Private and sensitive content is summarised discreetly and never shared
  outside the conversation.
- If unsure where a thread goes, it goes up, not down.

## Output
**Needs you today** (≤ 7, one line each, draft ready or not) · **This week** ·
**Waiting on others** · counts of FYI and noise · rules applied · new
commitments tracked.

## Defaults
- Cadence → every weekday morning in their timezone.
- Drafts → shown in the conversation until they allow Gmail drafts.
- Noise → counted, never listed, never archived without a rule.
