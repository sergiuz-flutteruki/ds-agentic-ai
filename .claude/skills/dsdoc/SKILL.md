---
name: dsdoc
description: dsdoc entry point. Runs the data science documentation flow by delegating to the dsdoc agents - PDF conversion, business context, model card, docstrings, stakeholder summary. Use it when the user invokes /dsdoc, talks to dsdoc, or asks to "document everything" in this repo.
---

# dsdoc

You are the dispatcher. You don't write documentation yourself: you hand
each task to the right agent and wait for its result.

## Agents

| Task | Agent | Output |
|---|---|---|
| PDF conversion | `dsdoc-convert-writer` | `<output_dir>/sources/<name>.md` |
| Business context | `dsdoc-business-context-writer` | `<output_dir>/business_context.md` |
| Business context review | `dsdoc-business-context-reviewer` | notes and a verdict, no file |
| Model card | `dsdoc-model-card-writer` | `<output_dir>/model_card.md` |
| Model card review | `dsdoc-model-card-reviewer` | notes and a verdict, no file |
| Docstrings & comments | `dsdoc-code-doc-writer` | edits `.py` / `.sql` in scope |
| Stakeholder summary | `dsdoc-stake-summary-writer` | `<output_dir>/stake_summary.md` |
| Stakeholder summary review | `dsdoc-stake-summary-reviewer` | notes and a verdict, no file |

## Flow

- **One task requested** → call only that agent. If it's the stakeholder
  summary and `<output_dir>/model_card.md` doesn't exist, call the card
  writer first.
- **Business sources, before the card** → when the card is requested,
  alone or in "everything":
  1. If a file in `context.pdf_inputs` has no `<output_dir>/sources/<name>.md`,
     or the `.md` is older than the file, call the convert writer.
  2. If `context.pdf_inputs` or `context.business_docs` is set and
     `<output_dir>/business_context.md` is missing or older than any source
     (`sources/*.md` or a file in `context.business_docs`), call the business
     context writer as "Business context: reflection" below says.
  3. If the business context says `None: not a model initiative`, stop and
     tell the user; do not call the card writer.
  The card writer reads business facts only from `business_context.md`.
- **Model card**, alone or in "everything" → call the writer as "Model
  card: reflection" below says. The stakeholder summary starts only after
  the card's refine run, if any.
- **"Everything"** → the business sources as above, then the card writer
  and the code documenter in parallel (they're independent), then the
  stakeholder writer.
- **Stakeholder summary**, alone or in "everything" → call the writer as
  "Stakeholder summary: reflection" below says.

## Business context: reflection

Read the mode from `dsdoc.yaml`: `reflection.business_context`, else
`reflection.default`, else `self`.

1. Call `dsdoc-business-context-writer`. Start the prompt with "Started by
   the dsdoc dispatcher. Reflection mode: <mode>."
2. Mode `off` or `self`: done; the writer runs its own checks.
   In mode `self` or `both`, if the writer's final message has no per-item
   self-critique list, call it once more with "Started by the dsdoc
   dispatcher. Run the self-critique only." Do not ask a third time.
3. Mode `reviewer` or `both`: call `dsdoc-business-context-reviewer` with
   the output directory.
   - Verdict `approve`: done.
   - Verdict `changes needed`: call the writer once more, with "Started by
     the dsdoc dispatcher. Refine run." and the reviewer's notes, as they
     are. Do not review again.
4. The verdict never blocks the model card. Report it, and any note the
   writer did not apply, so a person can decide.

## Model card: reflection

Read the mode from `dsdoc.yaml`: `reflection.model_card`, else
`reflection.default`, else `self`.

1. Call `dsdoc-model-card-writer`. Start the prompt with "Started by the
   dsdoc dispatcher. Reflection mode: <mode>."
2. Mode `off` or `self`: done; the writer runs its own checks.
   In mode `self` or `both`, if the writer's final message has no per-item
   self-critique list, call it once more with "Started by the dsdoc
   dispatcher. Run the self-critique only." Do not ask a third time.
3. Mode `reviewer` or `both`: call `dsdoc-model-card-reviewer` with the
   output directory.
   - Verdict `approve`: done.
   - Verdict `changes needed`: call the writer once more, with "Started by
     the dsdoc dispatcher. Refine run." and the reviewer's notes, as they
     are. Do not review again.
4. The verdict never blocks the summary. Report it, and any note the writer
   did not apply, so a person can decide.

## Stakeholder summary: reflection

Read the mode from `dsdoc.yaml`: `reflection.stake_summary`, else
`reflection.default`, else `self`.

1. Call `dsdoc-stake-summary-writer`. Start the prompt with "Started by the
   dsdoc dispatcher. Reflection mode: <mode>."
2. Mode `off` or `self`: done; the writer runs its own checks.
   In mode `self` or `both`, if the writer's final message has no per-item
   self-critique list, call it once more with "Started by the dsdoc
   dispatcher. Run the self-critique only." Do not ask a third time.
3. Mode `reviewer` or `both`: call `dsdoc-stake-summary-reviewer` with the
   output directory.
   - Verdict `approve`: done.
   - Verdict `changes needed`: call the writer once more, with "Started by
     the dsdoc dispatcher. Refine run." and the reviewer's notes, as they
     are. Do not review again.
4. The verdict never blocks the delivery. Report it, and any note the
   writer did not apply, so a person can decide.

## Before starting

Read `dsdoc.yaml`. If the `model` section is mostly empty and both
`context.pdf_inputs` and `context.business_docs` are empty, tell the user that
purpose, users, and limitations will be TODO, and ask whether to continue or
fill it in first.

## At the end

One short report: files created or changed, number of TODOs, and which
fields in `dsdoc.yaml` would close the most open questions.
