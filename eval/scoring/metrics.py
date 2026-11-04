"""Turns judge verdicts and static results into scores in [0, 1] and averages them over runs."""
import statistics
from pathlib import Path

import yaml

WEIGHTS = yaml.safe_load((Path(__file__).parent / "weights.yaml").read_text())


def judge_score(skill, judge, verdict):
    """One number per judge. None when the judge has nothing to score (empty claim list, text answers)."""
    if "claims" in verdict:
        claims = verdict["claims"]
        if not claims:
            return None
        return sum(c["verdict"] == "supported" for c in claims) / len(claims)
    if "items" in verdict:
        items = verdict["items"]
        return sum(bool(i["found"]) for i in items) / len(items) if items else None
    if "answer" in verdict:
        return 1.0 if verdict["answer"] else 0.0
    return None  # text answers are graded by comprehension_grade


def static_score(static):
    checks = list(static["checks"].values())
    if not checks:
        return None
    return sum(c["passed"] for c in checks) / len(checks)


def run_score(skill, static, judges):
    """Weighted mean of the static and judge scores of one run. 0 when the sensitive check fails."""
    if not static["sensitive"]["passed"]:
        return 0.0
    parts = []
    s = static_score(static)
    if s is not None:
        parts.append((WEIGHTS["static"], s))
    for judge, verdict in judges.items():
        sc = judge_score(skill, judge, verdict)
        if sc is not None:
            parts.append((WEIGHTS["judges"].get(f"{skill}/{judge}", 1), sc))
    total = sum(w for w, _ in parts)
    return sum(w * v for w, v in parts) / total if total else None


def summarize(scores):
    """Mean and spread over the runs of one test. Scores that are None are left out."""
    vals = [s for s in scores if s is not None]
    if not vals:
        return {"mean": None, "stdev": None, "runs": 0}
    return {"mean": statistics.mean(vals), "stdev": statistics.pstdev(vals), "runs": len(vals)}
