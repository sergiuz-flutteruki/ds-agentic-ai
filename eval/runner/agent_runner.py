"""Runs one writer agent in a sandbox with `claude -p` and copies its output back."""
import shutil
import subprocess
from pathlib import Path


def build_task(skill):
    """The prompt the writer gets. The input is in ./input, the result goes to ./output."""
    # TODO(owner): check that this prompt starts the skill the way /dsdoc does in a real repo.
    return (f"Use the {skill} skill on the documents in ./input. "
            "Write the result to ./output and do not read anything outside this folder.")


def run_agent(sandbox, skill, command, timeout):
    """Run the writer in the sandbox. Returns (ok, stdout+stderr)."""
    cmd = list(command) + [build_task(skill)]
    try:
        r = subprocess.run(cmd, cwd=sandbox, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s"
    return r.returncode == 0, (r.stdout + r.stderr)


def collect_output(sandbox, dest):
    """Copy the writer's output/ folder to dest (a results folder). Returns the list of files."""
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(Path(sandbox) / "output", dest)
    return sorted(str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file())
