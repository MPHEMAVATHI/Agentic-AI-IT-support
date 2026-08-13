"""
LangGraph Workflow
---------------------
This file wires the five agents together into an executable graph.

ASCII diagram of the graph:

    START
      |
      v
   [triage]              Agent 1: understand + classify the ticket
      |
      v
  [knowledge]             Agent 2: RAG search over knowledge_base/
      |
      v
  [resolution]            Agent 3: generate grounded troubleshooting steps
      |
      v
    [review]              Agent 4: APPROVE or REJECT the resolution
      |
      v
[escalation_check]        Agent 5: deterministic rules -> requires_human?
      |
      +---- False ----> [finalize_response] ----> END
      |
      +---- True  ----> [human_escalation]  ----> END
"""

from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from agents.triage_agent import run_triage_agent
from agents.knowledge_agent import run_knowledge_agent
from agents.resolution_agent import run_resolution_agent
from agents.reviewer_agent import run_reviewer_agent
from agents.escalation_agent import run_escalation_agent


def finalize_response(state):
    """Terminal node used when no escalation is required."""
    log = state.get("execution_log", [])
    log.append("Final response ready")
    return {
        "final_response": state["proposed_resolution"],
        "execution_log": log,
    }


def human_escalation_response(state):
    """Terminal node used when human approval is required."""
    log = state.get("execution_log", [])
    log.append("Routed to human escalation")
    message = (
        "HUMAN APPROVAL REQUIRED\n\n"
        f"Reason: {state.get('escalation_reason', 'Unspecified')}\n\n"
        "A support engineer will review this ticket before any action is taken."
    )
    return {
        "final_response": message,
        "execution_log": log,
    }


def route_after_escalation_check(state):
    """
    Conditional edge function. LangGraph calls this with the current
    state and expects back the NAME of the next node to go to.
    """
    return "human_escalation" if state.get("requires_human") else "finalize_response"


def build_workflow():
    graph = StateGraph(SupportState)

    graph.add_node("triage", run_triage_agent)
    graph.add_node("knowledge", run_knowledge_agent)
    graph.add_node("resolution", run_resolution_agent)
    graph.add_node("review", run_reviewer_agent)
    graph.add_node("escalation_check", run_escalation_agent)
    graph.add_node("finalize_response", finalize_response)
    graph.add_node("human_escalation", human_escalation_response)

    graph.add_edge(START, "triage")
    graph.add_edge("triage", "knowledge")
    graph.add_edge("knowledge", "resolution")
    graph.add_edge("resolution", "review")
    graph.add_edge("review", "escalation_check")

    graph.add_conditional_edges(
        "escalation_check",
        route_after_escalation_check,
        {
            "finalize_response": "finalize_response",
            "human_escalation": "human_escalation",
        },
    )

    graph.add_edge("finalize_response", END)
    graph.add_edge("human_escalation", END)

    return graph.compile()


workflow = build_workflow()


def run_ticket(ticket_text: str) -> dict:
    """
    Convenience function: builds a fresh initial state for a new ticket
    and runs it through the whole compiled graph, returning the final state.
    """
    initial_state: SupportState = {
        "ticket": ticket_text,
        "category": "",
        "severity": "",
        "intent": "",
        "missing_information": [],
        "is_security_related": False,
        "retrieved_documents": [],
        "retrieved_content": [],
        "proposed_resolution": "",
        "review_status": "",
        "review_reason": "",
        "confidence": 0.0,
        "requires_human": False,
        "escalation_reason": "",
        "final_response": "",
        "execution_log": ["Ticket received"],
    }
    return workflow.invoke(initial_state)
