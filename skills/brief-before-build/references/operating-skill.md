# The operating skill — the brief, turned into your rules

Once the brief is confirmed, write it down as a skill you keep. Not the brief
itself — the *procedure* it implies: what arrives, what makes it eligible,
what you do with it, what you never do, what you report. You read your skills
on every turn, so a rule written here is a rule you will actually follow in
three months, after the conversation that set it has scrolled out of reach.

## Where it lives

- **In the Skill Workshop**, as a skill of this instance, named for the thing:
  `publishing-<site>`, `operating-<tool>`, `running-<name>`. Versioned, so a
  change of mind is a new version and the old one is still there.
- **In the person's language.** It is theirs to read and edit; tell them it
  exists and that editing it is how they change how you work.
- **Never in `SOUL.md` or `AGENTS.md`** — those are overwritten by the
  platform. And never only in memory: memory is recall, not procedure.

## What goes in it, and what does not

| In the operating skill | Not here — it lives with the built thing |
|---|---|
| The material you expect and how it arrives (a `.docx` and a `.png` per article, a calendar file, an email to an address) | Worker source, schema, the deploy record (those sit in `orchestra/sites/<site>/`) |
| The eligibility rule — what must be true before something goes out | Secrets, tokens, database ids |
| When and how things are published (fixed hour, the person's yes, a status in a spreadsheet) | The design direction (that is in `DESIGN.md` next to the site) |
| Protections — what is never done without asking | Anything that is true of every site (that is the profession's skills, not this one) |
| What you report, to whom, where, and when | |
| Facts about this build that a future turn needs: the site's name, the domain, where the files are | |

## The shape

```markdown
---
name: publishing-<site>
description: How <person> and I publish <site>: what they send me, what makes a piece ready, when it goes live, what I never do without asking, what I report.
---

# Publishing <site>

## What arrives, and where
- One document per piece, named with its code (`AC_06_…`). A photo with the same code. The editorial calendar (a spreadsheet) with a row per piece: code, date, section, title, status.
- They come by Telegram; they land in Files.

## When a piece is ready
All three must agree: the document exists, the photo with the same code exists, and the calendar row has a valid date and the status "Ready". A row without its document or photo waits and does not hold up the others. Nothing is inferred or filled in.

## Publishing
- Load the piece and photo as *scheduled*, never as published-now.
- Visibility at 08:00 local on the calendar date. Before that hour it is not on the front page, in the archive, in the feed or in the sitemap.
- The front page shows the six newest public pieces, newest first. The seventh is not deleted; it lives in the archive and its section.

## Never without asking
- Publish anything not in the calendar as "Ready".
- Delete a piece to make room.
- Change the front page's organisation.

## Before any change to the site's code or data
Back up the database first. Verify on a preview before it is public.

## What I report
After each batch: what was validated, what was scheduled (code, title, section, date), and what is pending and why. Every day at 17:00: comments and contact messages. Every Sunday at 22:00: what is due next.

## Facts
Site: <name>. Domain: <domain>. Files: `orchestra/sites/<site>/`.
```

This is the shape of a real one, running for a real publisher. Yours will
differ in every line — that is the point. A tool for a team has "what a
request contains" and "who may approve" where this one has codes and hours.

## When the brief changes

They will change their mind — a new section, a different hour, comments on
after all. Change the skill, tell them the version moved, and carry on. If a
change contradicts a protection they set earlier, say so before you apply it.
