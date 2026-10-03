---
name: knowledge-base
version: 0.1.0
description: >-
  Build and keep the one set of answers support works from — what the product
  does, how to do things, policies (refunds, billing, shipping), known issues
  and their workarounds — written from the documents, FAQs and past replies
  the business already has, one article per question, each with its source
  and the date it was last confirmed; and grow it from every new question.
  Use when the user says "knowledge base", "help center", "FAQ", "support
  docs", "write the answer down", "add this to the docs", "what do we tell
  customers about". Not for drafting a reply to a customer (support-reply).
metadata:
  openclaw:
    emoji: "📚"
---
# Knowledge Base — every answer written once, sourced, and kept current

Support is only as good as what it can say with confidence. This skill turns
what the business already knows — scattered across docs, FAQs, policies and
the replies people have sent before — into one set of short articles, each
answering one question, each saying where the answer came from and when it
was last true. Every reply drafted later stands on it.

## Related skills
- **support-reply** — answers a customer from these articles.
- **distill** — compresses a long policy or manual into an article.
- **voice-guide** — how the articles and the replies should sound.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Starting support, or tidying answers that live in people's heads.
- A question was answered that the base did not cover — add it.
- **Do NOT use** to invent a policy. If the documents do not say what the
  refund window is, the article says "unknown — ask {owner}", and you ask.

## Workflow
1. **Collect the sources.** Ask for what exists: the help center or FAQ URL
   (`web_fetch`), product docs, policy pages, terms, a sample of past
   replies (forwarded emails or an export), the questions customers ask most.
2. **List the questions** customers actually ask, from the replies and the
   inbox first and the docs second; merge duplicates phrased differently.
3. **One article per question.** Title = the question in the customer's
   words. Body = the answer in the first two lines, then steps or detail.
   Footer = source (document, page, or "confirmed by {person}, {date}") and
   last confirmed date. Mark anything the sources contradict.
4. **Store it** in the instance database (`orch-database`, table
   `kb_articles`: id, question, answer, steps, tags, source, owner,
   confirmed_at, status (draft / live / stale), audience (customer /
   internal)). Create it on first use and say so. Long articles also go to
   `orch-files`.
5. **Review with the person.** New and changed articles go to them as a
   short list for a yes before they are `live`. Internal notes (workarounds,
   who to escalate to) are marked internal and never quoted to a customer.
6. **Keep it current.** When a reply needs an answer the base lacks, draft
   the article from the person's answer. When a product or policy change is
   mentioned, mark the affected articles `stale` and ask.

## Standards
- One question, one article. An article that answers three questions is
  three articles.
- Every article has a source. An answer with no source is a draft.
- Policies (money, data, legal, safety) are quoted from the policy, not
  paraphrased into something softer or harder.
- Nothing internal leaks into a customer-facing article: names of staff,
  internal tools, workarounds marked internal.

## Output
- On build: the list of articles created — question, status, source — and
  the questions the sources could not answer, for the person.
- On update: what changed, in one line per article.

## Defaults
- No sources sent → start from the public website and the five questions the
  person says they get most.
- Contradicting sources → the newest policy page wins; flag both.
- Articles older than 90 days without confirmation → listed as due for a
  check in the weekly support summary.
