"""The agent's sandbox never contains eval/ or the reference data (eval-plan.md, principle 3)."""
import sys
from pathlib import Path

import pytest

EVAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL))

from runner.sandbox import assert_no_eval, make_sandbox  # noqa: E402


def test_sandbox_has_claude_and_input_only(tmp_path):
    claude = tmp_path / ".claude"
    (claude / "skills").mkdir(parents=True)
    (claude / "skills" / "SKILL.md").write_text("x")
    inp = tmp_path / "case" / "input"
    inp.mkdir(parents=True)
    (inp / "model_card.md").write_text("y")

    root = make_sandbox(claude, inp)
    names = {p.relative_to(root).as_posix() for p in root.rglob("*")}
    assert ".claude/skills/SKILL.md" in names
    assert "input/model_card.md" in names
    assert "output" in names
    assert not any(n.startswith("eval") for n in names)


def test_reference_file_in_input_is_refused(tmp_path):
    (tmp_path / "reference.json").write_text("{}")
    with pytest.raises(RuntimeError):
        assert_no_eval(tmp_path)


def test_eval_folder_inside_sandbox_is_refused(tmp_path):
    (tmp_path / "eval").mkdir()
    # Simulate a leak: the check compares against the real EVAL folder, so use the real path.
    inside = EVAL / "config.yaml"
    assert inside.exists()
    from runner import sandbox as sb
    original = sb.EVAL_DIR
    try:
        sb.EVAL_DIR = tmp_path
        with pytest.raises(RuntimeError):
            sb.assert_no_eval(tmp_path)
    finally:
        sb.EVAL_DIR = original
