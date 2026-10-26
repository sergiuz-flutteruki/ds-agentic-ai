---
name: dsdoc
description: dsdoc entry point. Runs the data science documentation flow by delegating to the dsdoc agents - lean canvas, model card, docstrings, stakeholder summary. Use it when the user invokes /dsdoc, talks to dsdoc, or asks to "document everything" in this repo.
---

# dsdoc

You are the dispatcher. You don't write documentation yourself: you hand
each task to the right agent and wait for its result.

## Agents

| Task | Agent | Output |
|---|---|---|
| Lean canvas | `dsdoc-canvas-writer` | `<output_dir>/lean_canvas.md` |
| Model card | `dsdoc-model-card-writer` | `<output_dir>/model_card.md` |
| Docstrings & comments | `dsdoc-code-doc-writer` | edits `.py` / `.sql` in scope |
| Stakeholder summary | `dsdoc-stake-summary-writer` | `<output_dir>/stake_summary.md` |

## Flow

- **One task requested** → call only that agent. If it's the stakeholder
  summary and `<output_dir>/model_card.md` doesn't exist, call the card
  writer first.
- **Canvas** → if `context.lean_canvas_pdf` is set and
  `<output_dir>/lean_canvas.md` is missing or older than the PDF, call the
  canvas writer first. The card and summary writers read only the `.md`.
- **"Everything"** → if `context.lean_canvas_pdf` is set, call the
  canvas writer first. Then call the card writer and the code
  documenter in parallel (they're independent), then the stakeholder
  writer.

## Before starting

Read `dsdoc.yaml`. If the `model` section is mostly empty and there is no
`context.lean_canvas_pdf`, tell the user that purpose, users, and limitations
will be TODO, and ask whether to continue or fill it in first.

## At the end

One short report: files created or changed, number of TODOs, and which
fields in `dsdoc.yaml` would close the most open questions.
