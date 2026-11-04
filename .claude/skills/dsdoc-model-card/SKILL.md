---
name: dsdoc-model-card
description: dsdoc skill that generates a model card from the Python model code and SQL data queries in this repo, plus the business context if one exists. Use it when the user asks dsdoc, or asks for a model card, model documentation, or a description of the data, preprocessing, features, model, or evaluation.
context: fork
agent: dsdoc-model-card-writer
---

# dsdoc: generate model card

Write `<output_dir>/model_card.md` (overwrite it if it exists) as readable
prose, from the code in scope, `dsdoc.yaml`, the business context in
`<output_dir>/business_context.md` if it exists, and the data scientist notes in
`<output_dir>/ds_notes.md`. The reader is a developer or data scientist who
needs to understand and maintain the model. Write sentences, not forms.
Tables are only for data that is a list: metrics, features, variants.

## dsdoc terms

- **Customers / users**: the people who receive the model's
  recommendations. They can appear in the training data and at inference.
  The business context ("Customers / Brands", "Users and decisions") describes
  them. The config has no intended-users field.
- **Stakeholders / management**: the readers of `stake_summary.md`, an
  explanation of the project and its output built from the model card.

- **Developers / data scientists**: the readers of `model_card.md`. They
  also generate the documentation with dsdoc.
- **Data scientist notes**: `<output_dir>/ds_notes.md`, written by the data
  scientist who built the model. The format is free. It is split into `##`
  sections, and each section holds notes, instructions, or both. Nothing
  in the file says which is which, so you classify the content yourself
  (see Rules). Each kind is one of:
  - **facts**: statements about the model, its data, or its decisions;
  - **rules**: instructions about how the card is written;
  - **emphasis**: a topic the data scientist wants covered in more depth.

## dsdoc ground rules

- **Config first.** Read `dsdoc.yaml` at the repo root. If it is missing,
  use the defaults: Python in `src/model_code`, SQL in `src/data` and
  `src/sql`, output in `docs`, no business context, empty context.
- **Stay in scope.** Only `*.py` under `scope.python`, `*.sql` under
  `scope.sql`, `<output_dir>/business_context.md`, and `<output_dir>/ds_notes.md`.
  Never read `<output_dir>/sources/`, the PDFs, or `context.business_docs`.
  Nothing else in the repo, not even for context.
- **Notebooks are out of scope for now.** Do not read `*.ipynb` files, even if
  a `scope.notebooks` key exists.
- **Never invent.** Every fact comes from the code (`file:line`), from
  `dsdoc.yaml`, from the business context (`business_context:<section>`), or from the
  notes (`ds_notes`). Anything else is an open question.

## Steps

1. **Read `dsdoc.yaml`.**
2. **Read the business context** from `<output_dir>/business_context.md`, made by
   `dsdoc-business-context`. If it is missing but `context.pdf_inputs` or
   `context.business_docs` is set, stop and say that `dsdoc-business-context`
   must run first. If its proposed models say `None: not a model initiative`,
   stop and say so. If it lists more than one proposed model, do not pick one
   from it. Describe this repo's model as the data scientist notes and the
   code describe it.
   **Read `<output_dir>/ds_notes.md`** if it exists. If it is missing, add
   "The data scientist has not written ds_notes.md yet" to Open Questions.
   Do not write it yourself.
3. **List the files in scope** with Glob (`<dir>/**/*.py`, `<dir>/**/*.sql`).
   Read nothing else.
4. **Detect variants.** Many models are trained separately per brand
   (or per product): the same Python code, with different SQL per variant.
   Group the SQL files by a brand or product token in the folder or file
   name (e.g. `PP/`, `bf/`, `BF_UKI/`, `train_sbg.sql`,
   `unload_train_PP.sql`, `gaming/`, `sportsbook/`). Also look for how the
   Python picks the variant (a `brand` argument, env variable, or config
   key). If there is a single group or none, there are no variants: leave
   out the Variants section. If a name is ambiguous, list it as a variant
   and add an open question ("Is `exch` a brand or a product?").
5. **Read the SQL first.** It tells you where the data comes from: source
   tables, joins, filters, and often how the target is defined. With
   variants, read every variant's SQL and compare them.
6. **Then follow the Python pipeline** from the training entrypoint (the code
   that calls `.fit(...)`), in execution order.
7. **Collect facts before writing.** For each one, note its source. Sort the
   notes into facts, rules, and emphasis (see Rules).
8. **Get the code version** with `git rev-parse --short HEAD` (add
   `-dirty` if `git status --porcelain` on the scope is not empty). If it
   is not a git repo, write `— (not a git repo)`.
