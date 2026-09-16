---
name: interview-guide
version: 0.1.0
description: >-
  Prepare a person to interview someone — an expert, a customer, a candidate, a
  witness — with a short brief on who they are, the questions that will get
  what the person needs, the order to ask them, and what to listen for. Use
  when the user says "I'm meeting X, what should I ask", "prepare questions
  for", "interview guide", "discovery call prep", "expert call", "user
  interview", "what do I need to know before I talk to". Not for conducting
  the interview (the person does that), and not for background research alone
  (research-brief).
metadata:
  openclaw:
    emoji: "🎤"
---
# Interview Guide — the questions that get what you came for

The person is going to talk to someone who knows something they need. This
skill prepares them: who the interviewee is and what they are likely to say
unprompted, the few questions worth the time, in an order that opens people up
before it asks for the hard thing, and what a good answer sounds like — so the
conversation is theirs, not a script.

## Related skills
- **research-brief** — background on the interviewee or the topic; this skill
  turns it into questions.
- **distill** — after the interview, the notes or transcript become the
  findings.
- **decision-brief** — when the interview feeds a choice, the questions test
  the criteria.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A conversation is scheduled and the person wants to get the most from it.
- **Do NOT use** to write a survey or a form; do not produce twenty questions
  when six would do; never suggest recording someone without telling them.

## Workflow
1. **What must the person leave with?** Ask: the decision or piece the
   interview feeds, the two or three things they do not know and cannot find
   out otherwise, how long they have.
2. **Know the interviewee.** With `web_search` / `web_fetch`: role, what they
   have said publicly on the topic, what they are likely proud of, what they
   might be guarded about. One paragraph. If they are private, say what you
   could not find rather than guessing.
3. **Write the questions** — 6–10, open, one thing each, in plain words. Order:
   an easy one they will enjoy answering; the ones that need context they will
   give in their own words; the hard or specific ones once trust is there; a
   closing "what should I have asked?".
4. **For each question, say what to listen for**: what a substantive answer
   contains, the follow-up if the answer is vague, the number or example to
   ask for.
5. **Flag what not to do**: leading questions, asking two things at once,
   filling silences, the topic that would make them close up early.
6. **Deliver** in the shape under Output, one page, saved to `orch-files`
   when they will bring it to the call.

## Standards
- Every question traces to something the person needs to leave with; a
  question that is only interesting is cut.
- Questions are open ("how did you decide…") unless a fact is needed
  ("how many…"); no yes/no questions except to confirm.
- Nothing in the guide assumes an answer. "Why did the launch fail?" becomes
  "how did the launch go, from where you sat?".
- Background is sourced; anything uncertain about the interviewee is marked.

## Output
- **Purpose** — what they need to leave with, in two lines.
- **Who you are talking to** — one paragraph, sourced.
- **Questions** — numbered, with the listen-for note under each.
- **If time is short** — the three to keep.
- **Avoid** — 2–4 lines.

## Defaults
- Duration unknown → plan for 30 minutes, eight questions, three marked as
  the core.
- Customer or user interview → past behaviour over hypotheticals ("the last
  time you…", never "would you…").
- Candidate interview → the same structure; the listen-for notes carry the
  criteria, and the guide says which questions are unlawful to ask where the
  person is (say to check locally).
