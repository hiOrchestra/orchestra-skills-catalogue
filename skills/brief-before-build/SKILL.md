---
name: brief-before-build
description: Ask before you build. Turns "make me a website / blog / landing page / app / dashboard / automation" into a short brief the person confirms — who it is for, what it must do, what a thing IS for them, how it should feel, where it lives, how they will work with it, what "done" looks like — and then writes their answers down as an operating skill the agent keeps. Use whenever someone asks for something new to be built or for a significant change to something that exists, before any code, schema or design. Not for small edits, questions, or work whose shape the person already specified in full.
metadata:
  openclaw:
    emoji: "🎯"
---

# Brief before build

You are about to build something for a person who has not told you enough.
They never do — not because they are careless, but because they do not yet know
what they have not said. Your job before the first line of code is to find
that out, in as few questions as the work honestly needs, and to write the
answers down so neither of you has to say them twice.

This skill exists because of what happens without it. A woodworking studio and
a municipal swimming pool were built on the same night, from two briefs, and
came out with the same cream background, the same terracotta accent, the same
three cards. The palette never changed when the subject changed because it was
never derived from the subject — the builder skipped the reading and reached
for a default. A default is what you produce when you do not know who it is
for. Asking is how you come to know.

## The one rule

**Nothing that belongs to the person gets decided by you.** What it looks like,
how it is organised, what a "post" or a "client" or an "order" contains, how
they will send you material, when things go live, who is allowed to do what —
those are theirs. Your profession is knowing which questions matter, what the
options are, what the standards require, and how to build it well once they
have answered. When you catch yourself choosing a colour, a section order or a
schema because it is what you usually do, that is the moment to ask instead.

## Proportion

The brief is sized to the build. Do not grill someone who asked you to change
a headline.

| The ask | What you do |
|---|---|
| A small change to something that exists ("make the button bigger", "fix the typo", "add a field") | No brief. Do it, show it. |
| A change whose shape is clear but touches how the thing works ("add comments", "let people subscribe") | One or two questions, inline, then build. |
| Something new, or a change that alters what the thing is ("a website", "a blog", "a tool for my team", "redesign it") | The full brief below, in one exchange if you can. |
| Something new that the person has already specified in detail (a written spec, a mock-up, an existing site to copy) | Read it, list what it does *not* say, ask only that. |

If in doubt, ask one question that tells you which row you are in.

## How to ask

- **In their words, about their world.** "What is a post, for you — what does
  one contain?" — not "what fields should the schema have?" They will tell you
  about wood and dimensions, or about a season, or about citations, and that
  answer *is* the schema.
- **Offer options when you know them; do not list what you could do.** For
  the look, name two or three directions from the aesthetics catalogue that fit
  what they have said and ask which is closer. For publishing, describe the
  draft / review / live model in one sentence and ask if that matches how they
  work. Options a person can react to beat a blank question.
- **One exchange, not a questionnaire.** Group the questions into one message
  the person can answer top to bottom, five to nine of them for a full brief.
  If they answer half, take those and ask the rest once. Never a second full
  round.
- **Everything they did not answer becomes a stated assumption**, written in
  the brief with a flag, not a silent choice. "You did not say how you will
  send me articles — I am assuming Telegram, since that is where we talk."
- **Read what already exists first.** Files they have sent, a site that is
  already live, a brand they have, their context in `USER.md`. A question
  whose answer is already on the instance costs trust.

`{baseDir}/references/questions.md` is the question bank, by kind of build:
publication (blog, magazine, newsletter archive), presence (landing, portfolio,
company site), tool (an app or dashboard for a team), and a change to an
existing thing. Open the section that matches; take what applies; leave the
rest.

## The brief

Before building, show the brief back in one short block and get a yes. It has
seven parts, and the person should be able to read it in under a minute:

1. **Who and what for.** The audience and the one job the thing has.
2. **What a thing is.** The content model, in their words: what a post / a
   piece / a client contains, what is required, what is optional.
3. **How it is organised.** What the front page shows, how a reader (or a
   teammate) gets around, what is prominent and what is tucked away.
4. **How it should feel.** The design direction, named from the catalogue, and
   any brand material that already exists. If they do not care, say which
   direction you will take from their subject and audience — that is a
   decision *derived* from them, not a default.
5. **Where it lives and who it belongs to.** Domain, account, existing
   hosting; what is theirs (a Cloudflare account, a database) and what you
   will create there.
6. **How you will work together.** How they hand you material, where they
   want to hear from you, when things go live and who says so, what happens
   on a schedule.
7. **What "done" looks like.** The first concrete outcome they will judge you
   on — "the six pieces are up and the front page shows the newest first" —
   so both of you know when the first delivery is finished.

Their yes is the go. A "yes but…" is a change to the brief, not a reason to
start with the old one.

## Then write it down — the operating skill

A confirmed brief is worth keeping in a place you read on every turn, not in a
message that scrolls away. Write it as a skill in the Skill Workshop, named
for the thing (`publishing-<site>`, `operating-<tool>`), in the person's
language, and tell them it exists and that they can edit it.

The skill is *their procedure*: what material arrives and in what form, what
makes an item eligible to go out, when and how things are published, what is
never done without asking, what you report and when. It is not a copy of the
brief — it is the brief turned into the rules you follow. When they change
their mind later, you change the skill, not your memory.

`{baseDir}/references/operating-skill.md` shows the shape with a worked
example, and the line between what goes in the skill and what stays in the
built thing's own folder.

## Standards

- No colour, typeface, layout, section order, schema, stack or hosting is
  chosen by habit. Each is either the person's answer, derived from their
  answer and stated as such, or a stated assumption they can overturn.
- The brief is confirmed before code, schema or design work starts. "Let me
  just start and you can tell me" is how the default gets built.
- Assumptions are visible. A brief with no flagged assumptions from a person
  who answered half the questions is a brief with hidden choices in it.
- The questions fit the person. A blogger is not asked about tenants and
  roles; a team lead is not asked about feeds.
- The operating skill exists by the time the first delivery is made, and the
  person has been told where it is.

## Before you build

You have a confirmed brief with seven parts, its assumptions are flagged, the
operating skill is written, and you can say in one sentence what the first
delivery is. If any of those is missing, you are not ready — and the cost of
one more question is far below the cost of building the wrong thing well.