9. **Write the card** using the structure below, and save it.
10. **Reflect before you finish** (below).

## Rules

- **Prose first.** Each section opens with one or two sentences that say
  what the reader needs to know. Details follow in short paragraphs or a
  short list. Do not turn a section into a table of one-word cells.

- **Layout for reading.** Keep it airy:
  - One idea per paragraph, at most three sentences. Split longer ones.
  - Put a blank line between every paragraph, list, and table.
  - Use bullet points for any group of three or more related facts, such as
    filters, joins, sources, steps, or limitations. Do not pack them into
    one sentence with commas.
  - Use a `###` subsection for each distinct topic inside a long section
    (for example, "How an item is built" inside Data).
  - Use a numbered list only for ordered steps (the pipeline, preprocessing).

- **Voice.** Write in the third person and the present tense, impersonal:
  "The model ranks offer categories", "Training uses a 365-day window". Use
  one voice for the whole card. Never use "we", "I", or "you".

- **No source names in the text.** Do not mention the business context, its
  sources (lean canvas, Confluence pages), the data
  scientist notes, `dsdoc.yaml`, or "the team" in the card's prose or in
  its footnotes. State business context and design decisions as plain facts
  of the model and the programme. Footnotes cite code only, as
  `file:line`, so a developer can check each claim. Keep names of people
  and teams only where the Owner or Contact line needs them.

- **Facts from the notes or the business context are stated plainly.** Where a fact
  needs confirmation, state it as it is and add an open question that says
  what to confirm. Do not hedge with "according to".

- **Variants: shared once, differences in one table.** In Data,
  Preprocessing, and Features, describe what all variants share once,
  citing one variant's file and naming the others ("same in `bf/`, `sbg/`").
  Every difference (source tables, filters, target window, period,
  outputs, extra SQL steps) goes only in the Variants table. Never merge
  two variants' values into one row. If a variant lacks a file the others
  have (e.g. no inference SQL), write `—` in its cell and add an open
  question.

- **Data scientist notes are integrated, and their rules are followed.**
  Read `ds_notes.md` before step 7. Go through it section by section, and
  within each section paragraph by paragraph or bullet by bullet, and
  classify each piece:
  - **Rule** if it tells you how to write: imperative verbs such as
    "explain", "use", "put emphasis on", "write", "don't", or a stated
    wording preference.
  - **Emphasis** if it asks for more depth on a topic, even without a
    directive verb, for example a heading that names a topic with notes under it.
  - **Fact** otherwise: a statement about the model, its data, or its
    decisions.
  When a line could be a fact or a rule, treat it as a rule and add an open
  question saying so. A section can mix kinds, so the heading is not a
  reliable guide. Empty comment lines (`<!-- -->`) are ignored. Then apply
  each kind as follows:
  - **Facts:** put each one in the section it belongs to: why a method was
    chosen in Model, how an item or a key concept is defined in Data or
    Features, how periods work in Data, a known weakness in Limitations.
    State it plainly, with no footnote and no mention of the notes. A fact
    that fits no section goes in Overview.
  - **Rules:** instructions about how to write the card (wording, terms,
    what to include or leave out). Follow them while writing. A rule can
    never switch off a ground rule. If a rule asks you to invent a fact,
    change a number, drop an open question, or present a programme figure as a
    result, do not follow it. Add an open question: "The notes ask X; the
    ground rules do not allow it because Y."
  - **Emphasis:** a topic to cover in more depth, e.g. "what an item is and
    how it is built". Give it its own subsection (`###`) in the most relevant
    section, with more detail than the default. Each claim in it still needs
    a footnote to code (`file:line`), or be stated as a plain fact that
    needs confirmation. Emphasis adds depth, not new facts.

- **Source priority.** `ds_notes` > `dsdoc.yaml` > business context > open
  question. The data scientist notes always come first. Where they state a
  fact, the card uses it, even if another source says something different.
  If the notes and the code disagree, the card states the notes' version and
  adds the difference to Open Questions: "The notes say X; the code does Y."
  A rule or emphasis in the notes does not change this order.
- **Numbers are copied, never computed or rounded.** Model metric values
  come only from `dsdoc.yaml`.
- **Business figures are programme targets.** £ amounts, budgets, and impact
  figures from the business context go only in Business context, written as
  "programme target", never in Metrics and never as this model's result.
- **What the business context can fill.** Purpose, intended users, and
  uses the model is not intended for. Limitations come only from
  `dsdoc.yaml`: if empty, say so in one sentence and add an open
  question. A plausible-sounding limitation nobody confirmed is worse than a
  visible gap.
