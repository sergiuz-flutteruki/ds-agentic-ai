---
name: dsdoc-stake-summary
description: dsdoc skill that turns the model card into a one-page, non-technical summary for stakeholders. Use it when the user asks dsdoc, or asks for a business summary, a document for management, or "explain the model in plain language".
context: fork
agent: dsdoc-stake-summary-writer
---

# dsdoc: generate stakeholder summary

Write `<output_dir>/stake_summary.md` (overwrite it if it exists) from
`<output_dir>/model_card.md` and, for exact metric values only, `dsdoc.yaml`.
You don't read the code, the notes or the canvas: the card already contains
what they say.

If `model_card.md` is missing, stop and tell the user to run
`dsdoc-model-card` first.

## What this document is

A plain-language explanation of **what was built, what it does, and how well
it works**. A manager who reads only this page should understand the model
and its results. The page stands on its own: it does not point to the model
card for the substance. The card's Business context says why the work
exists, in one or two sentences.

## dsdoc terms

- **Customers / users**: the people who receive the model's
  recommendations. They can appear in the training data and at inference.
- **Stakeholders / management**: the readers of `stake_summary.md`. One
  general summary serves all of them.

## dsdoc ground rules

- **Source priority.** The model card is the source of facts. `dsdoc.yaml`
  is used only for exact metric values; if a value differs from the card,
  use the yaml value and say so in "Still to be confirmed".
- **No code.** You work only from the model card and the config.
- **Never invent.** Anything not in those files is not written.

## Rules

- **Explain the results.** The summary must say how well the model works, in
  plain words. Use the metrics in `dsdoc.yaml` (or the model card, if the
  config has none). Give the main metric first, then the others.
- **Main metric.** Use `model.main_metric` from `dsdoc.yaml`. If it is not
  set, use the ranking metric closest to the success measure in the model card,
  and say in "Still to be confirmed" that the main metric has not
  been chosen by the owner.
- **Each metric, in plain words.** For every metric shown, give:
  - its name in plain words, not its code name;
  - its exact value, copied from `dsdoc.yaml` and never rounded;
  - one sentence on what it measures, taken from that metric's entry in the
    model card's "Metrics explained" section. Rewrite it for a reader with no
    technical background: keep the meaning, drop the jargon, and say what it
    means for the customers or the business. Each metric gets its own sentence.
    Never reuse a sentence from another metric, and do not write a grouped line
    such as "these all check X". Do not show a metric the card does not list.
    If an entry says "general definition", say so in the summary.
  Say whether higher is better only if the card's sentence says so.
- **Do not interpret beyond the numbers.** Say what a value measures. Do not
  say whether it is good or bad unless the model card says what a
  good value is. If the card gives no threshold, say so in "Still to be
  confirmed".
- **Baseline comparison.** If the model card has a baseline comparison, say
  in one plain sentence per main metric whether the model does better, worse,
  or the same as the baseline, with both exact values. Use the baseline's
  values from the model card, never estimate them.
- **Measure of success.** State the success measure from the model card,
  and say whether the results measure it. If a success measure is not
  measured by any result, say so plainly.
- **Problem: little.** At most 2 sentences from the card's Business context:
  the problem and what this model is expected to change. At most one
  programme figure, written as "the programme aims to…", exactly as the card
  writes it. Don't copy the hypothesis, brands, tribe, investment category,
  pending items, or undefined terms.
- **Describe the solution, not the code.** Say what the model predicts, for
  which customers, from which kinds of information, and what comes out.
  Group the information into 3-5 plain categories; never list columns.
- **No new facts.** Every claim must exist in the model card or `dsdoc.yaml`.
  Never present programme figures as what this model
  achieved.
- **Don't hide gaps.** If results are missing, write "To be completed".
- **Plain language.** Write only words a manager without a data or IT
  background would use in a business meeting. Replace any other term with
  plain words, or leave it out. Never copy a name the card writes as code
  (in backticks): columns, tables, functions, metric keys. Examples:

  | Don't write | Write instead |
  |---|---|
  | feature, column, variable | information, signal |
  | target, label | what the model predicts |
  | training set, holdout, train/test split | data used to build the model / data kept aside to check it |
  | algorithm names (XGBoost, ALS, regression...) | "the model" |
  | pipeline, inference, table, query | "each run", "the results" |
  | baseline | "the current approach" or "a simple comparison" (as the card describes it) |
  | ranking, top-k | ordering, "the best N" |

  Metric code names (AUC, NDCG, MAP, precision@k, recall@k, RMSE, F1...) are
  not written as the metric's name. Use the plain name first; a code name may
  appear once, in brackets, only if the card itself uses it as the metric's
  name. Acronyms and internal terms not defined in the card are omitted.
  "Information", "what the model predicts" and "score" are the preferred words.
- **Write for a general reader** with no technical background. There is one
  summary, not one per audience.
- **Variants.** If the model card has a Variants section, say once that the
  same model is built separately for each brand (or product) and name them.
  Give results per brand.
- **Output in one plain sentence, no steps.** Say what the model returns and
  what a reader can do with it. Do not describe how it is computed: no
  pipeline steps, no ranking procedure, no intermediate calculations.
- **Operational claims need a source.** Describe how results are used only if
  the model card states it. Do not add who makes the
  final decision.
- **Keep out-of-scope uses visible.** Say what the model is not for, from the
  model card.
- **"Still to be confirmed": at most 3 items**, the ones that change how far
  the results can be trusted or used. Business terms, one line each. When
  more than 3 apply (yaml value differs from the card, main metric not
  chosen, no threshold, success measure not measured, other gaps), keep them
  in that order and drop the rest.
- **Length: 400 words at most.** Cut detail before you cut a section.

## Check before you finish

After writing `stake_summary.md`, run with Bash:

`bash .claude/skills/dsdoc-stake-summary/check.sh <output_dir>/stake_summary.md <output_dir>/model_card.md`

It checks banned technical terms, code names copied from the card, and the
400-word limit. Fix the file and rerun until it prints `PASS`. A banned-term
hit that is part of a brand, product or card-defined metric name may stay,
as the rule on metric code names permits. Cut detail before cutting a
section.

Report in your final message any hit you kept on purpose, and why.

## Template

```markdown
# {What the model does, in 5-8 words}

## Summary
Two or three sentences: what the model does for which customers, why it
matters to the problem, and the headline result in plain words.

## How it works
Three bullets at most, in plain words: what it learns from, what it
predicts, and what it produces each run.

## Results
Main measure first, in one sentence with its exact value and what it means.
Then one bullet per other metric, in plain words, with its exact value. Say
which success measure the results do and do not cover.

## Where it is used
Two sentences: which customers receive the results, and how they reach
them. Then **Not intended for:** one line, from the model card.

## Still to be confirmed
Three items at most, business terms, one line each. Omit if there are none.
```
