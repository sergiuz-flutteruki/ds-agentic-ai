"""Shared judge client: builds the judge input from the registry, calls the model, validates the JSON.

A judge is one question with one schema. It runs only when its prompt is calibrated
(frontmatter `calibrated` is set) or when the caller passes allow_uncalibrated=True (development only).
"""
import json
import re
from pathlib import Path

import jsonschema
import yaml

JUDGES_DIR = Path(__file__).resolve().parent


class UncalibratedJudge(RuntimeError):
    pass


def load_registry():
    return yaml.safe_load((JUDGES_DIR / "registry.yaml").read_text())


def find_entry(skill, judge):
    for entry in load_registry().get(skill, []):
        if entry["judge"] == judge:
            return entry
    raise KeyError(f"no judge {skill}/{judge} in registry.yaml")


def parse_prompt(path):
    """Split the YAML frontmatter from the prompt body. Returns (meta, body)."""
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path}: missing frontmatter")
    return yaml.safe_load(m.group(1)), m.group(2)


def build_user_message(inputs):
    """Each input field goes into its own XML tag."""
    return "\n".join(f"<{name}>\n{text}\n</{name}>" for name, text in inputs.items())


def load_schema(entry):
    return json.loads((JUDGES_DIR / entry["schema"]).read_text())


def load_examples(entry):
    """Human-scored examples from examples/<skill>/<judge>.jsonl, one JSON object per line."""
    path = JUDGES_DIR / "examples" / Path(entry["prompt"]).parent.name / (Path(entry["prompt"]).stem + ".jsonl")
    if not path.exists():
        return ""
    return "\n".join(line for line in path.read_text().splitlines() if line.strip())


def validate(payload, schema):
    """Raise jsonschema.ValidationError when the payload does not follow the schema."""
    jsonschema.validate(payload, schema)
    return payload


def extract_json(text):
    """The model should answer JSON only; tolerate a fenced block around it."""
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    return json.loads(m.group(1) if m else text)


def run_judge(skill, judge, inputs, client, config, allow_uncalibrated=False):
    """Run one judge. `inputs` maps each registry field name to its text.

    `client` is an object with `.complete(system, user, model, temperature, max_tokens) -> str`.
    Returns the validated verdict dict with `_prompt_version` and `_attempts` added.
    """
    entry = find_entry(skill, judge)
    meta, body = parse_prompt(JUDGES_DIR / entry["prompt"])
    if meta.get("calibrated") is None and not allow_uncalibrated:
        raise UncalibratedJudge(f"{skill}/{judge} is not calibrated (calibrated: null)")

    body = body.replace("{{examples}}", load_examples(entry) or "(none yet)")
    schema = load_schema(entry)
    user = build_user_message(inputs) + "\n\nSchema:\n" + json.dumps(schema)
    judge_cfg = config["judge"]
    last_error = None
    for attempt in range(1 + judge_cfg["retries"]):
        raw = client.complete(body, user, judge_cfg["model"], judge_cfg["temperature"], judge_cfg["max_tokens"])
        try:
            verdict = validate(extract_json(raw), schema)
            verdict["_prompt_version"] = meta.get("version")
            verdict["_attempts"] = attempt + 1
            return verdict
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            last_error = f"{type(e).__name__}: {e}"
    raise ValueError(f"{skill}/{judge}: no valid JSON after {attempt + 1} attempts ({last_error})")


class AnthropicClient:
    """Real model calls. The SDK and ANTHROPIC_API_KEY are needed only here."""

    def __init__(self):
        import anthropic  # imported here so the tests run without the SDK

        self._client = anthropic.Anthropic()

    def complete(self, system, user, model, temperature, max_tokens):
        msg = self._client.messages.create(
            model=model, system=system, temperature=temperature, max_tokens=max_tokens,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in msg.content if block.type == "text")


def judge_is_calibrated(skill, judge):
    """True when the judge's prompt has a calibration date in its frontmatter."""
    entry = find_entry(skill, judge)
    meta, _ = parse_prompt(JUDGES_DIR / entry["prompt"])
    return meta.get("calibrated") is not None
