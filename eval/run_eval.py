"""Evaluation driver: sandbox -> agent -> static checks -> judges -> score -> report.

Per skill, per case, per run (config.yaml: runs_per_test). Plan: eval-plan.md, section 4.

  python3 eval/run_eval.py --skill stake_summary
  python3 eval/run_eval.py --skill all --runs 3
  python3 eval/run_eval.py --skill model_card --dry-run      # list the runs, call nothing
"""
import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

EVAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL_DIR))

from judges.judge_client import UncalibratedJudge, load_registry, run_judge  # noqa: E402
from runner.agent_runner import collect_output, run_agent  # noqa: E402
from runner.sandbox import make_sandbox  # noqa: E402
from scoring.metrics import summarize, run_score  # noqa: E402
from static.run_checks import run_static  # noqa: E402

SKILLS = ["code_doc", "business_context", "model_card", "stake_summary"]
DATASETS = EVAL_DIR / "datasets"
RESULTS = EVAL_DIR / "results"


def load_config():
    return yaml.safe_load((EVAL_DIR / "config.yaml").read_text())


def claude_dir(config):
    return (EVAL_DIR / config["claude_dir"]).resolve()


def list_cases(skill):
    """Cases of a skill: datasets/<skill>/cases/<case>/input/, with the reference in reference.json."""
    root = DATASETS / skill
    ref_path = root / "reference.json"
    if not ref_path.exists():
        return []
    reference = json.loads(ref_path.read_text())
    needed = required_reference_keys(skill)
    cases = []
    for case in sorted(reference):
        if not (root / "cases" / case / "input").exists():
            continue
        missing = needed - set(reference[case])
        if missing:  # a dataset error: fail before any agent run, naming the case and the keys
            raise ValueError(f"{skill}/{case}: reference.json lacks {sorted(missing)} (used by the judges)")
        cases.append((case, root / "cases" / case / "input", reference[case]))
    return cases


def required_reference_keys(skill):
    """The reference.json keys that the registry's judges read for this skill."""
    keys = set()
    for entry in load_registry().get(skill, []):
        for source in entry["inputs"].values():
            if source.startswith("reference."):
                keys.add(source.split(".", 1)[1])
    return keys


def read_texts(folder, suffixes):
    """All files of a folder with these suffixes, as one labelled text block each."""
    if not folder.exists():
        return ""
    parts = [f"## {p.relative_to(folder)}\n{p.read_text()}"
             for p in sorted(folder.rglob("*")) if p.is_file() and p.suffix in suffixes]
    return "\n\n".join(parts)


def resolve_inputs(entry, output_dir, input_dir, reference, verdicts):
    """Build the text of each registry input: output, input, reference.<key> or judge:<name>."""
    text = {}
    for field, source in entry["inputs"].items():
        if source == "output":
            text[field] = read_texts(output_dir, {".md", ".py"})
        elif source == "input":
            text[field] = read_texts(input_dir, {".md", ".py", ".yaml", ".txt", ".json"})
        elif source.startswith("reference."):
            text[field] = json.dumps(reference[source.split(".", 1)[1]], ensure_ascii=False, indent=2)
        elif source.startswith("judge:"):
            text[field] = json.dumps(verdicts[source.split(":", 1)[1]], ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"unknown input source {source!r} for {field}")
    return text


def run_judges(skill, output_dir, input_dir, reference, client, config, allow_uncalibrated):
    """Run every judge of the skill in registry order. Uncalibrated judges are skipped, not run."""
    verdicts = {}
    for entry in load_registry().get(skill, []):
        name = entry["judge"]
        inputs = resolve_inputs(entry, output_dir, input_dir, reference, verdicts)
        try:
            verdicts[name] = run_judge(skill, name, inputs, client, config, allow_uncalibrated)
        except UncalibratedJudge as e:
            verdicts[name] = {"skipped": str(e)}
    return verdicts


