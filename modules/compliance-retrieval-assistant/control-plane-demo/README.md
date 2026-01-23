# Pre-invocation Control Plane Demo

A working demonstration of governance-by-design for AI systems in regulated environments.

## What This Demonstrates

This demo embodies a core thesis: **governance is most effective before an AI model executes, not after.**

The control plane:
1. **Classifies** incoming queries against deterministic policy rules
2. **Decides**: `ALLOW`, `ESCALATE`, or `BLOCK`
3. **Invokes** the LLM only when classification permits
4. **Emits** an audit trail for every decision

This is the architecture pattern I advocate for regulated AI workflows — pre-invocation controls that are deterministic, auditable, and enforceable.

## Why Pre-invocation Matters

Once an LLM generates output, governance becomes probabilistic and expensive:
- Output filtering is unreliable
- Post-hoc review doesn't scale
- Audit trails become reconstruction exercises

Pre-invocation controls:
- Are deterministic (rules, not probabilities)
- Are auditable (every decision is logged)
- Scale efficiently (most risk is filtered before expensive compute)
- Fail safely (blocked queries never reach the model)

## Usage

```bash
# Classification only (no API key needed)
python control_plane.py --dry-run "Your query here"

# With LLM invocation (requires OPENAI_API_KEY)
export OPENAI_API_KEY="your-key-here"
python control_plane.py "Summarize SR 11-7 model risk management"
```

## Example Outputs

See `examples.md` for sample queries demonstrating each decision type.

## Policy Configuration

Policies are defined as explicit dictionaries in the code, making them:
- Easy to audit ("here's the rule, here's the enforcement")
- Easy to extend (add new policies without changing logic)
- Easy to explain in interviews

Current policies cover:
- Self-harm detection → BLOCK
- PII requests → BLOCK  
- Medical advice requests → BLOCK
- Clinical decision support topics → ESCALATE
- General queries → ALLOW

## Architecture Alignment

This demo maps to the **Compliance Retrieval Assistant** module in my Regulated AI Workflow Toolkit:

| Component | Role |
|-----------|------|
| Policy Config | Defines what's allowed, blocked, escalated |
| Classification Engine | Deterministic rule evaluation |
| Decision Gate | ALLOW / ESCALATE / BLOCK |
| LLM Invocation | Only on ALLOW |
| Audit Trail | Every decision logged with timestamp, policy version, latency |

## Regulatory Context

This pattern supports compliance with:
- **NIST AI RMF**: Risk managed at design-time, not post-deployment
- **SR 11-7**: Model risk management through controlled execution paths
- **HIPAA/Clinical workflows**: Sensitive queries routed appropriately

## Limitations

This is a demonstration, not production code:
- Policies use simple regex patterns (production would use more sophisticated NLU)
- No persistence layer for audit logs
- No integration with actual clinical workflows
- Single-model invocation (production might use retrieval-augmented generation)

The point is to show the **pattern**, not to ship a product.
