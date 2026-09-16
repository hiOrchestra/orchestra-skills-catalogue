---
name: action-tracker
version: 0.1.0
description: >-
  Keep the list of who owes what to whom, by when — commitments from
  meetings, emails and chats in one table — follow them up on a cadence,
  and give the person a weekly view of what is due, late and blocked, and a
  view per person before they meet them. Use when the user says "track this",
  "follow up on", "what's outstanding", "who owes me what", "what's due this
  week", "before my meeting with X, what's open", "remind them", "chase".
  Not for planning a project from scratch (plan-work) or for writing the
  meeting up (meeting-notes).
metadata:
  openclaw:
    emoji: "📌"
---
# Action Tracker — commitments in one place, followed up, never forgotten

The chief of staff's real job: nothing that was promised falls through the
cracks. This skill keeps one table of commitments — from meeting notes, from
a forwarded email, from "can you track that" in a chat — follows each one up
at the agreed cadence, and answers the two questions that matter: what is
due this week, and what is open with the person I am about to meet.

## Related skills
- **meeting-notes** — where most actions come from.
- **plan-work** — for a project that needs sequencing; this skill tracks
  what was promised, whatever the project.
- **topic-watch** — the same routine shape, for the outside world.
- **orch-jobs** — the weekly digest and the follow-ups are routines.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Anything someone committed to, with or without a date.
- **Do NOT use** to chase people on the person's behalf outside the
  conversation without their yes: a reminder to a colleague is a message sent
  in their name.

## Workflow
1. **One table.** In the instance database (`orch-database`, table
   `actions`): id, action, owner, asked-by, due, source (the meeting file, the
   email, the chat), status (open / done / blocked / dropped), last-touched,
   notes. Create it on first use and say so.
2. **Capture.** From `meeting-notes` automatically; from an email or a message
   when the person says "track this" — one row per commitment, in the words
   used, with `[owner?]` / `[date?]` where unknown, and ask once for the gaps.
3. **Set the routine with them, once**: the weekly view — day, time, channel
   — and the follow-up rule (how many days before a due date they want a
   nudge, and whether nudges to others go through them or directly). Create
   it with `orch-jobs create`; `--notify` the channel they read.
4. **Weekly view** (the routine): due this week, late (with days late),
   blocked (and on whom), done since last week. Short; the table is the
   detail.
5. **Before a meeting**: "what is open with X" — every row where X is owner or
   asked-by, open or late, newest first, plus anything they decided together
   that is pending.
6. **Update on a word.** "Done", "push it a week", "drop it" from the person
   updates the row; say what changed. Nothing is closed by inference.

## Standards
- Every row has a source: where the commitment was made. A row without one
  is a wish.
- The person's own commitments are tracked like everyone else's, and shown
  first in their weekly view.
- A nudge to another person is drafted for the person's yes unless they set
  the rule to send directly; either way it is short, names the commitment
  and the date, and blames nobody.
- Late is a fact stated with a number of days, not a judgement.
- Dropped is a status, kept with the reason; nothing is deleted.

## Output
- Weekly view (the routine): four short sections — due this week, late,
  blocked, done — each row as `owner · action · due (· days late)`.
- Per-person view: the same rows filtered, with the last thing decided
  together.
- On capture: the row as recorded, one line, so they can correct it.

## Defaults
- Cadence unknown → Monday morning in their timezone; nudges three days
  before due and on the day.
- Owner unknown after asking → the person who asked for the meeting notes.
- No due date → "no date", listed in a fifth section once a week until one
  is set.
