---
name: dsdoc-code-doc
description: dsdoc skill that adds docstrings and comments to the Python and SQL files in scope, without changing any logic. Use it when the user asks dsdoc, or asks to document the code, add docstrings, or comment the SQL queries.
context: fork
agent: dsdoc-code-doc-writer
---

# dsdoc: generate docstrings and code documentation

Add documentation directly in the files in scope. Change nothing else: no
refactoring, no renaming, no fixes, even if you spot a problem.

## dsdoc ground rules

- **Config first.** Read `dsdoc.yaml` at the repo root. If it is missing,
  use the defaults: Python in `src/model_code`, SQL in `src/data` and
  `src/sql`.
- **Stay in scope.** Only `*.py` under `scope.python` and `*.sql` under
  `scope.sql`. Nothing else in the repo, not even for context. Not the
  business context either: comments describe the code, not the business intent.
- **Never invent.** Every fact comes from the code (`file:line`) or from
  `dsdoc.yaml`. Anything else is `TODO(owner): <specific question>`.

## Steps

1. **Read `dsdoc.yaml`** and list the files in scope (Python in
   `scope.python`, SQL in `scope.sql`).
2. **Order:** SQL files first, then Python modules that are imported by
   others, then the ones that import them. By the time you document the
   training function, you know what everything it calls does.
3. **For each file** (`<rel>` = its path relative to the repo root):
   1. Back it up:
      ```bash
      mkdir -p "$(dirname /tmp/dsdoc/<rel>)" && cp <rel> /tmp/dsdoc/<rel>.orig
      ```
   2. Add the documentation (see below).
   3. **Reflect before you finish** (below) for that file.

## Python

NumPy-style docstrings for every module and function:

```python
def scale_numeric(train_df, test_df):
    """Standardize the base numeric columns.

    The scaler is fitted on train only and applied to both sets.

    Parameters
    ----------
    train_df : pd.DataFrame
        Training features.
    test_df : pd.DataFrame
        Test features.

    Returns
    -------
    tuple
        (scaled train_df, scaled test_df, fitted scaler).
    """
```

- First line: what it does, under 80 characters.
- For DataFrames: which columns are expected or added.
- A `Notes` section (underlined with `-----`) for non-obvious effects (NaN
  handling, in-place changes, what must be reused at inference).

## SQL

A header comment at the top of each file, plus inline comments on
non-obvious parts:

```sql
-- Purpose: one row per active customer with billing totals.
-- Sources: crm.customers, billing.invoices
-- Output:  customer_id, tenure, monthly_charges, total_charges, churn
-- Grain:   one row per customer_id
```

Comment joins that can duplicate rows, filters, and how derived columns
(especially the target) are computed.

## Comments and markers

Comment the **why**, not the **what**. Use two markers so they can be found
with grep:
- `NOTE:` an important fact (e.g. "median computed before the split").
- `TODO(owner):` a question the code can't answer (e.g. unit of `tenure`).

Never write an assumption as a fact.

## Reflection before you finish

Self-reflection only: your own checks on your own work. This skill has no
reviewer.

### Mode

Not used yet: the script check always runs, and there is no self-critique.

### 1. Script check (always)

For every edited file, run with Bash:

`python .claude/skills/dsdoc-code-doc/scripts/check_unchanged.py /tmp/dsdoc/<rel>.orig <rel>`

It checks that the Python AST (docstrings removed) or the SQL (comments
removed, whitespace normalized) is unchanged. If it fails, restore the
backup and report the file.

### 2. Self-critique

Not yet: there is no `criteria.md` for this skill (planned in
`agent-todo.md`).

### Stop

One check per file; a failed file is restored, not retried.

## Refine run (started by the dispatcher)

Not applied: no reviewer for this skill.

## At the end

Report: the files changed, every `NOTE` / `TODO(owner)` added, and the
script check result per file.