def run_one(skill, case, input_dir, reference, run_dir, agent, client, config, allow_uncalibrated, dry_run):
    """One run of one case. Returns the score record."""
    run_dir.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return {"skill": skill, "case": case, "dry_run": True}

    sandbox = make_sandbox(claude_dir(config), input_dir)
    ok, log = agent(sandbox, skill, config["agent"]["command"], config["agent"]["timeout_seconds"])
    (run_dir / "agent.log").write_text(log)
    output_dir = run_dir / "output"
    files = collect_output(sandbox, output_dir) if ok else []

    static = run_static(skill, output_dir, input_dir) if files else {
        "checks": {}, "sensitive": {"passed": True, "output": ""}, "passed": False}
    verdicts = {}
    if files:
        verdicts = run_judges(skill, output_dir, input_dir, reference, client, config, allow_uncalibrated)
    judge_values = {k: v for k, v in verdicts.items() if "skipped" not in v}
    score = run_score(skill, static, judge_values) if files else 0.0

    (run_dir / "static.json").write_text(json.dumps(static, indent=2, ensure_ascii=False))
    (run_dir / "judges.json").write_text(json.dumps(verdicts, indent=2, ensure_ascii=False))
    record = {"skill": skill, "case": case, "agent_ok": ok, "files": files,
              "static_passed": static["passed"], "score": score,
              "judges_skipped": sorted(k for k, v in verdicts.items() if "skipped" in v)}
    (run_dir / "score.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    return record


def write_summary(stamp_dir, records):
    """summary.csv: one row per run. report.md: one table per skill, with mean and spread per case."""
    with open(stamp_dir / "summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["skill", "case", "run", "agent_ok", "static_passed", "score", "judges_skipped"])
        for r in records:
            w.writerow([r["skill"], r["case"], r.get("run", ""), r.get("agent_ok", ""),
                        r.get("static_passed", ""), r.get("score", ""), ";".join(r.get("judges_skipped", []))])

    lines = ["# Evaluation report", "", f"Generated {datetime.now():%Y-%m-%d %H:%M}.", ""]
    skipped = sorted({j for r in records for j in r.get("judges_skipped", [])})
    if skipped:
        lines += ["**Judges not calibrated, not run:** " + ", ".join(skipped) + ". "
                  "Scores below use the static checks and the calibrated judges only.", ""]
    for skill in sorted({r["skill"] for r in records}):
        lines += [f"## {skill}", "", "| Case | Runs | Mean score | Spread | Static passed |", "|---|---|---|---|---|"]
        for case in sorted({r["case"] for r in records if r["skill"] == skill}):
            rs = [r for r in records if r["skill"] == skill and r["case"] == case]
            s = summarize([r["score"] for r in rs])
            mean = "-" if s["mean"] is None else f"{s['mean']:.2f}"
            spread = "-" if s["stdev"] is None else f"{s['stdev']:.2f}"
            passed = sum(bool(r.get("static_passed")) for r in rs)
            lines.append(f"| {case} | {s['runs']} | {mean} | {spread} | {passed}/{len(rs)} |")
        lines.append("")
    (stamp_dir / "report.md").write_text("\n".join(lines))


def load_scores(run, skill):
    """{case: [score per run]} of one skill in an earlier run folder."""
    out = {}
    for p in sorted((Path(run) / skill).rglob("score.json")):
        rec = json.loads(p.read_text())
        out.setdefault(rec["case"], []).append(rec["score"])
    return out


def compare_runs(old_run, records, threshold):
    """Case by case: the change of the mean score against the earlier run.

    A drop is a regression when it is larger than the spread of either run and than `threshold`
    (config regression_threshold). The threshold stops a run with no spread from flagging noise.
    Returns rows (skill, case, old_mean, new_mean, delta, verdict).
    """
    rows = []
    for skill in sorted({r["skill"] for r in records}):
        old = load_scores(old_run, skill)
        for case in sorted({r["case"] for r in records if r["skill"] == skill}):
            new = summarize([r["score"] for r in records if r["skill"] == skill and r["case"] == case])
            if case not in old:
                rows.append((skill, case, None, new["mean"], None, "new case"))
                continue
            prev = summarize(old[case])
            if prev["mean"] is None or new["mean"] is None:
                rows.append((skill, case, prev["mean"], new["mean"], None, "no score"))
                continue
            delta = new["mean"] - prev["mean"]
            band = max(prev["stdev"], new["stdev"], threshold)
            verdict = "regression" if delta < -band else "improved" if delta > band else "same"
            rows.append((skill, case, prev["mean"], new["mean"], delta, verdict))
    return rows


def print_comparison(rows):
    print("comparison with the earlier run:")
    for skill, case, old, new, delta, verdict in rows:
        fmt = lambda v: "-" if v is None else f"{v:.2f}"  # noqa: E731
        print(f"  {skill}/{case}: {fmt(old)} -> {fmt(new)} ({fmt(delta)}) {verdict}")


def write_comparison(stamp_dir, old_run, rows):
    lines = ["", f"## Comparison with {Path(old_run).name}", "",
             "| Skill | Case | Earlier | Now | Change | Verdict |", "|---|---|---|---|---|---|"]
    for skill, case, old, new, delta, verdict in rows:
        fmt = lambda v: "-" if v is None else f"{v:.2f}"  # noqa: E731
        lines.append(f"| {skill} | {case} | {fmt(old)} | {fmt(new)} | {fmt(delta)} | {verdict} |")
    with open(stamp_dir / "report.md", "a") as f:
        f.write("\n".join(lines) + "\n")


def estimate(skills, runs, config, allow_uncalibrated):
    """Count the agent and judge calls a run would make, per skill. Calls nothing.

    Judge calls: one per judge that will run per run, times up to `retries + 1` attempts (the worst case).
    Cost: only if config.estimate has a price; the prices are the owner's, not set here.
    """
    from judges.judge_client import judge_is_calibrated
    prices = config.get("estimate") or {}
    rows = []
    for skill in skills:
        cases = list_cases(skill)
        judges_run = [e["judge"] for e in load_registry().get(skill, [])
                      if allow_uncalibrated or judge_is_calibrated(skill, e["judge"])]
        n_runs = len(cases) * runs
        agent_calls = n_runs
        judge_calls = n_runs * len(judges_run)
        judge_worst = judge_calls * (config["judge"]["retries"] + 1)
        row = {"skill": skill, "cases": len(cases), "runs": n_runs, "agent_calls": agent_calls,
               "judges_run": judges_run, "judge_calls": judge_calls, "judge_calls_worst": judge_worst}
        if prices.get("agent_cost_per_run") is not None:
            row["agent_cost"] = agent_calls * prices["agent_cost_per_run"]
        if prices.get("judge_cost_per_call") is not None:
            row["judge_cost"] = judge_worst * prices["judge_cost_per_call"]
        rows.append(row)
    return rows


def print_estimate(rows):
    print(f"{'skill':20} {'cases':>5} {'runs':>5} {'agent':>6} {'judge':>6} {'judge(worst)':>12}  judges")
    for r in rows:
        print(f"{r['skill']:20} {r['cases']:>5} {r['runs']:>5} {r['agent_calls']:>6} "
              f"{r['judge_calls']:>6} {r['judge_calls_worst']:>12}  {', '.join(r['judges_run']) or '-'}")
    tot_agent = sum(r["agent_calls"] for r in rows)
    tot_judge = sum(r["judge_calls"] for r in rows)
    print(f"total: {tot_agent} agent calls, {tot_judge} judge calls (up to {sum(r['judge_calls_worst'] for r in rows)} with retries)")
    if any("agent_cost" in r for r in rows):
        cost = sum(r.get("agent_cost", 0) + r.get("judge_cost", 0) for r in rows)
        print(f"estimated cost: {cost:.2f} (config.estimate prices; worst case for judges)")
    else:
        print("no prices in config.yaml (estimate:), so no cost is shown")


def main(argv=None, agent=run_agent, client=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--skill", default="all", help="skill name or 'all'")
    p.add_argument("--case", help="run only this case")
    p.add_argument("--runs", type=int, help="runs per case (default: config runs_per_test)")
    p.add_argument("--allow-uncalibrated", action="store_true", help="development only")
    p.add_argument("--dry-run", action="store_true", help="list the runs; call no agent and no judge")
    p.add_argument("--estimate", action="store_true", help="count the agent and judge calls; call nothing")
    p.add_argument("--compare", metavar="RUN", help="earlier run (folder or stamp) to compare with; exit 1 on regression")
    p.add_argument("--e2e", action="store_true", help="not implemented yet (plan step 10)")
    args = p.parse_args(argv)

    if args.e2e:
        print("--e2e is not implemented yet (eval-plan.md, step 10).")
        return 2
    config = load_config()
    skills = SKILLS if args.skill == "all" else [args.skill]
    runs = args.runs or config["runs_per_test"]
    if args.estimate:
        print_estimate(estimate(skills, runs, config, args.allow_uncalibrated))
        return 0
    stamp_dir = RESULTS / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")

    records = []
    for skill in skills:
        cases = [c for c in list_cases(skill) if not args.case or c[0] == args.case]
        if not cases:
            print(f"{skill}: no cases in datasets/{skill}/ (reference.json and cases/<case>/input/ needed)")
            continue
        if client is None and not args.dry_run:
            from judges.judge_client import AnthropicClient
            client = AnthropicClient()
        for case, input_dir, reference in cases:
            for n in range(1, runs + 1):
                run_dir = stamp_dir / skill / case / f"run_{n}"
                rec = run_one(skill, case, input_dir, reference, run_dir, agent, client, config,
                              args.allow_uncalibrated, args.dry_run)
                rec["run"] = n
                records.append(rec)
                print(f"{skill}/{case}/run_{n}: " + ("dry run" if args.dry_run else
                      f"score={rec['score']:.2f} static={rec['static_passed']}"))
    if records and not args.dry_run:
        stamp_dir.mkdir(parents=True, exist_ok=True)
        write_summary(stamp_dir, records)
        print(f"report: {stamp_dir / 'report.md'}")
        if args.compare:
            old = Path(args.compare) if Path(args.compare).exists() else RESULTS / "runs" / args.compare
            rows = compare_runs(old, records, config["regression_threshold"])
            write_comparison(stamp_dir, old, rows)
            print_comparison(rows)
            if any(r[-1] == "regression" for r in rows):
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
