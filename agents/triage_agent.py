"""
Agent 1 - Triage Agent
------------------------
Responsibility: read the raw ticket and produce a structured understanding
of it - category, severity, intent, missing info, and whether it's security
related.

We use LangChain's `with_structured_output()` with a Pydantic model instead
of asking the LLM to "please reply in this format" and parsing raw text.
This guarantees the output always matches our schema (correct types, no
missing fields), which is far more reliable than manual string parsing.
"""

from typing import List
from pydantic import BaseModel, Field

from utils.llm import get_llm


class TriageResult(BaseModel):
    category: str = Field(
        description=(
            "One of: VPN, Password, Teams, Laptop Performance, "
            "Access Management, Phishing/Security, Other"
        )
    )
    severity: str = Field(description="One of: Low, Medium, High")
    intent: str = Field(
        description="A short sentence describing what the user wants resolved"
    )
    missing_information: List[str] = Field(
        default_factory=list,
        description="Important missing details needed to resolve this ticket safely. Empty list if the ticket is clear enough.",
    )
    is_security_related: bool = Field(
        description=(
            "True if this ticket involves phishing, a suspicious link, "
            "credentials entered on an unknown page, or suspected "
            "unauthorized account access."
        )
    )


TRIAGE_PROMPT = """You are the Triage Agent in an internal IT support system.
Read the ticket below and classify it carefully.

Ticket: "{ticket}"

Guidance:
- category must be exactly one of: VPN, Password, Teams, Laptop Performance, Access Management, Phishing/Security, Other
- severity: "High" for security incidents or a total inability to work, "Medium" for partial disruption, "Low" for minor inconvenience
- is_security_related must be True for ANY mention of a suspicious email, a clicked link, credentials entered on an unfamiliar page, or suspected account compromise - even if the user does not sound alarmed
- missing_information should list only genuinely important missing details (e.g. operating system, error message, when it started). Leave it as an empty list if the ticket is already clear enough to act on.
"""


def run_triage_agent(state):
    """
    LangGraph node function. Receives the current state, returns a dict
    of the fields it wants to update. LangGraph merges this dict back
    into the shared state automatically.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(TriageResult)

    prompt = TRIAGE_PROMPT.format(ticket=state["ticket"])
    result: TriageResult = structured_llm.invoke(prompt)

    log = state.get("execution_log", [])
    log.append(f"Triage: {result.category} / {result.severity}")

    return {
        "category": result.category,
        "severity": result.severity,
        "intent": result.intent,
        "missing_information": result.missing_information,
        "is_security_related": result.is_security_related,
        "execution_log": log,
    }
