# Architecture Documentation

## Overview


                     START
                       |
                       v
                 TRIAGE AGENT
                       |
                       v
              KNOWLEDGE AGENT
                       |
                       v
              RESOLUTION AGENT
                       |
                       v
                REVIEW AGENT
                  /         \
            APPROVED       REJECTED
               |              |
               v              v
           RESPONSE       ESCALATION
                              |
                              v
                       HUMAN APPROVAL
                              |
                              v
                             END



## Frontend
`app.py` (Streamlit) is a thin presentation layer. It calls `run_ticket()` from `graph/workflow.py` and renders every field of the returned state. It contains no business logic itself.

## LangGraph
`graph/workflow.py` defines a `StateGraph(SupportState)` with 7 nodes and one conditional edge. The graph is compiled once at import time and reused across requests.

## State
`graph/state.py` defines `SupportState` as a `TypedDict` — the single shared object every node reads from and writes back to.

## Agents
Each agent lives in its own file under `agents/`, exposing one function `(state) -> dict`, matching what LangGraph expects from a node.

## LLM
`utils/llm.py` centralizes LLM client creation. Every agent imports `get_llm()` from here rather than instantiating its own client.

## RAG
`utils/retrieval.py` implements: `DirectoryLoader` reads `.md` files → `RecursiveCharacterTextSplitter` chunks them → `OpenAIEmbeddings` vectorizes → `FAISS` stores/searches. Only the top-k (k=3) chunks go to the LLM, never the whole knowledge base.

## Knowledge Base
Six Markdown files, each following: Problem, Common Symptoms, Possible Causes, Troubleshooting Steps, Resolution, Warnings, Escalation Conditions.

## Reviewer
`reviewer_agent.py` makes a second, independent LLM call whose only job is to critique the Resolution Agent's output against the same retrieved knowledge.

## Conditional Routing
`route_after_escalation_check()` is passed to `add_conditional_edges()`. LangGraph calls it after `escalation_check` runs and routes to `finalize_response` or `human_escalation`.

## Escalation
`escalation_agent.py` applies five independent rules in plain Python — not an LLM call — because escalation is a safety gate that must be consistent and explainable.

## Audit Logs
Every node appends a short human-readable string to `state["execution_log"]`, not raw LLM reasoning — just event names — rendered as the "Execution Trace" in the UI.
