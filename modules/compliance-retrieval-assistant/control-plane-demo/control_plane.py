#!/usr/bin/env python3
"""
Pre-invocation Control Plane Demo
- Classify input deterministically
- Decide: ALLOW / ESCALATE / BLOCK
- Only invoke LLM if ALLOW
- Emit audit trail

Run (classification only, no API key needed):
  python control_plane.py "Your query here"

Run with LLM invocation:
  export OPENAI_API_KEY="..."
  python control_plane.py "Summarize SR 11-7 model risk management in 5 bullets"

Dry run (show classification without LLM call even if allowed):
  python control_plane.py --dry-run "Your query here"

Notes:
- This demo intentionally blocks requests for individualized medical/legal/financial advice.
- It demonstrates governance-by-design, not model capability.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Literal

Decision = Literal["ALLOW", "ESCALATE", "BLOCK"]

# -----------------------------
# 1) Policy Configuration
# -----------------------------
# Keeping policies as explicit dictionaries makes them easy to explain in interviews:
# "Here's the policy, here's the enforcement."

POLICIES = {
    "self_harm": {
        "decision": "BLOCK",
        "patterns": [
            r"\bkill myself\b",
            r"\bsuicide\b",
            r"\bhurt myself\b",
            r"\bself[- ]?harm\b",
        ],
        "reason": "Self-harm intent or ideation detected",
        "response": (
            "I'm really sorry you're going through this. I can't help with self-harm. "
            "If you're in immediate danger, call your local emergency number right now. "
            "If you're in the U.S., you can call or text 988 (Suicide & Crisis Lifeline)."
        ),
    },
    "pii_request": {
        "decision": "BLOCK",
        "patterns": [
            r"\bssn\b",
            r"\bsocial security\b",
            r"\bdate of birth\b",
            r"\bdob\b",
            r"\bmy address\b",
            r"\bphone number\b",
            r"\bemail address\b",
            r"\bmrn\b",  # medical record number
        ],
        "reason": "PII-sensitive content requested or provided",
        "response": (
            "I can't help with requests involving sensitive personal information. "
            "If you need help, share a redacted version and I can assist with general guidance."
        ),
    },
    "medical_advice": {
        "decision": "BLOCK",
        "patterns": [
            r"\bshould i (take|stop|change|increase|decrease)\b",
            r"\bshould my (patient|mom|dad|aunt|uncle|friend|husband|wife)\b",
            r"\bwhat should i do about my\b",
            r"\bdo i need to (see|call|visit)\b",
            r"\bcan i stop taking\b",
            r"\bchange my (medication|dosage|prescription)\b",
            r"\bstop taking my\b",
            r"\bis it safe for me to\b",
        ],
        "reason": "Individualized medical advice request detected",
        "response": (
            "I can't provide individualized medical advice. "
            "If this is about a real situation, it should be reviewed by a licensed clinician. "
            "I can share general, non-personal educational information about the topic if helpful."
        ),
    },
    "clinical_decision_support": {
        "decision": "ESCALATE",
        "patterns": [
            r"\bdiagnos(e|is|tic)\b",
            r"\btreatment plan\b",
            r"\bmedication interact(ion|s)\b",
            r"\bdrug interact(ion|s)\b",
            r"\bcontraindicat(ed|ion)\b",
            r"\bprescri(be|ption)\b",
            r"\bwarfarin\b",
            r"\binsulin dosing\b",
        ],
        "reason": "Clinical topic detected; requires additional validation or clinician workflow",
        "response": (
            "This request touches a clinical decision-support area. "
            "In a production system, it would route to a clinician review workflow or validated knowledge pathway. "
            "I can provide general educational information (not medical advice) if helpful."
        ),
    },
}

POLICY_VERSION = "demo-policy-v1"

# -----------------------------
# 2) Classification Engine
# -----------------------------

@dataclass
class Classification:
    decision: Decision
    label: str
    reasons: List[str]
    triggered_pattern: str | None
    policy_version: str = POLICY_VERSION


def classify(query: str) -> Classification:
    """
    Evaluate query against policies in priority order.
    Returns first matching policy or ALLOW if none match.
    """
    q = query.strip().lower()

    # Evaluate policies in order (order matters for priority)
    for label, policy in POLICIES.items():
        for pattern in policy["patterns"]:
            if re.search(pattern, q, flags=re.IGNORECASE):
                return Classification(
                    decision=policy["decision"],
                    label=label,
                    reasons=[policy["reason"]],
                    triggered_pattern=pattern,
                )

    # Default: ALLOW
    return Classification(
        decision="ALLOW",
        label="general",
        reasons=["No policy triggers matched"],
        triggered_pattern=None,
    )


def get_policy_response(classification: Classification) -> str:
    """Return the canned response for a BLOCK or ESCALATE decision."""
    if classification.label in POLICIES:
        return POLICIES[classification.label]["response"]
    return "Request blocked by policy."


# -----------------------------
# 3) LLM Invocation (ALLOW only)
# -----------------------------

def call_openai_llm(prompt: str) -> str:
    """
    Minimal OpenAI Chat Completions API call.
    Uses official OpenAI Python SDK v1.x.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set; skipping LLM call.")

    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            "OpenAI SDK not installed. Install with: pip install openai"
        ) from e

    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for product managers working in regulated industries. "
                    "Provide clear, concise, factual information. Do not provide medical, legal, or financial advice."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )
    
    return response.choices[0].message.content


