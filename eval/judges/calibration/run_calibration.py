"""Calibrates one judge against human labels (eval-plan.md, section 10).

Cases: calibration/cases/<skill>/<judge>/<id>.json with
  {"id": str, "inputs": {field: text}, "human_pass": bool, "planted": bool, "split": "dev"|"holdout"}
A case passes when the judge's verdict is a pass (see verdict_pass). Each case runs `repeats` times.
Targets: config.yaml, calibration_targets. Only a run that meets them on the holdout split can set
`calibrated` in the prompt's frontmatter (--write-calibrated).

  python3 eval/judges/calibration/run_calibration.py --judge stake_summary/fidelity
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
JUDGES_DIR = HERE.parent
EVAL_DIR = JUDGES_DIR.parent
sys.path.insert(0, str(JUDGES_DIR))

from judge_client import find_entry, parse_prompt, run_judge  # noqa: E402


def verdict_pass(verdict):
    """Pass/fail of one verdict, the same way the metrics read it."""
    if "claims" in verdict:
        return all(c["verdict"] == "supported" for c in verdict["claims"])
    if "items" in verdict:
        return all(i["found"] for i in verdict["items"])
    if "answer" in verdict:
        return bool(verdict["answer"])
    raise ValueError("verdict has no pass/fail form (text answers are graded by comprehension_grade)")


def load_cases(skill, judge):
    folder = HERE / "cases" / skill / judge
    return [json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))]


def evaluate(cases, judge_fn, repeats):
    """Run the judge on every case. Returns the numbers that the targets are compared with."""
    results = []
    for case in cases:
        verdicts = [judge_fn(case["inputs"]) for _ in range(repeats)]
        passes = [verdict_pass(v) for v in verdicts]
        results.append({"id": case["id"], "human": case["human_pass"], "planted": case.get("planted", False),
                        "passes": passes, "consistent": len(set(passes)) == 1,
                        "judge": passes[0], "majority": sum(passes) * 2 >= len(passes)})
    total = len(results)
    agree = sum(r["majority"] == r["human"] for r in results)
    planted = [r for r in results if r["planted"]]
    tp = sum(r["human"] and r["majority"] for r in results)
    predicted_pass = sum(r["majority"] for r in results)
    return {
        "cases": total,
        "judge_human_agreement": agree / total if total else None,
        "planted_error_recall": (sum(not r["majority"] for r in planted) / len(planted)) if planted else None,
        "precision": (tp / predicted_pass) if predicted_pass else None,
        "judge_consistency": sum(r["consistent"] for r in results) / total if total else None,
        "results": results,
    }


def meets(numbers, targets):
    """Each target that has a number must be met. Missing numbers fail: nothing is assumed."""
    checks = {
        "judge_human_agreement": numbers["judge_human_agreement"] is not None
        and numbers["judge_human_agreement"] > targets["judge_human_agreement"],
        "planted_error_recall": numbers["planted_error_recall"] is not None
        and numbers["planted_error_recall"] > targets["planted_error_recall"],
        "precision": numbers["precision"] is not None and numbers["precision"] > targets["precision"],
        "judge_consistency": numbers["judge_consistency"] is not None
        and numbers["judge_consistency"] > targets["judge_consistency"],
    }
    return all(checks.values()), checks


def main(argv=None, client=None):
    p = argparse.ArgumentParser()
    p.add_argument("--judge", required=True, help="skill/judge, e.g. stake_summary/fidelity")
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--write-calibrated", action="store_true")
    args = p.parse_args(argv)
    skill, judge = args.judge.split("/", 1)
    config = yaml.safe_load((EVAL_DIR / "config.yaml").read_text())
    cases = load_cases(skill, judge)
    if not cases:
        print(f"no calibration cases in calibration/cases/{skill}/{judge}/ (human labels needed)")
        return 2
    if client is None:
        from judge_client import AnthropicClient
        client = AnthropicClient()

    def judge_fn(inputs):
        return run_judge(skill, judge, inputs, client, config, allow_uncalibrated=True)

    dev = [c for c in cases if c.get("split", "dev") == "dev"]
    holdout = [c for c in cases if c.get("split") == "holdout"]
    dev_numbers = evaluate(dev, judge_fn, args.repeats)
    report = [f"# Calibration {skill}/{judge}", "", f"Prompt version: {parse_prompt(JUDGES_DIR / find_entry(skill, judge)['prompt'])[0].get('version')}", ""]
    report += ["## Dev split", "```json", json.dumps({k: v for k, v in dev_numbers.items() if k != 'results'}, indent=2), "```", ""]

    _, dev_checks = meets(dev_numbers, config["calibration_targets"])
    print(json.dumps({"dev_targets_met": dev_checks}, indent=2))
    if not holdout:
        print("no holdout cases yet: the judge cannot be marked calibrated (plan, section 10.9)")
        return 1
    hold_numbers = evaluate(holdout, judge_fn, args.repeats)
    ok_hold, hold_checks = meets(hold_numbers, config["calibration_targets"])
    report += ["## Holdout split", "```json", json.dumps({k: v for k, v in hold_numbers.items() if k != 'results'}, indent=2), "```", ""]
    (HERE / "reports").mkdir(exist_ok=True)
    report_path = HERE / "reports" / f"{judge}_{date.today():%Y-%m-%d}.md"
    report_path.write_text("\n".join(report))
    print(f"report: {report_path}")
    if ok_hold and args.write_calibrated:
        prompt = JUDGES_DIR / find_entry(skill, judge)["prompt"]
        text = prompt.read_text().replace("calibrated: null", f"calibrated: {date.today():%Y-%m-%d}", 1)
        prompt.write_text(text)
        print(f"{skill}/{judge} marked calibrated")
    return 0 if ok_hold else 1


if __name__ == "__main__":
    sys.exit(main())
