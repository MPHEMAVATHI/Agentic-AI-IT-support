"""
LangGraph State
----------------
Think of the State as a SHARED NOTEBOOK that gets passed from agent to
agent. Each agent reads what it needs from the notebook and writes its
own findings back into it, so the next agent can use that information.

We use TypedDict (not a plain dict) because it gives us:
  - A clear, single source of truth for what fields exist in the state
  - Editor autocomplete and type checking
  - Self-documentation: anyone reading this file understands the whole
    workflow's data shape at a glance
"""

from typing import TypedDict, List


class SupportState(TypedDict):
    ticket: str
    category: str
    severity: str
    intent: str
    missing_information: List[str]
    is_security_related: bool
    retrieved_documents: List[str]
    retrieved_content: List[str]
    proposed_resolution: str
    review_status: str
    review_reason: str
    confidence: float
    requires_human: bool
    escalation_reason: str
    final_response: str
    execution_log: List[str]
