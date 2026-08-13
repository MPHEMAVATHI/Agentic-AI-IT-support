"""
Simple CLI runner - lets you test the full LangGraph workflow from the
terminal before touching the Streamlit UI. Much faster for debugging.

Usage:
    python cli.py "My VPN stopped working after I changed my password."
"""

import sys
from graph.workflow import run_ticket


def main():
    if len(sys.argv) > 1:
        ticket = " ".join(sys.argv[1:])
    else:
        ticket = input("Enter an IT support ticket: ")

    result = run_ticket(ticket)

    print("\n--- Ticket ---")
    print(result["ticket"])

    print("\n--- Triage ---")
    print(f"Category: {result['category']}")
    print(f"Severity: {result['severity']}")
    print(f"Intent: {result['intent']}")
    print(f"Missing Information: {result['missing_information']}")
    print(f"Security Related: {result['is_security_related']}")

    print("\n--- Knowledge Retrieved ---")
    print(f"Sources: {result['retrieved_documents']}")

    print("\n--- Proposed Resolution ---")
    print(result["proposed_resolution"])

    print("\n--- Review ---")
    print(f"Status: {result['review_status']}")
    print(f"Reason: {result['review_reason']}")
    print(f"Confidence: {result['confidence']}")

    print("\n--- Escalation ---")
    print(f"Human Required: {result['requires_human']}")
    print(f"Escalation Reason: {result['escalation_reason']}")

    print("\n--- Final Response ---")
    print(result["final_response"])

    print("\n--- Execution Trace ---")
    for step in result["execution_log"]:
        print(f"  -> {step}")


if __name__ == "__main__":
    main()
