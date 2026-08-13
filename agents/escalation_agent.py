"""
Agent 5 - Escalation / Human Approval Agent
-----------------------------------------------
Responsibility: make the FINAL, deterministic decision on whether a human
must review this ticket before the user sees any resolution.

IMPORTANT DESIGN DECISION: this agent does NOT call the LLM. It applies
plain Python if/else rules over fields already in the state.

Why deterministic rules instead of another LLM call here?
- Escalation is a SAFETY GATE. It must behave the same way every time given
  the same inputs (i.e. be deterministic and auditable) - an LLM call could
  in principle behave inconsistently across runs even with temperature=0.
- Rules are trivial to read, test, and explain in an interview: "high
  severity always escalates" is unambiguous, unlike "the LLM decided to
  escalate."
- It's cheaper and faster - no extra API call needed.

This is a common and important pattern in agentic systems: use the LLM for
understanding/generation (where flexibility helps), and use deterministic
code for safety-critical decisions (where consistency matters more).
"""

CONFIDENCE_THRESHOLD = 0.7


def run_escalation_agent(state):
    reasons = []

    if state.get("is_security_related"):
        reasons.append("Ticket is security/phishing related")

    if state.get("severity") == "High":
        reasons.append("Severity classified as High")

    if state.get("missing_information"):
        reasons.append(
            f"Missing information: {', '.join(state['missing_information'])}"
        )

    if state.get("review_status") != "APPROVED":
        reasons.append(
            f"Reviewer rejected the resolution: {state.get('review_reason', 'no reason given')}"
        )

    if state.get("confidence", 0) < CONFIDENCE_THRESHOLD:
        reasons.append(
            f"Confidence {state.get('confidence', 0):.2f} is below the "
            f"required threshold of {CONFIDENCE_THRESHOLD}"
        )

    requires_human = len(reasons) > 0
    escalation_reason = "; ".join(reasons)

    log = state.get("execution_log", [])
    if requires_human:
        log.append(f"Escalation check: HUMAN APPROVAL REQUIRED ({escalation_reason})")
    else:
        log.append("Escalation check: no escalation needed")

    return {
        "requires_human": requires_human,
        "escalation_reason": escalation_reason,
        "execution_log": log,
    }
