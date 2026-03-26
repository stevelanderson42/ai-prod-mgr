import json
import re


def parse_json_response(raw: str) -> dict:
    """Parse JSON from an LLM response, stripping markdown code fences if present."""
    text = raw.strip()
    # Remove ```json ... ``` or ``` ... ``` wrappers
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)
