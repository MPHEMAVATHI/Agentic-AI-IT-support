"""Command-line interface for the IT support workflow."""

import sys
from graph.workflow import run_ticket


def main():
    if len(sys.argv) > 1:
        ticket = " ".join(sys.argv[1:])
    else:
        ticket = input("Describe the IT issue: ").strip()

    result = run_ticket(ticket)

    print("\n=== TRIAGE ===")
    print("Category:", result.get("category"))
    print("Severity:", result.get("severity"))
    print("Intent:", result.get("intent"))
    print("Missing information:", result.get("missing_information"))
    print("Security related:", result.get("is_security_related"))

    print("\n=== KNOWLEDGE ===")
    print("Sources:", result.get("retrieved_documents"))

    print("\n=== RESOLUTION ===")
    print(result.get("proposed_resolution"))

    print("\n=== REVIEW ===")
    print("Status:", result.get("review_status"))
    print("Reason:", result.get("review_reason"))
    print("Confidence:", result.get("confidence"))

    print("\n=== ESCALATION ===")
    print("Requires human:", result.get("requires_human"))
    print("Reason:", result.get("escalation_reason"))

    print("\n=== FINAL RESPONSE ===")
    print(result.get("final_response"))

    print("\n=== EXECUTION TRACE ===")
    for item in result.get("execution_log", []):
        print("-", item)


if __name__ == "__main__":
    main()
