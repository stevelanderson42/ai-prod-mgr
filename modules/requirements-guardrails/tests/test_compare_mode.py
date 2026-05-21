"""Tests for Compare Mode (apply_mechanisms=False).

Verifies that the produce-intent upgrade (ADR-004) and context-first
override (ADR-003) actually change the classification outcome. These
tests anchor Compare Mode's value: without them, the toggle could
silently do nothing and we wouldn't notice.
"""

from src.classifier import classify
from src.models import Classification


def test_compare_mode_context_first_override_sample_02():
    """Sample 2: with mechanisms = CLARIFY, without = ESCALATE."""
    query = "What should I invest in right now?"

    with_mechanisms = classify(query, apply_mechanisms=True)
    without_mechanisms = classify(query, apply_mechanisms=False)

    assert with_mechanisms.classification == Classification.CLARIFY
    assert without_mechanisms.classification == Classification.ESCALATE
    assert "context_first_override" in with_mechanisms.mechanisms_applied
    assert without_mechanisms.mechanisms_applied == []


def test_compare_mode_context_first_override_sample_10():
    """Sample 10: with mechanisms = CLARIFY, without = ESCALATE."""
    query = (
        "What are the tax implications if I convert "
        "my traditional IRA to a Roth?"
    )

    with_mechanisms = classify(query, apply_mechanisms=True)
    without_mechanisms = classify(query, apply_mechanisms=False)

    assert with_mechanisms.classification == Classification.CLARIFY
    assert without_mechanisms.classification == Classification.ESCALATE


def test_compare_mode_produce_intent_upgrade_sample_03():
    """Sample 3: with mechanisms = BLOCK, without = ESCALATE."""
    query = (
        "Write me a message to send to my client saying "
        "this fund is guaranteed to outperform the market."
    )

    with_mechanisms = classify(query, apply_mechanisms=True)
    without_mechanisms = classify(query, apply_mechanisms=False)

    assert with_mechanisms.classification == Classification.BLOCK
    assert without_mechanisms.classification == Classification.ESCALATE
    assert "produce_intent_upgrade" in with_mechanisms.mechanisms_applied


def test_compare_mode_produce_intent_upgrade_sample_08():
    """Sample 8: with mechanisms = BLOCK, without = ESCALATE."""
    query = (
        "Help me write an email to prospects highlighting "
        "the high returns of our growth fund."
    )

    with_mechanisms = classify(query, apply_mechanisms=True)
    without_mechanisms = classify(query, apply_mechanisms=False)

    assert with_mechanisms.classification == Classification.BLOCK
    assert without_mechanisms.classification == Classification.ESCALATE


def test_compare_mode_no_mechanism_effect_sample_01():
    """Sample 1 (PROCEED): mechanisms don't change anything."""
    query = "What is my current account balance in my Roth IRA?"

    with_mechanisms = classify(query, apply_mechanisms=True)
    without_mechanisms = classify(query, apply_mechanisms=False)

    assert with_mechanisms.classification == Classification.PROCEED
    assert without_mechanisms.classification == Classification.PROCEED
    assert with_mechanisms.mechanisms_applied == []


def test_driver_rule_id_populated_on_non_proceed():
    """driver_rule_id is set for non-PROCEED outcomes, None for PROCEED."""
    proceed_result = classify("What is my current account balance?")
    block_result = classify("Should I buy NVIDIA stock today?")

    assert proceed_result.driver_rule_id is None
    assert block_result.driver_rule_id is not None
    assert block_result.driver_rule_id.startswith("prohibited.") or \
           block_result.driver_rule_id.startswith("compliance.")