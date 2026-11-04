"""Scores: the sensitive check is a gate, judges score as their schema says."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scoring.metrics import judge_score, summarize, run_score  # noqa: E402


def static(sensitive=True, checks=None):
    return {"checks": checks or {}, "sensitive": {"passed": sensitive, "output": ""}, "passed": sensitive}


def test_sensitive_failure_zeroes_the_test():
    s = run_score("stake_summary", static(sensitive=False, checks={"c": {"passed": True}}),
                   {"fidelity": {"claims": [{"claim": "a", "evidence": "", "verdict": "supported"}]}})
    assert s == 0.0


def test_claim_score_is_share_supported():
    v = {"claims": [{"claim": "a", "evidence": "", "verdict": "supported"},
                    {"claim": "b", "evidence": "", "verdict": "unsupported"}]}
    assert judge_score("stake_summary", "fidelity", v) == 0.5


def test_match_score_is_share_found():
    v = {"items": [{"item": "a", "quote": "q", "found": True}, {"item": "b", "quote": "", "found": False}]}
    assert judge_score("stake_summary", "critical_facts", v) == 0.5


def test_binary_score_is_answer():
    assert judge_score("stake_summary", "business_link", {"justification": "", "answer": True}) == 1.0


def test_text_answers_have_no_score_of_their_own():
    assert judge_score("stake_summary", "comprehension_answer", {"answers": []}) is None


def test_summarize_mean_and_spread():
    s = summarize([0.5, 1.0, None])
    assert s["runs"] == 2 and s["mean"] == 0.75
