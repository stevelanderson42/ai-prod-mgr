"""
Output contract for the Requirements Guardrails classifier.

Defines the structured decision returned for every classified request.
These dataclasses are the module's public interface — downstream systems
(Compliance Retrieval Assistant, audit logging) consume these structures.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4


class Classification(Enum):
    """Routing decision with strict priority ordering.

    Priority: BLOCK > ESCALATE > CLARIFY > PROCEED.
    When multiple rules fire, the highest-priority classification wins.
    """

    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"
    CLARIFY = "CLARIFY"
    PROCEED = "PROCEED"

    @property
    def priority(self) -> int:
        """Return comparable integer for priority routing.

        Higher value = higher priority. Usage:
            max(classifications, key=lambda c: c.priority)
        """
        return {
            Classification.PROCEED: 0,
            Classification.CLARIFY: 1,
            Classification.ESCALATE: 2,
            Classification.BLOCK: 3,
        }[self]


class Category(Enum):
    """Guardrail category that triggered the routing decision.

    Each value corresponds to a rule module under src/rules/.
    'none' indicates no guardrail triggered (PROCEED).
    """

    COMPLIANCE = "compliance"
    SUITABILITY = "suitability"
    PROHIBITED = "prohibited"
    NONE = "none"


@dataclass(frozen=True)
class TriggeredRule:
    """A single rule that fired during classification.

    Attributes:
        rule_id: Identifier in {category}.{rule_name} format.
                 Example: 'compliance.guarantee_language'
        description: Human-readable explanation of what the rule detects.
    """

    rule_id: str
    description: str


@dataclass
class GuardrailResult:
    """The complete output contract for a single classification request.

    Every request produces exactly one GuardrailResult, regardless of
    whether it proceeds, is clarified, escalated, or blocked. This
    structure is written to the audit log and returned to the caller.

    Attributes:
        request_id: Unique identifier for this classification request.
        timestamp: ISO-8601 timestamp of when classification occurred.
        classification: Routing decision (BLOCK, ESCALATE, CLARIFY, PROCEED).
        category: Primary guardrail category that drove the decision.
        decision_reason: Human-readable rationale for the routing decision.
        next_action: Description of what happens next for the caller.
        triggered_rules: List of all rules that fired, across all categories.
                         May contain rules from multiple categories even when
                         only one determines the final classification.
        missing_context: Fields the user must provide (CLARIFY only).
                         Empty list for non-CLARIFY decisions.
    """

    classification: Classification
    category: Category
    decision_reason: str
    next_action: str
    triggered_rules: list[TriggeredRule] = field(default_factory=list)
    missing_context: list[str] = field(default_factory=list)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        """Serialize to a plain dict for JSON output and audit logging."""
        result = asdict(self)
        result["classification"] = self.classification.value
        result["category"] = self.category.value
        return result
