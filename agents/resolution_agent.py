"""
Agent 3 - Resolution Agent
-----------------------------
Responsibility: generate a step-by-step troubleshooting resolution using
ONLY the ticket, triage info, and retrieved knowledge base content.

The prompt explicitly forbids inventing steps not supported by the
retrieved content - this is our main defense against hallucination at
generation time (the Reviewer Agent is our second defense, at check time).
"""

from utils.llm import get_llm

RESOLUTION_PROMPT = """You are the Resolution Agent in an internal IT support system.
Write a clear, numbered, step-by-step troubleshooting resolution for this ticket.

Ticket: "{ticket}"
Category: {category}
Severity: {severity}
User intent: {intent}

Knowledge base content (this is your ONLY source of truth for troubleshooting steps):
---
{knowledge}
---

Rules:
- Base your steps ONLY on the knowledge base content above. Do not invent steps that are not supported by it.
- If the knowledge base content does not fully cover the issue, say so explicitly instead of guessing.
- Keep it concise: numbered steps, plain language, no unnecessary jargon.
- Do not present any risky or security-sensitive action as safe to do without approval - reflect any warnings from the knowledge base.
"""


def run_resolution_agent(state):
    llm = get_llm()

    knowledge_text = "\n\n".join(state.get("retrieved_content", [])) or (
        "No relevant knowledge base content was found for this ticket."
    )

    prompt = RESOLUTION_PROMPT.format(
        ticket=state["ticket"],
        category=state["category"],
        severity=state["severity"],
        intent=state["intent"],
        knowledge=knowledge_text,
    )
    response = llm.invoke(prompt)

    log = state.get("execution_log", [])
    log.append("Resolution generated")

    return {
        "proposed_resolution": response.content,
        "execution_log": log,
    }
