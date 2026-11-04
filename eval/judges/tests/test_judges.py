"""Judge tests (eval-plan.md, section 9) that need no API: format, refusal, retry, registry integrity.

Behaviour tests (catches a planted error, consistency, length bias) need the real model; they run
through judges/calibration and are not in this file.
"""
import json
import sys
from pathlib import Path

import pytest

JUDGES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(JUDGES))

from judge_client import (UncalibratedJudge, find_entry, load_registry, parse_prompt,  # noqa: E402
                          run_judge)

CONFIG = {"judge": {"model": "m", "temperature": 0, "max_tokens": 10, "retries": 1}}


class FakeClient:
    def __init__(self, answers):
        self.answers = list(answers)
        self.calls = 0

    def complete(self, system, user, model, temperature, max_tokens):
        self.calls += 1
        return self.answers.pop(0)


def test_registry_points_to_existing_files():
    for skill, entries in load_registry().items():
        for e in entries:
            assert (JUDGES / e["prompt"]).exists(), e["prompt"]
            assert (JUDGES / e["schema"]).exists(), e["schema"]


def test_every_prompt_has_one_question_and_frontmatter():
    for skill, entries in load_registry().items():
        for e in entries:
            meta, body = parse_prompt(JUDGES / e["prompt"])
            assert "version" in meta and "calibrated" in meta
            assert body.count("# Question") == 1


def test_uncalibrated_judge_is_refused():
    entry = find_entry("stake_summary", "fidelity")
    with pytest.raises(UncalibratedJudge):
        run_judge("stake_summary", "fidelity", {"summary": "x", "model_card": "y"},
                  FakeClient([]), CONFIG, allow_uncalibrated=False)


def test_invalid_json_is_retried_once_then_accepted():
    good = json.dumps({"claims": [{"claim": "a", "evidence": "a", "verdict": "supported"}]})
    client = FakeClient(["not json", good])
    verdict = run_judge("stake_summary", "fidelity", {"summary": "x", "model_card": "y"},
                        client, CONFIG, allow_uncalibrated=True)
    assert client.calls == 2
    assert verdict["_attempts"] == 2


def test_schema_violation_is_an_error():
    bad = json.dumps({"claims": [{"claim": "a", "evidence": "", "verdict": "maybe"}]})
    with pytest.raises(ValueError):
        run_judge("stake_summary", "fidelity", {"summary": "x", "model_card": "y"},
                  FakeClient([bad, bad]), CONFIG, allow_uncalibrated=True)


def test_criteria_md_is_never_the_judge_rubric():
    for skill, entries in load_registry().items():
        for e in entries:
            assert "criteria" not in (JUDGES / e["prompt"]).read_text().lower().split("# role")[0]
            assert "criteria.md" not in (JUDGES / e["prompt"]).read_text()