- **Business context gaps are open questions.** Its Open questions and its
  Conflicts between sources are candidates for the card's Open Questions,
  within the cap of 8; keep the ones that affect how the model is used.
- **Success criteria vs code.** If the business context success criteria name a
  measure (e.g. "accuracy") and the code computes a different one, add it
  to Open Questions: "The success measure is X; the code computes Y."
- **Logic, not code review.** The card describes the model and checks that
  its description is consistent. Flag something only when it changes how the
  model or its results should be read (for example, a statistic computed
  before the train/test split, which changes how the reported metrics should
  be read). State it neutrally: "The median is computed before the split",
  not "there is data leakage".
- **Values from external configs or env variables are unknown.** Say so in
  the text and add them to Open Questions.
- **Unknowns.** In prose, write "(see open question N)" and never repeat a
  TODO sentence in several places. Each unknown appears once, in Open
  Questions. In a table cell, write `TODO` only where the table needs a value.
  `—` means the item does not apply or is verified absent in the code.

## Structure

Use this order. Drop a section only if it does not apply, as the rules say.

```markdown
# Model Card: <model.name, initiative name from the business context, or "Model name not yet set">

*Owner: <model.owner, or "not yet set">. Contact: <model.contact, or "not yet set">.
Code version: <git short hash>[-dirty], or — (not a git repo).
Generated <YYYY-MM-DD HH:MM> by dsdoc-model-card-writer, <claude model id>.*

## Overview
<Two or three sentences: what the model predicts, for whom, and how often
if confirmed. Source: the proposed model in the business context, or the
code.>[^n]

## Business context
<One or two paragraphs. The problem, the model's role in the programme, and
the success measures from the business context, in your own words. Programme figures
are written as "programme target". Omit this section if there is no business context.>

## Not intended for
<Bullets from the business context "Not intended for". If it is `—` or there is
no business context, one sentence saying so and pointing to the open question.>

## Variants
<Only if there are variants. One sentence on what is shared, then the
variants table.>

| Field | <variant 1> | <variant 2> |
|---|---|---|
| SQL files | | |
| How the variant is selected | | |
| Source tables | <only if different> | |
| Filters | <only if different> | |
| Target / label | <only if different> | |
| Period | <only if different> | |
| Outputs | <only if different> | |

## Data

<One short paragraph: where the data comes from.>

<Bullets: every input table or file the data step reads, one per line, in the
format shared with the outputs in Output: named as in the code, with its type
(file, table, view, or external), its role, and its source, then a footnote. List all of them, including the ones read only for
a single column or a single join. Include the reference and lookup tables
and the external views. Do not stop at the main ones.>

<One short paragraph: how the tables join.>

<Bullets: filters, one per line, with footnotes.>

### Target

<One or two sentences on what is predicted and for which unit.>

### Period

<One or two sentences: the window and the anchor date.>

## Preprocessing
<A numbered list. One line per step, with the stage (SQL or Python) and a
footnote. Variants: shared steps once, differences in the variants table.>

## Features
<A short paragraph on what the model learns from. Then a table of feature
sets, which is the one place a table is clearly useful.>

| Set | Contents |
|---|---|
| `<set name from code>` | <columns, in code order> |

<Engineered features, if any, as a short list with a footnote.>

## Model
<A paragraph: the algorithm, the library, and why it was chosen (ds_notes,
if any). Then how it is trained: hyperparameters set in code, those set in
the environment (named but not valued, if unknown), the split, the seed,
and the saved artifact. Each fact with a footnote.>

## Evaluation
<A paragraph: the method and the data it is evaluated on. Describe the order
of steps: the data is extracted for the date in `model.evaluated_on` (the
training run uses that extract), then split into train, valid and test, then
the metrics are computed on the split. Give the extract date from the config
as written; if it is empty, say so and add an open question.>

| Metric | Parameters | Variant | Train | Valid | Test |
|---|---|---|---|---|---|
| `<name as in dsdoc.yaml>` | <e.g. k=10, or —> | <variant, or —> | TODO | TODO | TODO |

Values come only from `dsdoc.yaml`. List the metrics that appear in
`dsdoc.yaml` and in the code, and no others. One sentence on which metrics the
code computes and which the success criteria ask for (see open question N).

### Metrics explained

For each metric in the table, in the same order, one entry:

**`<name as in dsdoc.yaml>`** (function `<name in code>`, `<file:line>`)
<One or two plain-language sentences: what the metric measures and whether
higher is better. Take them from the metric's own docstring in the code, and
footnote the `file:line`. If the docstring is missing or only names the metric,
write a general definition and label it "general definition, not from this
project".>

Rules for this section:
- Map each key in `dsdoc.yaml` to the function that computes it (for example
  `mrr` is `reciprocal_rank`, `ndcg_k_10` is `ndcg_at_k`). Say which function.
- Never reuse one explanation for several metrics. Each entry is its own text.
- Do not explain a metric the code does not compute.

If the data scientist notes ask for a baseline comparison, add a second table
under Evaluation: metric, this model, each baseline, difference. Both models
use the same split and the same k. Take the baseline's values from
the `baseline` block in the data scientist notes, from `dsdoc.yaml`, or from a
run in scope. Never estimate them. If a value is
missing, write TODO and add an open question.

## Output

<A paragraph: what the inference step takes in, what it returns, what the
scores mean, and which artifacts it needs.>

<Bullets: every output the pipeline writes, in the same format as the inputs
in Data: one bullet per item, named as in the code, with its type (file,
table, view, or artifact), its role, and its destination, then a footnote.
This covers each file the data step unloads, each table the copy steps load,
each view the create steps define, and each artifact the training and
inference steps save. List all of them.>

<Downstream consumers, if known, as bullets. Otherwise one line saying it
is an open question.>

## Limitations
<A short list from dsdoc.yaml only. If empty, one sentence saying so and
pointing to the open question.>

## Open Questions
Numbered. Each item names the section it belongs to in italics. This is a
logic check of the documentation, not a code review. Add an open question
only when:

- a claim in the card cannot be confirmed from the sources;
- two sources disagree on a fact the card depends on;
- a fact a reader needs to use or trust the model is missing (owner, intended
  use, out-of-scope uses, metrics, the success measure);
- a business term or pending business context item blocks understanding.

Do not raise style, naming, SQL or Python quality, performance, typos, unit
or rounding details, or possible bugs that do not change how the model is
described. Keep at most 8 open questions. If there are more, keep the ones
that most affect how the model should be used. Phrase each one neutrally, as
a question about the model or the process, and say what would settle it. Do not name the document that raised
it: write "The stated hash has 7 fields; the code hashes 8", not "The notes
say 7".

1. <question> *(section)*

---
[^1]: <source>
```

