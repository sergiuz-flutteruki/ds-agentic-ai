"""Sandbox for one agent run: a copy of .claude/ and the test input, nothing else.

The agent never sees eval/, so reference data and calibration labels cannot leak into its prompt.
"""
import shutil
import tempfile
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parents[1]


def make_sandbox(claude_dir, input_dir):
    """Create a temporary folder with .claude/, input/ and an empty output/. Returns its path."""
    claude_dir, input_dir = Path(claude_dir).resolve(), Path(input_dir).resolve()
    root = Path(tempfile.mkdtemp(prefix="dsdoc-sandbox-"))
    shutil.copytree(claude_dir, root / ".claude", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(input_dir, root / "input")
    (root / "output").mkdir()
    assert_no_eval(root)
    return root


def assert_no_eval(root):
    """Refuse a sandbox that contains the evaluation code or its data."""
    eval_dir = EVAL_DIR.resolve()
    for p in Path(root).rglob("*"):
        if p.resolve() == eval_dir or eval_dir in p.resolve().parents:
            raise RuntimeError(f"sandbox leak: {p} is inside eval/")
        if p.name in {"reference.json", "human_labels"} or p.name.endswith(".jsonl") and "examples" in p.parts:
            raise RuntimeError(f"sandbox leak: reference or label file {p}")
