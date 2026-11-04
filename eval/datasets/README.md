# Datasets

Reference data is written by people (plan, sections 6 and 2.3). Nothing in this folder is generated.
The driver refuses to run a case whose `reference.json` lacks a key the judges read; the keys are listed by
`python3 -c "import run_eval as r; print(r.required_reference_keys('business_context'))"` (run from `eval/`).

```
datasets/<skill>/
  reference.json            { "<case>": { "<key>": ..., ... } }   TODO(owner): written by a person
  cases/<case>/input/       the frozen inputs the agent gets (sandbox: copied into ./input)
```

Status per skill (plan, section 6):

| Skill | Cases | Owner's task |
|---|---|---|
| code_doc | 0 of 30–50 | TODO(owner): functions, categories, planted errors |
| business_context | 0 of 10–15 | TODO(owner): Lean Canvas PDF + Confluence pages, contradictions, missing fields |
| model_card | 0 of 8–12 | TODO(owner): projects, documented and undocumented variants, planted conflicts |
| stake_summary | 0 of 8–12 | TODO(owner): model cards, critical facts, the five fixed questions |
| convert | — | TODO(owner): scope of the convert skill is not defined yet |
