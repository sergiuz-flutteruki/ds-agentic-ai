"""End to end with a fake agent and a fake model: the driver runs, scores and reports.

Nothing here calls Claude. The dataset is a temporary one.
"""
import json
import sys
from pathlib import Path

import pytest

EVAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL))

import run_eval  # noqa: E402


def fake_agent(sandbox, skill, command, timeout):
    """Writes a business_context.md into output/, like a writer would."""
    (Path(sandbox) / "output" / "business_context.md").write_text("# Business context\n\nText.\n")
    return True, "ok"


class FakeModel:
    """Answers each judge with a valid answer for its schema (pass for every item)."""

    def complete(self, system, user, model, temperature, max_tokens):
        if '"title": "claim_verdicts"' in user:
            return json.dumps({"claims": [{"claim": "c", "evidence": "e", "verdict": "supported"}]})
        if '"title": "match"' in user:
            return json.dumps({"items": [{"item": "i", "quote": "q", "found": True}]})
        if '"title": "text"' in user:
            return json.dumps({"answers": [{"question": "q", "answer": "a"}]})
        return json.dumps({"justification": "j", "answer": True})


@pytest.fixture
def dataset(tmp_path, monkeypatch):
    datasets = tmp_path / "datasets"
    case = datasets / "business_context" / "cases" / "demo" / "input"
    case.mkdir(parents=True)
    (case / "lean_canvas.md").write_text("Problem: X.\n")
    (datasets / "business_context" / "reference.json").write_text(
        json.dumps({"demo": {"facts": ["X"], "cited_facts": [], "conflicts": []}}))
    monkeypatch.setattr(run_eval, "DATASETS", datasets)
    monkeypatch.setattr(run_eval, "RESULTS", tmp_path / "results")
    return tmp_path


def test_run_scores_and_reports(dataset):
    code = run_eval.main(["--skill", "business_context", "--runs", "2", "--allow-uncalibrated"],
                         agent=fake_agent, client=FakeModel())
    assert code == 0
    runs = list((dataset / "results" / "runs").iterdir())
    assert len(runs) == 1
    stamp = runs[0]
    scores = sorted(stamp.rglob("score.json"))
    assert len(scores) == 2
    for p in scores:
        rec = json.loads(p.read_text())
        assert 0.0 <= rec["score"] <= 1.0
        assert rec["judges_skipped"] == []
    report = (stamp / "report.md").read_text()
    assert "business_context" in report and "| demo |" in report


def test_uncalibrated_judges_are_skipped_and_reported(dataset):
    run_eval.main(["--skill", "business_context", "--runs", "1"], agent=fake_agent, client=FakeModel())
    stamp = next((dataset / "results" / "runs").iterdir())
    rec = json.loads(next(stamp.rglob("score.json")).read_text())
    assert "recall" in rec["judges_skipped"]
    assert "Judges not calibrated" in (stamp / "report.md").read_text()


def test_missing_cases_are_reported_not_crashing(dataset, capsys):
    code = run_eval.main(["--skill", "model_card", "--dry-run"], agent=fake_agent, client=FakeModel())
    assert code == 0
    assert "no cases" in capsys.readouterr().out


def test_e2e_is_not_silently_run(dataset, capsys):
    assert run_eval.main(["--e2e"]) == 2


def test_missing_reference_key_fails_before_any_run(tmp_path, monkeypatch):
    datasets = tmp_path / "datasets"
    case = datasets / "business_context" / "cases" / "demo" / "input"
    case.mkdir(parents=True)
    (datasets / "business_context" / "reference.json").write_text(json.dumps({"demo": {"facts": []}}))
    monkeypatch.setattr(run_eval, "DATASETS", datasets)
    with pytest.raises(ValueError, match="lacks"):
        run_eval.list_cases("business_context")


def test_estimate_counts_calls(dataset):
    config = {"judge": {"retries": 1}, "estimate": {"agent_cost_per_run": 2.0, "judge_cost_per_call": 0.5}}
    rows = run_eval.estimate(["business_context"], 3, config, allow_uncalibrated=True)
    r = rows[0]
    # 1 case x 3 runs = 3 agent calls. Judge calls = runs x judges in the registry for the skill;
    # the worst case doubles them for the one retry.
    n_judges = len(run_eval.load_registry()["business_context"])
    assert r["cases"] == 1 and r["agent_calls"] == 3
    assert r["judge_calls"] == 3 * n_judges
    assert r["judge_calls_worst"] == 2 * r["judge_calls"]
    assert r["agent_cost"] == 6.0


def test_estimate_skips_uncalibrated_judges_by_default(dataset):
    config = {"judge": {"retries": 0}}
    r = run_eval.estimate(["business_context"], 1, config, allow_uncalibrated=False)[0]
    assert r["judges_run"] == []
    assert r["judge_calls"] == 0


def _write_old_run(root, skill, case, scores):
    for n, s in enumerate(scores, 1):
        d = root / skill / case / f"run_{n}"
        d.mkdir(parents=True)
        (d / "score.json").write_text(json.dumps({"skill": skill, "case": case, "score": s}))


def test_compare_flags_drop_larger_than_spread_and_threshold(tmp_path):
    old = tmp_path / "old"
    _write_old_run(old, "business_context", "a", [0.9, 0.9])   # stable, high
    _write_old_run(old, "business_context", "b", [0.6, 0.8])   # noisy
    records = [
        {"skill": "business_context", "case": "a", "score": 0.6},
        {"skill": "business_context", "case": "a", "score": 0.6},   # drop 0.3, no spread -> regression
        {"skill": "business_context", "case": "b", "score": 0.66},  # drop 0.07, inside old spread
        {"skill": "business_context", "case": "b", "score": 0.66},
        {"skill": "business_context", "case": "c", "score": 0.5},   # not in the old run
    ]
    rows = {r[1]: r for r in run_eval.compare_runs(old, records, threshold=0.05)}
    assert rows["a"][-1] == "regression"
    assert rows["b"][-1] == "same"
    assert rows["c"][-1] == "new case"


def test_compare_threshold_stops_noise_on_zero_spread(tmp_path):
    old = tmp_path / "old"
    _write_old_run(old, "business_context", "a", [0.80, 0.80])
    records = [{"skill": "business_context", "case": "a", "score": 0.79}] * 2
    rows = run_eval.compare_runs(old, records, threshold=0.05)
    assert rows[0][-1] == "same"   # drop 0.01 is below the threshold
