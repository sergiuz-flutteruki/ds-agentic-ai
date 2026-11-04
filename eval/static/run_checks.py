"""Runs the existing static checks of a skill on one writer output. Nothing is reimplemented here.

The scripts are called from .claude/skills/ exactly as the reviewers call them: bash for .sh,
cwd = the script's folder, absolute paths. Exit 0 = pass, anything else = fail.
Plan: eval-plan.md, sections 5 and 7.
"""
import json
import subprocess
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parents[1]
SKILLS_DIR = (EVAL_DIR / "..").resolve() / ".claude" / "skills"
SENSITIVE = SKILLS_DIR / "dsdoc" / "scripts" / "check_sensitive.sh"

# The document the writer must produce, per skill (name inside output/).
OUTPUT_DOC = {
    "business_context": "business_context.md",
    "model_card": "model_card.md",
    "stake_summary": "stake_summary.md",
}


def run_script(script, args, timeout=60):
    """Run one script; return {passed, output}. Scripts are run the way the reviewers run them."""
    script = Path(script)
    cmd = (["bash", str(script)] if script.suffix == ".sh" else ["python3", str(script)])
    cmd += [str(Path(a).resolve()) for a in args]
    r = subprocess.run(cmd, cwd=script.parent, capture_output=True, text=True, timeout=timeout)
    return {"passed": r.returncode == 0, "output": (r.stdout + r.stderr).strip()}


def script_calls(skill, output_dir, input_dir):
    """The (name, script, args) of each static check for one skill and case."""
    out, inp = Path(output_dir), Path(input_dir)
    yaml_arg = [inp / "dsdoc.yaml"] if (inp / "dsdoc.yaml").exists() else []
    if skill == "business_context":
        sources = sorted(p for p in inp.rglob("*") if p.is_file())
        return [("check.sh", SKILLS_DIR / "dsdoc-business-context" / "check.sh",
                 [out / OUTPUT_DOC[skill], *sources])]
    if skill == "model_card":
        return [("check.sh", SKILLS_DIR / "dsdoc-model-card" / "check.sh",
                 [out / OUTPUT_DOC[skill], *yaml_arg])]
    if skill == "stake_summary":
        return [("check.sh", SKILLS_DIR / "dsdoc-stake-summary" / "check.sh",
                 [out / OUTPUT_DOC[skill], inp / "model_card.md", *yaml_arg])]
    if skill == "code_doc":
        # One call per changed file: original (input/) and documented (output/).
        calls = []
        for changed in sorted(out.rglob("*.py")):
            original = inp / changed.relative_to(out)
            calls.append((f"check_unchanged:{changed.name}",
                          SKILLS_DIR / "dsdoc-code-doc" / "scripts" / "check_unchanged.py",
                          [original, changed]))
        return calls
    raise KeyError(f"no static checks for {skill}")


def run_static(skill, output_dir, input_dir):
    """Returns {checks: {name: {passed, output}}, sensitive: {passed, output}, passed}."""
    checks = {}
    for name, script, args in script_calls(skill, output_dir, input_dir):
        checks[name] = run_script(script, args)

    # Sensitive-data check on every text output. A failure here zeroes the test (see scoring).
    sensitive = {"passed": True, "output": ""}
    for doc in sorted(Path(output_dir).rglob("*.md")):
        res = run_script(SENSITIVE, [doc])
        if not res["passed"]:
            sensitive = {"passed": False, "output": f"{doc.name}: {res['output']}"}
            break

    passed = sensitive["passed"] and all(c["passed"] for c in checks.values())
    return {"checks": checks, "sensitive": sensitive, "passed": passed}


if __name__ == "__main__":
    import sys

    print(json.dumps(run_static(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2, ensure_ascii=False))
