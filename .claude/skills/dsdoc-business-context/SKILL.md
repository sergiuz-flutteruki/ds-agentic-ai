---
name: dsdoc-business-context
description: dsdoc skill that builds one business context document from the business sources of a model - converted PDFs (e.g. a lean canvas) and Markdown files (e.g. Confluence exports). Use it when the user asks dsdoc for the business context, or adds business documents for the model card.
context: fork
agent: dsdoc-business-context-writer
---

# dsdoc: build the business context

Read the business sources and write `<output_dir>/business_context.md`
(default `docs/business_context.md`) with the fixed sections below.
Overwrite it if it exists. The model card reads business facts only from
this file.

## Sources

- Every `.md` in `<output_dir>/sources/`, written by `dsdoc-convert` from
  `context.pdf_inputs`. Never read the PDFs themselves.
- Every file in `context.business_docs` (in `dsdoc.yaml`).
- If the user gives paths directly, use those instead.
- If a file in `context.pdf_inputs` has no `.md` in `sources/`, stop and
  say that `dsdoc-convert` must run first. If there are no sources at all,
  stop and ask for one.

No code, no `ds_notes.md`, no `dsdoc.yaml` fields other than `context`
and `output_dir`.

## dsdoc ground rules

- **Never invent.** Every statement comes from a source. A section with
  nothing in the sources is `—`, and the gap goes to Open questions.
- **Cite every paragraph and bullet** with a footnote to its source:
  `[^n]` and, at the end, `[^n]: <path> § <heading as written>`. The path is
  as listed in Sources (e.g. `docs/sources/canvas.md`).
  Cite the heading the text actually comes from. A statement built from
  several headings gets one footnote per heading. A gap (something no
  source says) has no footnote: never cite a heading for what it does not
  contain.
- **Close to the source.** Keep the source's wording; shorten only to
  remove repetition between sources. Keep typos, acronyms and £ figures
  exactly as written.
- **No interpretation.** Do not say whether a target is ambitious, a risk
  likely, or a figure good. Figures are written as "programme target"
  unless the source ties them to one model.
- **Conflicts are shown, never resolved.** If two sources disagree (a
  figure, a scope, an owner), write both under Conflicts between sources,
  each with its footnote, and use neither in the other sections.
- **Pending stays pending.** Every `[PENDING]` item in a source goes to
  Open questions, verbatim, with its footnote. Keep it in its section too,
  prefixed `[PENDING]`.
- **Analyses are not models.** A proposed analysis, study or segmentation
  keeps the label `(analysis, not a model)` in Proposed models and scope.
- **Each fact once.** A figure, a target or a name appears in one section
  only, the one whose question it answers best.
- **No sensitive data.** Leave out personal emails, phone numbers, internal
  URLs and hostnames, credentials, and customer-level data. Names of
  people in a role (owner, validator) are allowed.

## Matching sources to sections

Sources do not share a template. Match **by meaning, not by heading**.
Lean canvas headings seen so far:

| Section | Canvas headings seen so far |
|---|---|
| Problem | "What is the problem?", "What is the problem or opportunity?" |
| Proposed models and scope | the "we propose" / "models are required" part of the problem |
| Objective and success criteria | "How big is the problem?", "Estimated benefits / ROI", "What is your hypothesis?", "The success of the model will be measured by" |
| Stakeholders and validators | "Who will be needed to validate?", business lead, tribe |
| Constraints and risks | "What are the next steps to validate?" only where they name a risk or a dependency; plain steps go to Other |

Ignore template guidance text (grey hints such as "Provide a high-level
overview..."). Content that fits no section goes under `## Other`, with
its original heading. Never drop content.

## Steps

1. **Read every source in full.**
2. **Split the proposed models.** One bullet per model, cohort or variant
   (brand, market), with its name as written. If no source proposes an ML
   model, write `None: not a model initiative`, say so to the user, and
   stop after writing the file: it must not be used for a model card.
3. **Fill the sections**, applying the ground rules.
4. **Collect the terms.** Terms a source defines go in Glossary, with the
   definition as written. Acronyms and terms used without a definition go
   to Open questions. Don't expand them yourself.
5. **Choose the open questions.** An open question is something a reader of
   the model card needs and the sources do not settle: a `[PENDING]` item,
   an undefined term, a conflict, or an empty Users and decisions or Not
   intended for. Write each as a question. An empty Glossary, Other or
   Conflicts section is not an open question.
6. **Reflect before you finish** (below).

## Template

```markdown
# Business context: <initiative name, as written>

| Field | Value |
|---|---|
| Sources | `<path>`, `<path>` |
| Generated | <YYYY-MM-DD HH:MM, from `date`> |
| Customers / Brands | <or —> |

## Problem
<2-5 sentences, cited>

## Proposed models and scope
- **<model, cohort or variant>**: <description>[^n]

## Objective and success criteria
<hypothesis, programme targets, and success measures, cited>

## Users and decisions
<who uses the output and which decision it supports, or —>

## Not intended for
<uses the sources exclude, or —>

## Constraints and risks
<regulation, safety, budget, dependencies, or —>

## Stakeholders and validators
<roles and names as written, or —>

## Glossary
- **<term>**: <definition as written>[^n]

## Other
<content that fits no section, under its original heading, or —>

## Conflicts between sources
- <topic>: <source A says>[^n]; <source B says>[^m]. (or —)

## Open questions
1. <[PENDING] item, undefined term, or empty section>[^n]

[^1]: <path> § <heading>
```

## Reflection before you finish

Self-reflection only: your own checks on your own draft. A reviewer, if the
config asks for one, is a separate agent started by the dispatcher after
you finish; see "Refine run".

### Mode

Read `reflection.business_context` in `dsdoc.yaml`, else `reflection.default`, else
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

`bash .claude/skills/dsdoc-business-context/check.sh <output_dir>/business_context.md <source> [<source> ...]`

It checks the required sections and their order, that every section has content or `—`,
that every footnote points to a listed source and to a heading in it, that
every `[PENDING]` item of the sources appears in the file, that no open
question cites a source for a gap, and that every quote is copied exactly. Fix the file and rerun, at most 3 times.

### 2. Self-critique (mode `self` or `both`)

After the script check passes, reread the file against
`.claude/skills/dsdoc-business-context/criteria.md`, answering each item as that file
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
the existing file, apply each note that the sources support, then run the
script check. Do not rewrite from scratch and do not run the self-critique.
After the script check, reread the file note by note: for each note marked
applied, quote the line that now satisfies it. A note whose line you cannot
quote, or whose quote still contains what the note asked to remove, is not
applied; fix it once or list it as not applied.
Never edit text inside quotation marks; if a note asks for it, cut the
other occurrence or list the note as not applied. Never apply a note that
breaks a ground rule (e.g. adds a fact no source states). List every note not applied, and why.

## At the end

Report: the output path, the sources read, the proposed models with their
names, the number of conflicts and open questions, the script check result, the self-critique "no" answers
and fixes, and, in a refine run, the notes not applied.
