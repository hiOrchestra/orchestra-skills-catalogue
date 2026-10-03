---
name: notion-workspace
version: 0.1.0
description: >-
  Work in the person's Notion workspace through their connected account —
  find pages and databases, read them, answer questions from them, and
  create pages, add database rows, append content or reorganise a section
  only after the person approves the exact change; and design a structure
  people can find things in (a wiki, a projects database, meeting notes, a
  CRM-lite) when they ask. Never deletes or archives without an explicit yes.
  Use when the user says "Notion", "in our wiki", "add this to Notion",
  "find the page about", "organise our Notion", "Notion database". Needs
  Notion connected.
metadata:
  openclaw:
    emoji: "🗒️"
  orchestra:
    requires:
      integrations:
        - notion
---
# Notion Workspace — find anything, add carefully, keep it findable

A Notion workspace is only as useful as it is findable. This skill searches
and reads it to answer questions, adds to it where the person wants, and —
when asked — proposes a structure that stops the sprawl. It changes nothing
without an approved preview, and never deletes.

## Related skills
- **meeting-notes** — notes written up, then filed in Notion.
- **policy-handbook** / **knowledge-base** — content that often lives in a
  Notion wiki.
- **plan-work** — a project plan as a Notion database.
- **orch-composio** — the tool every call goes through.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Questions answered from Notion; adding pages, rows and content; a
  reorganisation the person asked for.
- **Do NOT use** to delete or archive pages, change sharing or permissions,
  or restructure someone else's area without their owner's say-so.

## Workflow
1. **Check the connection**: `orch-composio connections`; not connected →
   say so and stop. The agent only sees pages the Notion integration was
   given access to — if something is missing, say how to share it.
2. **Confirm the schema before first use** (`orch-composio schema --slug
   <SLUG>`). Core actions: `NOTION_SEARCH_NOTION_PAGE`,
   `NOTION_RETRIEVE_PAGE`, `NOTION_GET_PAGE_MARKDOWN`,
   `NOTION_FETCH_DATABASE`, `NOTION_QUERY_DATABASE_WITH_FILTER`,
   `NOTION_FETCH_ROW`; writes `NOTION_CREATE_NOTION_PAGE`,
   `NOTION_ADD_PAGE_CONTENT`, `NOTION_INSERT_ROW_DATABASE`,
   `NOTION_UPDATE_ROW_DATABASE`, `NOTION_UPDATE_PAGE`.
3. **Answer from the workspace**, quoting the page and linking it.
4. **Writes are previews first**: where it goes (parent page or database),
   the title, the properties, the content; wait for the yes; create exactly
   that; read it back; log it (`orch-database`, table `notion_changes`).
5. **A structure, when asked**: map what exists (top-level pages,
   databases, duplicates, orphans), propose a layout — a few top-level
   areas, databases instead of loose pages for anything repeated, one
   template per recurring document — and a migration in small steps, each
   approved.

## Standards
- Nothing is deleted or archived by the agent; moving a page is a proposal.
- Properties of a database are respected; a new property is a proposal.
- Content written into Notion is the person's language and voice.
- What is read in Notion stays in the conversation.

## Output
Answers with page links. Writes: the preview, then "done" with the link.
Reorganisation: current map · proposed structure · step-by-step plan.

## Defaults
- Where to file → the database or page the procedure names; otherwise ask.
- Meeting notes → one row per meeting in a "Meetings" database if one exists.