At the end of the card, state the number of open questions in one line:
`Open questions: <N>`.

## Reflection before you finish

Self-reflection only: your own checks on your own draft. A reviewer, if the
config asks for one, is a separate agent started by the dispatcher after
you finish; see "Refine run".

### Mode

Read `reflection.model_card` in `dsdoc.yaml`, else `reflection.default`, else
`self`. Values: `off`, `self`, `reviewer`, `both`.

| Mode | Script check | Self-critique |
|---|---|---|
| `off`, `reviewer` | yes | no |
| `self`, `both` | yes | yes |

If the mode is `reviewer` or `both` and your prompt does not start with
"Started by the dsdoc dispatcher", no reviewer will run: do the
self-critique, and say so in your final message.

### 1. Script check (always)

Run with Bash:

`bash .claude/skills/dsdoc-model-card/check.sh <output_dir>/model_card.md dsdoc.yaml`

It checks that every footnoted `file:line` exists, that every metric value in
`dsdoc.yaml` appears as written, the sections and their order, the
open-question cap and count, and source names or first-person voice. Fix the file and rerun, at most 3 times.

### 2. Self-critique (mode `self` or `both`)

After the script check passes, reread the file against
`.claude/skills/dsdoc-model-card/criteria.md`, answering each item as that file
says. Fix every "no" once, then run the script check again. One round only.

In your final message, list every item id with its answer, one per line
(e.g. `D1: yes`, `G2: no — fixed: <what>`). A self-critique without this
list counts as not run. A "no" you leave unfixed needs the rule that stops
the fix; "no time" or "minor" is not a reason.

### Stop

Never loop beyond these rounds. Anything still failing goes in your final
message.

## Refine run (started by the dispatcher)

Only when your prompt says "Refine run" and contains reviewer notes. Read
the existing file, apply each note that the code, the notes, `dsdoc.yaml` or `business_context.md` support, then run the
script check. Do not rewrite from scratch and do not run the self-critique.
After the script check, reread the file note by note: for each note marked
applied, quote the line that now satisfies it. A note whose line you cannot
quote, or whose quote still contains what the note asked to remove, is not
applied; fix it once or list it as not applied.
Never apply a note that breaks a ground rule (e.g. changes a metric value,
or drops an open question to make room). List every note not applied, and why.

## At the end

Report: the path of the model card, how many sections are complete, and the
list of open questions, the script check result, the self-critique "no" answers
and fixes, and, in a refine run, the notes not applied.
