"""
Simple event logger.

We deliberately log WORKFLOW EVENTS (e.g. "Triage: VPN / Medium") rather
than the LLM's internal reasoning. This keeps the audit trail useful and
readable without exposing raw chain-of-thought.
"""


def log_event(message: str):
    print(f"[WORKFLOW] {message}")