# -----------------------------
# 4) Orchestration + Audit
# -----------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(query: str, dry_run: bool = False) -> Dict:
    """
    Main orchestration:
    1. Classify the query
    2. Apply policy decision
    3. Optionally invoke LLM (if ALLOW and not dry_run)
    4. Return result with audit trail
    """
    t0 = time.time()
    classification = classify(query)

    audit = {
        "timestamp": now_iso(),
        "policy_version": classification.policy_version,
        "decision": classification.decision,
        "label": classification.label,
        "reasons": classification.reasons,
        "triggered_pattern": classification.triggered_pattern,
        "model_invoked": False,
        "dry_run": dry_run,
        "latency_ms": None,
    }

    if classification.decision == "BLOCK":
        response = get_policy_response(classification)

    elif classification.decision == "ESCALATE":
        response = get_policy_response(classification)

    else:  # ALLOW
        if dry_run:
            response = "[DRY RUN] Query would be allowed. LLM not invoked."
        else:
            try:
                response = call_openai_llm(query)
                audit["model_invoked"] = True
            except RuntimeError as e:
                response = f"[ALLOW] LLM call skipped: {e}"

    audit["latency_ms"] = int((time.time() - t0) * 1000)

    return {
        "query": query,
        "classification": {
            "decision": classification.decision,
            "label": classification.label,
            "reasons": classification.reasons,
            "triggered_pattern": classification.triggered_pattern,
        },
        "response": response,
        "audit": audit,
    }


# -----------------------------
# 5) CLI Entry Point
# -----------------------------

def print_usage():
    print("""
Pre-invocation Control Plane Demo

Usage:
  python control_plane.py "your query here"
  python control_plane.py --dry-run "your query here"

Examples:
  python control_plane.py "Summarize the NIST AI RMF for product managers"
  python control_plane.py "What medications interact with warfarin?"
  python control_plane.py "Should my patient stop taking their heart medication?"

Options:
  --dry-run    Show classification without invoking LLM (even if ALLOW)
  --help       Show this message
""")


def main():
    args = sys.argv[1:]
    
    if not args or "--help" in args:
        print_usage()
        sys.exit(0)

    dry_run = "--dry-run" in args
    if dry_run:
        args.remove("--dry-run")

    if not args:
        print("Error: No query provided.")
        print_usage()
        sys.exit(1)

    query = " ".join(args)
    result = run(query, dry_run=dry_run)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
