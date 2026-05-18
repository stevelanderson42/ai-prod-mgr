"""
YAML rule evaluator — loads rule configs at module import time and
evaluates queries against keyword and regex rules.

For heuristic-type rules, returns metadata (rule ID, heuristic function name)
so the classifier orchestrator knows which Python function to call.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from src.models import Classification, Category, TriggeredRule


# ── Module-level config loading ──────────────────────────────────

_CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_config(filename: str) -> dict:
    """Load and return a single YAML config file."""
    with open(_CONFIG_DIR / filename) as f:
        return yaml.safe_load(f)


# Loaded once at import time — these are module-level constants.
COMPLIANCE_CONFIG = _load_config("compliance.yaml")
SUITABILITY_CONFIG = _load_config("suitability.yaml")
PROHIBITED_CONFIG = _load_config("prohibited.yaml")

# Explicit mapping from Category enum to loaded config dict.
# Category.NONE is intentionally absent — calling evaluate_category
# with NONE is a caller bug.
_CATEGORY_CONFIG_MAP: dict[Category, dict] = {
    Category.COMPLIANCE: COMPLIANCE_CONFIG,
    Category.SUITABILITY: SUITABILITY_CONFIG,
    Category.PROHIBITED: PROHIBITED_CONFIG,
}


# ── Data structures ──────────────────────────────────────────────


@dataclass
class RuleMatch:
    """Result of evaluating a single YAML rule against a query.

    Attributes:
        rule_id: e.g. "compliance.guarantee_language"
        description: Human-readable from YAML.
        classification: The rule's default classification.
        category: Which category config it came from.
        is_heuristic: True if detection.type == "heuristic".
        produce_intent_upgrade: The upgraded classification if
            produce-intent is detected, or None.
        missing_context: From YAML missing_context field (suitability rules).
    """

    rule_id: str
    description: str
    classification: Classification
    category: Category
    is_heuristic: bool
    produce_intent_upgrade: Classification | None = None
    missing_context: list[str] = field(default_factory=list)


# ── Pattern matching ─────────────────────────────────────────────


def _evaluate_keyword_rule(query: str, patterns: list[str]) -> bool:
    """Return True if any keyword pattern is found in the query.

    Both the query and each pattern are normalized to lowercase
    before comparison so matching is case-insensitive.
    """
    query_lower = query.lower()
    return any(pattern.lower() in query_lower for pattern in patterns)


def _evaluate_regex_rule(query: str, patterns: list[str]) -> bool:
    """Return True if any regex pattern matches within the query.

    Each pattern is compiled with re.IGNORECASE for
    case-insensitive matching.
    """
    return any(re.search(pattern, query, re.IGNORECASE) for pattern in patterns)


# ── Category evaluation ──────────────────────────────────────────


def evaluate_category(query: str, category: Category) -> list[RuleMatch]:
    """Evaluate all rules in a category against the query.

    For keyword/regex rules: returns a RuleMatch only if the rule fired.
    For heuristic rules: always returns a RuleMatch with is_heuristic=True,
    letting the orchestrator decide whether the heuristic function fires.

    Args:
        query: The user's input text.
        category: Which rule category to evaluate (COMPLIANCE,
            SUITABILITY, or PROHIBITED).

    Returns:
        List of RuleMatch objects for rules that triggered (keyword/regex)
        or need heuristic evaluation (heuristic type).

    Raises:
        ValueError: If called with Category.NONE — this indicates a bug
            in the caller since NONE means "no guardrail triggered."
    """
    if category == Category.NONE:
        raise ValueError(
            "evaluate_category called with Category.NONE. "
            "NONE means no guardrail triggered — there are no rules to evaluate."
        )

    config = _CATEGORY_CONFIG_MAP[category]
    matches: list[RuleMatch] = []

    for rule in config["rules"]:
        detection = rule["detection"]
        detection_type = detection["type"]

        # Build common RuleMatch fields
        rule_classification = Classification(rule["classification"])
        upgrade_value = rule.get("produce_intent_upgrade")
        produce_upgrade = Classification(upgrade_value) if upgrade_value else None
        missing_ctx = rule.get("missing_context", [])

        if detection_type == "heuristic":
            # Always return heuristic rules — the orchestrator will
            # call the corresponding Python function to decide.
            matches.append(
                RuleMatch(
                    rule_id=rule["id"],
                    description=rule["description"].strip(),
                    classification=rule_classification,
                    category=category,
                    is_heuristic=True,
                    produce_intent_upgrade=produce_upgrade,
                    missing_context=missing_ctx,
                )
            )
        elif detection_type == "keyword":
            if _evaluate_keyword_rule(query, detection["patterns"]):
                matches.append(
                    RuleMatch(
                        rule_id=rule["id"],
                        description=rule["description"].strip(),
                        classification=rule_classification,
                        category=category,
                        is_heuristic=False,
                        produce_intent_upgrade=produce_upgrade,
                        missing_context=missing_ctx,
                    )
                )
        elif detection_type == "regex":
            if _evaluate_regex_rule(query, detection["patterns"]):
                matches.append(
                    RuleMatch(
                        rule_id=rule["id"],
                        description=rule["description"].strip(),
                        classification=rule_classification,
                        category=category,
                        is_heuristic=False,
                        produce_intent_upgrade=produce_upgrade,
                        missing_context=missing_ctx,
                    )
                )

    return matches


# ── Config lookup ────────────────────────────────────────────────


def get_rule_config(rule_id: str) -> dict | None:
    """Look up the raw YAML config dict for a specific rule by ID.

    Used by heuristic functions to read signal lists from the YAML
    (e.g., benefit_signals, context_signals) rather than hardcoding
    values that are already in the config files.

    Args:
        rule_id: Rule identifier in "category.rule_name" format,
            e.g. "compliance.unbalanced_claims".

    Returns:
        The raw rule dict from YAML, or None if the rule_id is not found.
    """
    for config in _CATEGORY_CONFIG_MAP.values():
        for rule in config["rules"]:
            if rule["id"] == rule_id:
                return rule
    return None
