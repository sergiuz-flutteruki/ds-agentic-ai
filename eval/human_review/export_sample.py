"""Samples runs for human review (config.yaml: human_review_sample) into a CSV sheet.

  python3 eval/human_review/export_sample.py results/runs/<stamp>
The reviewer fills `human_pass` and `notes`. Labels go to judges/calibration/cases/... by hand.
"""
import csv
import json
import math
import random
import sys
from pathlib import Path

import yaml

EVAL = Path(__file__).resolve().parents[1]


def main(stamp_dir):
    rate = yaml.safe_load((EVAL / "config.yaml").read_text())["human_review_sample"]
    stamp = Path(stamp_dir)
    rows = [json.loads(p.read_text()) | {"run_dir": str(p.parent)} for p in sorted(stamp.rglob("score.json"))]
    k = max(1, math.ceil(len(rows) * rate)) if rows else 0
    sample = random.Random(0).sample(rows, k)
    out = EVAL / "human_review" / "sheets" / f"{stamp.name}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["skill", "case", "run", "output_dir", "automatic_score", "human_pass", "notes"])
        for r in sample:
            w.writerow([r["skill"], r["case"], r["run"], r["run_dir"] + "/output", r["score"], "", ""])
    print(f"{len(sample)} of {len(rows)} runs -> {out}")


if __name__ == "__main__":
    main(sys.argv[1])
