"""
Agent 4 - Review / Validation Agent
--------------------------------------
Responsibility: independently check the proposed resolution before it is
ever shown to the user.

Why a SECOND LLM call instead of trusting the Resolution Agent's own output?
- A model reviewing its own answer in the same "train of thought" tends to
  agree with itself. A fresh call, focused only on critique (not on
  generating), is more likely to catch missing grounding, invented steps,
  or risk - similar to why human writers use a separate editor/reviewer.
- It also gives us a natural place to compute a confidence score used by
  the Escalation Agent's rules.
"""

from pydantic import BaseModel, Field
from utils.llm import get_llm


class ReviewResult(BaseModel):
    status: str = Field(description="Either APPROVED or REJECTED")
    reason: str = Field(description="Short, specific explanation for the decision")
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0 that this resolution is safe, relevant, and grounded"
    )


REVIEW_PROMPT = """You are the Review / Validation Agent in an internal IT support system.
Critically check the proposed resolution against the knowledge base content it was supposed to be grounded in.

Ticket: "{ticket}"

Knowledge base content that was provided to the Resolution Agent:
---
{knowledge}
---

Proposed resolution:
---
{resolution}
---

Check all of the following:
1. Relevance - does the resolution actually address the ticket?
2. Grounding - is every step supported by the knowledge base content above (no invented/hallucinated steps)?
3. Completeness - are any important troubleshooting steps missing?
4. Risk - could any step be unsafe to perform without human review (e.g. deleting data, bypassing security controls, granting access)?

Return status "APPROVED" only if the resolution is relevant, grounded, reasonably complete, and safe.
Otherwise return "REJECTED" with a clear, specific reason.
Always include a confidence score between 0.0 and 1.0.
"""


def run_reviewer_agent(state):
    llm = get_llm()
    structured_llm = llm.with_structured_output(ReviewResult)

    knowledge_text = "\n\n".join(state.get("retrieved_content", [])) or (
        "No knowledge base content was retrieved."
    )

    prompt = REVIEW_PROMPT.format(
        ticket=state["ticket"],
        knowledge=knowledge_text,
        resolution=state.get("proposed_resolution", ""),
    )
    result: ReviewResult = structured_llm.invoke(prompt)

    log = state.get("execution_log", [])
    log.append(f"Reviewer: {result.status} (confidence {result.confidence:.2f})")

    return {
        "review_status": result.status,
        "review_reason": result.reason,
        "confidence": result.confidence,
        "execution_log": log,
    }
