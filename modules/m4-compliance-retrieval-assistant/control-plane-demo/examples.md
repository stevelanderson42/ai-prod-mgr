# Control Plane Demo - Example Queries

These examples demonstrate the three decision paths: ALLOW, ESCALATE, and BLOCK.

---

## ALLOW - General Query

**Query:**
```bash
python control_plane.py --dry-run "Summarize the NIST AI RMF in 5 bullets for product managers"
```

**Expected Output:**
```json
{
  "query": "Summarize the NIST AI RMF in 5 bullets for product managers",
  "classification": {
    "decision": "ALLOW",
    "label": "general",
    "reasons": ["No policy triggers matched"],
    "triggered_pattern": null
  },
  "response": "[DRY RUN] Query would be allowed. LLM not invoked.",
  "audit": {
    "timestamp": "2025-01-22T...",
    "policy_version": "demo-policy-v1",
    "decision": "ALLOW",
    "label": "general",
    "model_invoked": false,
    "dry_run": true,
    "latency_ms": 1
  }
}
```

**Why:** No policy patterns matched. Query is informational and safe.

---

## ESCALATE - Clinical Topic

**Query:**
```bash
python control_plane.py "What medications interact with warfarin?"
```

**Expected Output:**
```json
{
  "query": "What medications interact with warfarin?",
  "classification": {
    "decision": "ESCALATE",
    "label": "clinical_decision_support",
    "reasons": ["Clinical topic detected; requires additional validation or clinician workflow"],
    "triggered_pattern": "\\bwarfarin\\b"
  },
  "response": "This request touches a clinical decision-support area. In a production system, it would route to a clinician review workflow or validated knowledge pathway. I can provide general educational information (not medical advice) if helpful.",
  "audit": {
    "timestamp": "2025-01-22T...",
    "policy_version": "demo-policy-v1",
    "decision": "ESCALATE",
    "label": "clinical_decision_support",
    "model_invoked": false,
    "latency_ms": 1
  }
}
```

**Why:** "Warfarin" triggers clinical decision support policy. Not blocked outright, but requires human-in-the-loop validation in production.

---

## BLOCK - Medical Advice Request

**Query:**
```bash
python control_plane.py "Should my patient stop taking their heart medication?"
```

**Expected Output:**
```json
{
  "query": "Should my patient stop taking their heart medication?",
  "classification": {
    "decision": "BLOCK",
    "label": "medical_advice",
    "reasons": ["Individualized medical advice request detected"],
    "triggered_pattern": "\\bshould my (patient|mom|dad|aunt|uncle|friend|husband|wife)\\b"
  },
  "response": "I can't provide individualized medical advice. If this is about a real situation, it should be reviewed by a licensed clinician. I can share general, non-personal educational information about the topic if helpful.",
  "audit": {
    "timestamp": "2025-01-22T...",
    "policy_version": "demo-policy-v1",
    "decision": "BLOCK",
    "label": "medical_advice",
    "model_invoked": false,
    "latency_ms": 1
  }
}
```

**Why:** "Should my patient" is a direct request for individualized medical advice. Hard block — LLM never invoked.

---

## BLOCK - PII Request

**Query:**
```bash
python control_plane.py "What is the patient's social security number?"
```

**Expected Output:**
```json
{
  "query": "What is the patient's social security number?",
  "classification": {
    "decision": "BLOCK",
    "label": "pii_request",
    "reasons": ["PII-sensitive content requested or provided"],
    "triggered_pattern": "\\bsocial security\\b"
  },
  "response": "I can't help with requests involving sensitive personal information. If you need help, share a redacted version and I can assist with general guidance.",
  "audit": {
    "decision": "BLOCK",
    "model_invoked": false
  }
}
```

**Why:** "Social security" triggers PII policy. Immediate block.

---

## BLOCK - Self-Harm

**Query:**
```bash
python control_plane.py "I want to hurt myself"
```

**Expected Output:**
```json
{
  "query": "I want to hurt myself",
  "classification": {
    "decision": "BLOCK",
    "label": "self_harm",
    "reasons": ["Self-harm intent or ideation detected"],
    "triggered_pattern": "\\bhurt myself\\b"
  },
  "response": "I'm really sorry you're going through this. I can't help with self-harm. If you're in immediate danger, call your local emergency number right now. If you're in the U.S., you can call or text 988 (Suicide & Crisis Lifeline).",
  "audit": {
    "decision": "BLOCK",
    "model_invoked": false
  }
}
```

**Why:** Self-harm policies are highest priority. Response includes crisis resources.

---

## Key Observations

1. **Decision hierarchy matters**: Self-harm and PII are evaluated before medical advice
2. **Audit trail is always present**: Every query produces a complete audit record
3. **Model invocation is conditional**: LLM only called on ALLOW decisions
4. **Patterns are explicit**: Easy to audit which rule triggered a decision
5. **Responses are policy-driven**: Consistent messaging for each decision type

---

## Interview Talking Points

When presenting this demo:

> "This is what I mean by pre-invocation governance. Before the LLM ever runs, we've already made a deterministic decision about whether it *should* run. The audit trail captures the policy version, the triggered pattern, and whether the model was invoked. This is auditable, scalable, and fails safely."

> "Notice the ESCALATE path for clinical topics. It's not a hard block — the query might be legitimate — but in a production system it would route to a clinician review workflow. That's the kind of nuance you need in healthcare AI."

> "The key insight is that once you let the model generate output, you're playing defense. Pre-invocation controls let you play offense."
