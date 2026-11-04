# dsdoc evaluation

Implements `eval-plan.md` (at the repo root). Evaluates the writers of the `dsdoc-*` skills. Reviewers
are not evaluated yet (plan, scope). The old evaluation lives in `eval2/`.

## What runs

For each skill, each case, each run (`runs_per_test` in `config.yaml`):

1. **Sandbox** (`runner/sandbox.py`): a copy of `.claude/` and the case input. Refuses any folder that
   contains `eval/` or a reference or label file.
2. **Agent** (`runner/agent_runner.py`): the writer, run with `claude -p` inside the sandbox. Its
   `output/` is copied to `results/runs/<stamp>/<skill>/<case>/run_<n>/output/`.
3. **Static checks** (`static/run_checks.py`): the existing scripts of `.claude/skills/`, called as the
   reviewers call them, plus `check_sensitive.sh`. Nothing is reimplemented here.
4. **Judges** (`judges/`): one question per judge, a schema per answer, inputs from `judges/registry.yaml`.
   A judge that is not calibrated is **skipped**, not run.
5. **Score** (`scoring/`): weighted mean in [0, 1]. A sensitive-data failure scores 0.
6. **Report**: `summary.csv` and `report.md` in the run folder.

## Commands

```bash
python3 eval/run_eval.py --skill all --dry-run            # list runs, call nothing
python3 eval/run_eval.py --skill stake_summary --runs 3
python3 eval/run_eval.py --skill all --allow-uncalibrated  # development only
python3 eval/judges/calibration/run_calibration.py --judge stake_summary/fidelity
python3 eval/human_review/export_sample.py eval/results/runs/<stamp>
python3 -m pytest -q eval/tests eval/judges/tests           # no API calls
```

## Status

| Part | State |
|---|---|
| Config, sandbox, agent runner, static checks, scoring, driver, report | implemented, tested with a fake agent and a fake model |
| Judge client, schemas, registry, 15 prompts | implemented; prompts are drafts, `calibrated: null` |
| Judge format and refusal tests | implemented (`judges/tests/`, no API) |
| Judge behaviour tests (planted errors, consistency, length bias) | not yet: need the real model (`judges/calibration/`) |
| Calibration | script implemented; **no cases, no human labels yet** |
| Datasets | **empty**: written by people (`datasets/README.md`) |
| Static scripts in the JSON contract (plan, section 5) | **not done**: scripts keep exit code and text output; discuss before changing them |
| `e2e` | not implemented (`--e2e` says so and exits 2) |

Until the judges are calibrated, scores are static checks only, and the report says so. Do not quote
judge numbers as evidence.

## Rules (plan, section 13)

- `eval/` is never copied into `.claude/` or into a working project.
- Reference data and labels are not read by agents or skills.
- The agent runs only in a sandbox.
- Static scripts are called from `.claude/skills/`, never copied.
- Judges are API calls from `eval/`, with a different model from the agent, temperature 0.
- `criteria.md` of the reviewers is never a judge rubric.
- One judge = one question, JSON output, justification before verdict.
- No uncalibrated judge in a real evaluation.
- Each test runs `runs_per_test` times; the report shows mean and spread.

## Open points (owner)

- `TODO(owner)`: the `claude -p` flags and the writer prompt in `runner/agent_runner.py`.
- `TODO(owner)`: the datasets and `reference.json` files.
- `TODO(owner)`: 2 people for human labels; the calibration cases.
- `TODO(owner)`: `judges/examples/*.jsonl` are empty; 2–3 human-scored examples per judge.
- `TODO(owner)`: `CLAUDE.md` points to `docs/dsdoc-eval-plan.md`, which does not exist. The plan is at `eval-plan.md`.
- `TODO(owner)`: scope of the `convert` skill.
