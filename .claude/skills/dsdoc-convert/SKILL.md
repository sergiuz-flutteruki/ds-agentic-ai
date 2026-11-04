---
name: dsdoc-canvas
description: dsdoc skill that converts a lean canvas (PDF, image, or Markdown, any template) into one normalized Markdown file that the other dsdoc skills read. Use it when the user asks dsdoc to convert, import, or normalize a lean canvas, or gives a canvas to use for the model card.
context: fork
agent: dsdoc-canvas-writer
---

# dsdoc: normalize a lean canvas

Convert the lean canvas in `context.lean_canvas_pdf` (in `dsdoc.yaml`)
into `<output_dir>/lean_canvas.md` (default `docs/lean_canvas.md`).
Overwrite it if it exists. If the user gives a canvas path directly, use
that path instead of the yaml. If neither is set, stop and ask for one.
The other dsdoc skills read the canvas only from that `.md`.

The canvas is a business document. You copy it into a fixed structure.
You don't summarise, interpret, or improve it.

## dsdoc ground rules

- **Source only.** Read only the canvas file. No code, no other canvases,
  not even other canvases from the same programme.
- **Verbatim.** Copy the text word for word. Fix only line breaks that the
  PDF broke in the middle of a sentence. Keep typos, acronyms, and £ figures
  exactly as written.
- **Never invent.** Leave a section empty (`—`) if the canvas has nothing
  for it. Never fill one section with text taken from another.

## Templates

The canvases don't share a template. Match fields **by meaning, not by
heading**:

| Normalized section | Headings seen so far |
|---|---|
| Problem | "What is the problem?", "What is the problem or opportunity?" |
| Proposed models | the "we propose" / "models are required" part of the problem |
| Programme impact | "How big is the problem?", "Estimated benefits / ROI" |
| Hypothesis | "What is your hypothesis?", "What is the hypothesis?" |
| Success criteria | "The success of the model will be measured by" |
| Next steps | "What are the next steps to validate?" |
| Validators | "Who will be needed to validate?" |
| Nature of work | "What is the nature of this work?", "Type of Initiative" |

Ignore the template's guidance text (the grey hints under the headings,
e.g. "Provide a high-level overview..."). It is not canvas content.

If a heading fits no section, put it under `## Other` with its original
heading. Never drop content.

## Steps

1. **Read the whole canvas.** For a PDF, read every page. The title slide
   gives the initiative name; the canvas is usually the next page.
2. **Name the template:** `M&G` (orange "ITERATION 1 - IDENTIFY" band,
   strategic pillar, ROI box), `Identify v2` ("Request to move to
   Validate", nature of work, validators), or `other`.
3. **Mark pending text.** Text in red, highlighted, in square brackets as
   a placeholder (e.g. `[Mike Robinson]`), or worded as still to do goes
   in `## Pending`, verbatim, with the section it came from. Keep it in
   its original section too, prefixed `[PENDING]`.
4. **Split the proposed models.** One bullet per model or cohort the
   canvas describes, with its name as written. If the canvas proposes
   no ML model (e.g. a tooling or process initiative), write
   `None: not a model initiative` and say so to the user. Such a canvas
   must not be used for a model card.
5. **List the undefined terms.** Acronyms and terms the canvas uses
   without defining them (e.g. `MPU`, `PPB`, `CPP`) go in
   `## Undefined terms`. Don't expand them yourself.
6. **Fill in the template below** and save it.

## Template

```markdown
# <Initiative name, as written>

| Field | Value |
|---|---|
| Source | `<canvas file name>` |
| Template | M&G / Identify v2 / other |
| Converted | <YYYY-MM-DD HH:MM, from `date`> |
| Stage / Iteration | <e.g. Identify, Iteration 1, or —> |
| Business lead / Tribe | <as written, or —> |
| Strategic pillar | <or —> |
| Customers / Brands | <or —> |
| Nature of work | <or —> |
| Investment category | <or —> |

## Problem
<verbatim>

## Proposed models
- **<model or cohort name>**: <verbatim description>

## Programme impact
<verbatim. All figures here are programme-level unless the canvas
explicitly ties them to one model.>

## Hypothesis
<verbatim>

## Success criteria
1. <verbatim>

## Next steps
- <verbatim>

## Validators
<verbatim, or —>

## Other
<headings that fit no section above, or —>

## Pending
- <verbatim text> (from: <section>, marked: red / highlighted / placeholder)

## Undefined terms
- `<term>`
```

## At the end

Report to the user: the output path, the template detected, the number
of proposed models with their names, and the pending and undefined items.

