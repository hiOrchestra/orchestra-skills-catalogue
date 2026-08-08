---
name: build-data-view
version: 0.1.0
description: >-
  Build a screen people work *in*, not just look at — a list of records with
  filters, sorting, paging and status changes that behaves the way users expect.
  Use when the user says "build a screen to manage X", "a table of our orders /
  leads / tickets", "I need to filter and update these", "a view of the database",
  "admin screen", "make this list usable", or asks to add filters, search, paging
  or a status toggle to an existing view. Not for choosing which KPIs to show
  (build-dashboard) and not for a static document (build-report).
triggers:
  - build a screen to manage
  - screen to manage our data
  - table of our records
  - list of orders
  - list of leads
  - admin screen
  - manage this data
  - view of the database
  - add filters to this
  - make this list usable
  - let me update the status
  - I need to filter and sort this
metadata:
  openclaw:
    emoji: "🗂️"
requires:
  bins: []
  env: []
  config: []
---

# Build Data View — records people can find, read and change

Build a working surface over a set of records: a list someone opens every day to
find a row, understand it, and act on it. The bar is not "the data appears on
screen" — it is that a person can locate one record among thousands, trust what
they read, change it without fear, and come back tomorrow to the same view they
left. Most of the rules below exist because the alternative silently costs the
user a click, a scroll, or a mistake, every single time.

## Related skills
- **build-dashboard** — when the ask is *which numbers matter* (KPIs and charts
  that answer a question), not a list people operate on. A dashboard is read; a
  data view is worked in. They often ship together: dashboard on top, this below.
- **explore-dataset** — when nobody yet knows what the data says. Explore first;
  you cannot choose columns for a table you do not understand.
- **analyze-data-quality** — when the records may not be trustworthy (gaps,
  dupes, stale rows). A polished table launders bad data into something people
  believe. Run the trust check first and carry any caveat onto the screen.
- **build-report** — when the deliverable is a static document, not a surface
  someone returns to.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Someone needs to **operate on records**: find them, filter them, read one in
  detail, change its state.
- Triggers: "a screen to manage our X", "table of our orders/leads/tickets",
  "let me filter and update these", "admin view", "add search to this list".
- **Do NOT use** when a single number or one chart answers the ask — just answer.
  Do not use it to pick metrics (**build-dashboard**) or to explore unknown data
  (**explore-dataset**).

## Workflow
1. **Name the job and the row.** Who opens this, how often, and what they do
   here. Then say in one sentence what a single row *is* ("one order", "one
   lead"). Everything below follows from that sentence — if it is fuzzy, the
   screen will be too.
2. **Load the records.** `orch-database` for tenant tables, `orch-files` for an
   uploaded CSV. Learn the real shape: row count, the field that identifies a
   row, which fields are states, which are numbers, which are dates.
3. **Choose the columns.** Identifier leftmost — the thing that tells the user
   *which row am I looking at*. Then the field they compare most across rows
   (usually status or date). Numbers grouped on the right. Actions last.
   Everything else is a detail view, not a column. Six to eight columns is a
   working table; fifteen is a spreadsheet nobody scans.
4. **Give it a header that orients.** A plain-language title naming the records,
   and the count of what is currently shown ("Orders — 1,204"). If a few
   top-line numbers genuinely drive the work, put a small KPI row above the
   table (see **build-dashboard** for choosing them) — and make each number
   reflect the active filters, or it will contradict the table underneath.
5. **Make it findable.** A search box, always visible, never hidden behind an
   icon, with a placeholder naming what it searches. Filters matched to the data
   type: single-select for one state, multi-select for many, a range for numbers,
   a date picker with presets for dates. Show the active filters as removable
   chips with a "Clear all", and show the resulting count ("Showing 23 of 1,204").
6. **Make it navigable.** Every column header sorts, with a visible arrow on the
   active one. Default the sort to what people actually want first — usually
   newest. Page the results (not infinite scroll — people need to come back to
   where they were), with a page-size control and the current range spelled out.
   **Sort, filters and page must survive navigation**: encode them in the view's
   state/URL so opening a record and coming back does not reset the work.
7. **Design the three empty screens.** Every data view has four states, and three
   of them get forgotten: *loading* (a skeleton of the table, never a blank
   page — a blank page reads as "no results"), *no records at all* (explain what
   this screen will hold and how the first one gets here), *no results for these
   filters* (say so and offer "Clear all filters"), and *error* (what failed and
   what to do — never a bare spinner that never resolves).
8. **Let them change state safely.** Simple changes (a status, a flag) happen
   inline on the row. Complex edits open a detail panel or page. Then: name the
   record in every confirmation ("Archive 'Order #1042'?"), never just "Are you
   sure?"; show the new state immediately and reconcile if the write fails;
   offer undo for anything destructive; prefer archiving over deleting. For a
   bulk action, always show the exact count, and say plainly whether "select all"
   means this page or all 1,204 results.
9. **Build it on `orch-canvas`.** One component per job, reused: the same table,
   the same filter bar, the same confirmation dialog everywhere. A second table
   built differently is a second thing the user has to learn.
10. **Walk it once as the user.** Find a specific record. Filter, open it, come
    back. Change a status. Land on it with zero records. If any of those needs an
    explanation, fix the screen, not the explanation.

## Standards
- Numbers right-aligned, text left-aligned, dates in one consistent format. Right
  alignment is what lets the eye compare 1,234 against 12,345 without counting.
- Status is a labeled badge with a consistent colour per state across every
  screen — never a bare colour dot, which is unreadable to a colourblind user
  and meaningless to a new one.
- Nothing is silently hidden: if columns overflow, they scroll and say so; if a
  filter is on, it is visible as a chip.
- Every count on screen agrees with every other count on screen.
- The data window and source are stated, along with any caveat from the trust
  check — the same rule as a dashboard.
- Destructive actions are never adjacent to frequent ones.
- Actions the user's role cannot perform are hidden or disabled with a reason —
  never present and then failing.

## Anti-patterns
Treat these as bugs, not polish. They are the ones that get shipped by default:
- **Blank table while loading** — indistinguishable from "no results".
- **Filters that reset** when the user opens a record and comes back.
- **Delete without naming the record**, or with no undo.
- **Search behind an icon**, or search that only matches the exact full string.
- **A count that ignores the filters** — the header says 1,204, the table shows 23.
- **Ambiguous "select all"** — this page, or all results? Say which.
- **Inconsistent patterns** — create in a modal here, a full page there.
- **An unsortable, unfilterable table** of more than ~20 rows.
- **No empty state** — a new user's first impression is a blank rectangle.

## Output
- Build on `orch-canvas` and share the link. Lead the reply with what the screen
  lets someone do, the columns you chose and why, the filters available, and the
  data window and source.
- Call out anything you deliberately left out and what would change it (e.g. "no
  bulk actions yet — add them when someone needs to update more than a few rows
  at a time").
- If a static list is genuinely what was wanted, hand it to **build-report**.

## Defaults
- Unstated audience → the person who owns the records and the decision they make
  most often. State the assumption and proceed.
- Default sort: newest first. Default page size: 25.
- Under ~20 rows, drop the paging and the filters — a short list needs neither.
- When torn between more columns and a scannable table, choose scannable: extra
  fields belong in the detail view.
- Prefer archive over delete unless the user explicitly asks for permanent removal.
