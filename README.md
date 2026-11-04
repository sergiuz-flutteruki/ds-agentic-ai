# dsdoc

A documentation agent for data science projects, for Claude Code.
One dispatcher skill, six skills with their agents, one config file.

## Install

Copy into your project root:

```bash
cp -r .claude/agents .claude/skills /path/to/project/.claude/
cp -n dsdoc.yaml /path/to/project/        # -n: keep the project's own config
```

Or edit the project list in `copy-claude.sh` and run `bash copy-claude.sh`.

## Structure

```
.claude/
├── agents/
│   ├── dsdoc-convert-writer.md            # sonnet, effort low
│   ├── dsdoc-business-context-writer.md   # sonnet, effort low
│   ├── dsdoc-business-context-reviewer.md # opus, effort medium
│   ├── dsdoc-model-card-writer.md         # sonnet, effort low
│   ├── dsdoc-model-card-reviewer.md       # opus, effort medium
│   ├── dsdoc-code-doc-writer.md           # sonnet, effort low
│   ├── dsdoc-stake-summary-writer.md      # opus, effort low
│   └── dsdoc-stake-summary-reviewer.md    # opus, effort medium
└── skills/
    ├── dsdoc/SKILL.md                 # dispatcher
    ├── dsdoc-convert/SKILL.md         # PDF/image (e.g. lean canvas) -> verbatim .md
    ├── dsdoc-business-context/
    │   ├── SKILL.md                   # business sources -> business_context.md
    │   ├── check.sh
    │   └── criteria.md
    ├── dsdoc-model-card/
    │   ├── SKILL.md                   # generate model card
    │   ├── check.sh
    │   └── criteria.md
    ├── dsdoc-code-doc/
    │   ├── SKILL.md                   # generate docstrings & code comments
    │   └── scripts/check_unchanged.py
    └── dsdoc-stake-summary/
        ├── SKILL.md                   # generate stakeholder summary
        ├── check.sh
        └── criteria.md
dsdoc.yaml                             # scope, output folder, business sources, human context
```

## Terms

- **Customers / users**: who receives the recommendations; can be in
  training and in inference.
- **Stakeholders / management**: who reads `stake_summary.md`, the
  explanation of the project and its output, built from the model card.
- **Developers / data scientists**: who reads `model_card.md` and
  generates the documentation with dsdoc.

## Scope

dsdoc reads only:
- `*.py` in `src/model_code/`
- `*.sql` in `src/data/` and `src/sql/`
- the PDFs in `context.pdf_inputs` (convert writer only), converted into
  `docs/sources/<name>.md`
- the Markdown files in `context.business_docs` (e.g. Confluence exports)

The business context writer reads `docs/sources/` and `context.business_docs`
and writes `docs/business_context.md`; the model card reads business facts only
from that file.

Change it in `dsdoc.yaml` under `scope` and `context`.

## Use

1. Fill in `model:` in `dsdoc.yaml` (at least name and owner).
2. Business sources: list PDFs (e.g. the lean canvas) in `context.pdf_inputs`
   and Markdown files (e.g. Confluence exports) in `context.business_docs`.
   `/dsdoc` converts the PDFs and builds `docs/business_context.md` before the card.
3. In Claude Code, run:

| You want | Run |
|---|---|
| PDFs to Markdown | `/dsdoc-convert` (reads `context.pdf_inputs`) |
| Business context | `/dsdoc-business-context` (needs the converted PDFs) |
| Model card | `/dsdoc-model-card` |
| Docstrings & comments | `/dsdoc-code-doc` (use a git branch) |
| Stakeholder summary | `/dsdoc-stake-summary` (needs the model card) |
| Everything | `/dsdoc` or "dsdoc, document everything" |

Outputs go to `docs/sources/`, `docs/business_context.md`, `docs/model_card.md`
and `docs/stake_summary.md`
(change `output_dir` in `dsdoc.yaml`). Each run overwrites the previous file.

## Data scientist notes

`docs/ds_notes.md` is optional and written by hand by the data scientist. The model card reads it and gives it priority over `dsdoc.yaml` and the business context (`ds_notes.md` > `dsdoc.yaml` > business context); the stakeholder summary gets it through the card. The agents never write or edit it. If it is missing, the model card lists it as an Open Question. It has no template yet.

## Models per brand

Many models are trained separately per brand (or product): the same Python
code with different SQL per brand. The model card detects this from the
folder and file names (`PP/`, `bf/`, `train_sbg.sql`, `gaming/`) and
writes one card: the shared pipeline once, plus a **Variants** table with
only what differs per brand. Metrics can be given per brand in
`model.metrics` (`{PP: {...}, BF: {...}}`).

## Dependencies

- `dsdoc-convert`: before the business context, if `context.pdf_inputs` is set.
- `dsdoc-business-context`: before the model card, if `context.pdf_inputs` or
  `context.business_docs` is set.
- `dsdoc-model-card` and `dsdoc-code-doc`: independent.
- `dsdoc-stake-summary`: needs `model_card.md`.
