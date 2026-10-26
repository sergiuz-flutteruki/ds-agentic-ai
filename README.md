# dsdoc

A documentation agent for data science projects, for Claude Code.
One dispatcher skill, four agents with their skills, one config file.

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
│   ├── dsdoc-canvas-writer.md         # sonnet
│   ├── dsdoc-model-card-writer.md     # sonnet
│   ├── dsdoc-code-doc-writer.md       # sonnet
│   └── dsdoc-stake-summary-writer.md  # opus, effort low
└── skills/
    ├── dsdoc/SKILL.md                 # dispatcher
    ├── dsdoc-canvas/SKILL.md          # lean canvas (PDF/image) -> normalized .md
    ├── dsdoc-model-card/SKILL.md      # generate model card
    ├── dsdoc-code-doc/
    │   ├── SKILL.md                   # generate docstrings & code comments
    │   └── scripts/check_unchanged.py
    └── dsdoc-stake-summary/SKILL.md   # generate stakeholder summary
dsdoc.yaml                             # scope, output folder, canvas, human context
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
- the lean canvas PDF in `context.lean_canvas_pdf` (canvas writer only); the
  model card reads its normalized `docs/lean_canvas.md`

Change it in `dsdoc.yaml` under `scope` and `context`.

## Use

1. Fill in `model:` in `dsdoc.yaml` (at least name and owner).
2. If there is a lean canvas: set `context.lean_canvas_pdf` to the PDF and
   run `/dsdoc-canvas`. It writes `docs/lean_canvas.md`, which the
   model card reads.
3. In Claude Code, run:

| You want | Run |
|---|---|
| Normalized lean canvas | `/dsdoc-canvas` (reads `context.lean_canvas_pdf`) |
| Model card | `/dsdoc-model-card` |
| Docstrings & comments | `/dsdoc-code-doc` (use a git branch) |
| Stakeholder summary | `/dsdoc-stake-summary` (needs the model card) |
| Everything | `/dsdoc` or "dsdoc, document everything" |

Outputs go to `docs/lean_canvas.md`, `docs/model_card.md` and
`docs/stake_summary.md`
(change `output_dir` in `dsdoc.yaml`). Each run overwrites the previous file.

## Data scientist notes

`docs/ds_notes.md` is optional and written by hand by the data scientist. The model card reads it and gives it priority over `dsdoc.yaml` and the canvas (`ds_notes.md` > `dsdoc.yaml` > canvas); the stakeholder summary gets it through the card. The agents never write or edit it. If it is missing, the model card lists it as an Open Question. It has no template yet.

## Models per brand

Many models are trained separately per brand (or product): the same Python
code with different SQL per brand. The model card detects this from the
folder and file names (`PP/`, `bf/`, `train_sbg.sql`, `gaming/`) and
writes one card: the shared pipeline once, plus a **Variants** table with
only what differs per brand. Metrics can be given per brand in
`model.metrics` (`{PP: {...}, BF: {...}}`).

## Dependencies

- `dsdoc-canvas`: before the model card, if `context.lean_canvas_pdf` is set.
- `dsdoc-model-card` and `dsdoc-code-doc`: independent.
- `dsdoc-stake-summary`: needs `model_card.md`.
