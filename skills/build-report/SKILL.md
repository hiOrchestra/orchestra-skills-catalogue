---
name: build-report
version: 0.1.0
description: >-
  Turn findings, analysis, or data you already have into a polished, well-structured
  deliverable document — a report, DOCX, PDF, or slide deck — built with orch-docs.
  Use when the user says "write up a report", "make a PDF", "turn this into a deck",
  "put together a document", "format this into a report", or "create a presentation"
  from material that already exists. Not for gathering the findings themselves.
triggers:
  - write up a report
  - turn this into a report
  - make a PDF
  - make a deck
  - build a presentation
  - put together a document
  - format this into a report
  - create a slide deck
  - polished document
metadata:
  openclaw:
    emoji: "📄"
requires:
  bins: []
  env: []
  config: []
---

# Build Report — findings → polished deliverable document

Take material that already exists — research, analysis, a dataset's key findings —
and shape it into a real document a person would be glad to receive: a report, a
DOCX/PDF, or a slide deck. The bar is a clean structure, a clear takeaway up front,
sources and figures where they belong, and an actual file delivered — not just text
in the chat.

## Related skills
- **research-brief** — this skill formats findings; it does not gather them. If the
  facts don't exist yet, run **research-brief** first, then hand its output here.
- **explore-dataset** — when the raw material is a dataset that hasn't been analyzed,
  do the analysis with **explore-dataset** first; build-report renders the results.
- **distill** — when the job is to *compress* long source material into a tight
  summary (no document, no formatting), use **distill** instead.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- The user has findings/data/notes and wants a *finished document* out of them.
- Triggers: "write up…", "make a PDF/deck", "turn this into a report", "format this
  into a document", "put together a presentation".
- **Do NOT use** for gathering the findings (research-brief / explore-dataset), for
  a quick inline answer that needs no file, or for compressing text (distill).

## Workflow
1. **Confirm the brief.** Pin down three things that change everything downstream:
   **audience** (execs vs. practitioners), **format** (report / DOCX / PDF / deck),
   and **length/depth**. If unstated, state a sensible default (see Defaults) and
   proceed — don't stall on questions.
2. **Assemble the inputs.** Gather the source material: prior findings, an uploaded
   CSV or doc read via `orch-files`, or a query against `orch-database`. Confirm you
   have everything the document needs before structuring — a report is only as good
   as its inputs.
3. **Outline before you write.** Sketch the structure: executive summary → thematic
   sections → appendix/sources. Lead with the bottom line so a busy reader gets the
   answer in the first paragraph or slide. For a deck, one idea per slide.
4. **Draft the content** section by section against the outline. Keep each section to
   its point; move supporting detail, methodology, and raw tables to an appendix so
   the spine stays readable.
5. **Add figures and sources.** Pull in charts or images (`orch-img` for generated
   visuals) where a picture beats a paragraph, and carry through the citations from
   the source material — a formatted document must not silently drop provenance.
6. **Produce the actual file with `orch-docs`.** Generate the DOCX / PDF / PPTX. This
   is the deliverable; the point of the skill is a real document, not chat text.
7. **Deliver the file** and post a short summary pointing at it (see Output).

## Standards
- **Takeaway first.** Every report opens with an executive summary; every deck opens
  with the headline. Never bury the conclusion.
- **Faithful to the inputs.** Formatting reshapes findings — it never invents them.
  Don't add claims, numbers, or conclusions the source material doesn't support.
- **Sources survive the transfer.** Citations, dates, and figure captions carry from
  the findings into the document. A polished look must not launder away provenance.
- **Structure matches the format.** Prose and nested sections for a report; short
  parallel bullets and one idea per slide for a deck. Don't paste an essay onto slides.
- **The output is a file.** If you only produced text in the chat, the job isn't done.

## Output
- Produce a real document via `orch-docs` in the requested format (default below),
  then save/deliver it with `orch-files` and post a 2–3 line summary: what it is, its
  structure, and the filename/link.
- Only answer inline (no file) if the user explicitly wants a preview or just the
  outline before committing to the full build.
- Match depth to the ask: a one-page brief and a 20-page report are both valid — the
  brief is not a failed report.

## Defaults
- Format unstated → a clean **PDF report** with an executive summary; switch to a
  **deck** only if the audience or phrasing ("present", "slides") calls for it.
- Audience unstated → assume a decision-maker who wants the answer fast, detail on demand.
- Length unstated → as short as fully covers the material; push depth into an appendix.
- Missing inputs → say what's needed and, if it's research or analysis, point to
  **research-brief** / **explore-dataset** rather than fabricating to fill the gap.
