---
name: meeting-notes
version: 0.1.0
description: >-
  Turn a meeting — a transcript, a recording's text, rough notes, a thread —
  into the record that matters: decisions taken, actions with an owner and a
  date, open questions, and a short summary for the people who were not
  there. Use when the user says "notes from the meeting", "minutes", "what
  did we decide", "action items", "write up the call", "summarize this
  transcript", or sends you a transcript or notes. Not for compressing a
  document for reading (distill) or for following the actions afterwards
  (action-tracker).
metadata:
  openclaw:
    emoji: "📝"
---
# Meeting Notes — a meeting → decisions, actions, open questions

A meeting produces three things worth keeping: what was decided, who will do
what by when, and what was left open. Everything else is the path there. This
skill extracts those three from whatever record exists, in the words people
used, and writes them where the team will find them again.

## Related skills
- **action-tracker** — the actions from here go into the tracker; it follows
  them up.
- **distill** — a summary for reading; this skill produces a record for acting.
- **decision-brief** — when a question left open needs a recommendation.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Any record of a meeting or call, in any shape, that people need to act on.
- **Do NOT use** to invent what was not said: a decision that is not in the
  record is an open question. Never attribute a commitment to someone who did
  not make it.

## Workflow
1. **Read the whole record first.** Note who was there (from the record or
   from the person), the date, what the meeting was for.
2. **Decisions.** Each one in one sentence, as stated — what was decided, by
   whom if it matters, and the reason if one was given. A "let's think about
   it" is not a decision.
3. **Actions.** Each with an owner, a verb, an object and a date. Where the
   record has no date or owner, mark it `[owner?]` / `[date?]` — never fill
   it in. If the person was in the meeting, ask them to fill the gaps in one
   message, all at once.
4. **Open questions.** What was raised and not resolved, and who it waits on.
5. **Summary** — 3–5 lines for someone who was not there: purpose, outcome,
   what happens next.
6. **Write it** in the shape under Output to `orch-files` (`meetings/<date>
   -<topic>.md`), and hand the actions to `action-tracker` if it is installed.
   Send the summary and the actions where the person asked to receive them.

## Standards
- Decisions and actions in the words used, not paraphrased into something
  stronger or weaker.
- Names as they appear; do not guess who "he" was.
- Numbers, dates and amounts copied exactly, with what they refer to.
- What was disagreed on is recorded as disagreement, with both positions.
- Anything sensitive said in the room (a person's performance, a salary, a
  health matter) is left out of the summary and mentioned only to the person
  who asked for the notes.

## Output
`meetings/<date>-<topic>.md`:
- **Meeting** — date, who, purpose (one line each).
- **Decisions** — numbered.
- **Actions** — table: owner · action · due · status.
- **Open questions** — bullets, each with who it waits on.
- **Summary** — 3–5 lines.

## Defaults
- Language: the language of the record, unless the person asks otherwise.
- No date in the record → today, marked as assumed.
- Long transcript → decisions and actions first, in full; the summary last.
