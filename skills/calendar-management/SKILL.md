---
name: calendar-management
version: 0.1.0
description: >-
  Keep the person's Google Calendar working for them — the day and week
  ahead with what each meeting needs, conflicts and double bookings found,
  slots proposed for a meeting request, focus time protected by their
  rules, and events created or moved only with their yes. Use when the user
  says "what's my day", "my week", "find a time", "schedule a meeting with",
  "move my 3pm", "am I free", "block time for", "prep me for my meetings".
  Needs Google Calendar connected. Not for writing up a meeting afterwards
  (meeting-notes).
metadata:
  openclaw:
    emoji: "🗓️"
  orchestra:
    requires:
      integrations:
        - googlecalendar
---
# Calendar Management — the week arranged around what matters

A calendar is the person's priorities made visible. This skill reads it
through their connected Google Calendar, shows the day and week with what
each meeting needs, finds the conflicts before they bite, proposes times
that respect their rules, and changes nothing without their yes.

## Related skills
- **inbox-triage** — meeting requests arrive by email.
- **meeting-notes** — the meeting afterwards.
- **action-tracker** — what is open with the people they are about to meet.
- **orch-composio** — how Calendar is read and written
  (`orch-composio execute GOOGLECALENDAR_…`).
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The daily or weekly view, scheduling, rescheduling, preparing meetings.
- **Do NOT use** to accept, decline, create, move or delete events, or to
  invite anyone, without the person's yes on that exact change.

## Workflow
1. **Check the connection**: `orch-composio connections`; if Google Calendar
   is not connected, say so and stop. Use the calendar their procedure names.
2. **Read** the period (`GOOGLECALENDAR_EVENTS_LIST` with `timeMin`/`timeMax`
   in their timezone).
3. **The day / week view**: each event with time, who, where (link or
   place), and what it needs — a document to read, a decision to bring, what
   is open with those people (from the tracker).
4. **Find problems**: overlaps, back-to-back blocks with no travel time,
   meetings outside their working hours, focus blocks eaten, events with no
   agenda, declined-by-everyone meetings still on the calendar.
5. **Scheduling a request**: propose 2–3 slots that respect their rules
   (hours, buffer, focus days, max meetings per day), with the reason for
   each; create the event only after the yes, with title, attendees, link
   and agenda.
6. **Moving or cancelling**: propose the change and the message to the
   other attendees; do it only after the yes.

## Standards
- Every change is shown before it is made; nothing is changed silently.
- Times are always shown in the person's timezone, and in the other
  person's when they differ.
- Private events are shown as busy, never described to others.
- Their rules (working hours, buffers, focus time) win over convenience.

## Output
Day: timeline with prep notes and problems flagged. Week: load per day,
conflicts, what to prepare. Scheduling: the slots and the draft invitation.

## Defaults
- Working hours → 9:00–18:00 local, Monday to Friday, until they say.
- Buffer → 10 minutes between meetings; 30 if a place changes.
- Daily view → each weekday morning with the inbox triage.
