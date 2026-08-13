# Agentic-AI-IT-support
Multi-agent IT support system using LangChain + LangGraph


# Agentic AI IT Support Resolution System

A multi-agent AI system that reads an internal IT support ticket, triages it, retrieves grounded knowledge from a local Markdown knowledge base, generates a troubleshooting resolution, reviews it for safety/accuracy, and decides whether it can be returned automatically or must be escalated to a human.

## Problem

Support engineers manually read tickets, search internal docs, propose fixes, and decide on escalation. This is slow and inconsistent at scale. This project automates the first pass of that workflow while keeping a human in the loop for anything risky, security-related, or uncertain.

## Solution

Five LangGraph agents run in a fixed pipeline, with a rules-based safety gate deciding whether a human must review the result before the user sees it.

## Architecture

\```
                        START
                          |
                          v
                     [ TRIAGE ]            understand, classify, detect gaps
                          |
                          v
                    [ KNOWLEDGE ]          RAG search over knowledge_base/*.md
                          |
                          v
                    [ RESOLUTION ]        grounded step-by-step answer
                          |
                          v
                     [ REVIEW ]           APPROVED / REJECTED + confidence
                          |
                          v
                [ ESCALATION CHECK ]      deterministic rules (always runs)
                     /            \
              not required      required
                   |                |
                   v                v
          [FINALIZE RESPONSE]  [HUMAN ESCALATION]
                   |                |
                   v                v
                  END              END
\```

**Why escalation_check runs after every review, not just on REJECTED:**
A resolution can be perfectly APPROVED by the reviewer and still need a human — e.g. it's security-related, or severity is High, or the ticket was missing key details. Escalation is an independent safety layer, not just "did the reviewer like it."

## Agent Roles

| Agent | Calls LLM? | Responsibility |
|---|---|---|
| Triage Agent | Yes (structured output) | Category, severity, intent, missing info, security flag |
| Knowledge Retrieval Agent | No (vector search only) | Top-k relevant chunks from local Markdown KB |
| Resolution Agent | Yes | Grounded, numbered troubleshooting steps |
| Reviewer Agent | Yes (structured output) | APPROVED/REJECTED, reason, confidence score |
| Escalation Agent | No (deterministic rules) | Final human-approval-required decision |

**Why deterministic rules for escalation instead of another LLM call?** Escalation is a safety gate — it needs to be consistent and explainable every single time.

## LangGraph Workflow

Implemented in `graph/workflow.py` using `StateGraph`:
- **Nodes:** `triage`, `knowledge`, `resolution`, `review`, `escalation_check`, `finalize_response`, `human_escalation`
- **Edges:** straight-line edges connect triage → knowledge → resolution → review → escalation_check
- **Conditional edge:** `escalation_check` branches to either `finalize_response` or `human_escalation` based on the `requires_human` flag
- **Termination:** both branches lead to `END`

## RAG / Knowledge Base

- **Loader:** `DirectoryLoader` + `TextLoader` reads all `.md` files in `knowledge_base/`
- **Splitter:** `RecursiveCharacterTextSplitter` (chunk_size=800, overlap=100)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Vector store:** FAISS (local, in-memory, zero external dependencies)
- **Retriever:** `similarity_search(query, k=3)` — only top 3 chunks sent to the LLM

Six knowledge documents: `vpn_troubleshooting.md`, `password_reset.md`, `microsoft_teams.md`, `laptop_performance.md`, `access_management.md`, `phishing_security.md`.

## Project Structure

\```
agentic-ai-it-support/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── app.py
├── cli.py
├── agents/
├── graph/
├── knowledge_base/
├── utils/
├── tests/
└── docs/
\```

## Installation

\```bash
git clone <your-repo-url>
cd agentic-ai-it-support
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\```

## Environment Variables

Copy `.env.example` to `.env` and add your key:

\```
OPENAI_API_KEY=your_actual_key_here
\```

## How to Run

CLI:
\```bash
python cli.py "My VPN stopped working after I changed my password."
\```

Streamlit UI:
\```bash
streamlit run app.py
\```

## How to Test

\```bash
pytest tests/test_workflow.py -v
\```

## Test Scenarios

1. Normal: "My VPN stopped working after I changed my password." → APPROVED, no escalation.
2. Ambiguous: "My laptop isn't working properly." → missing information detected.
3. Security: "I received an email asking me to reset my Microsoft password. I clicked the link and entered my password." → always escalated.

## Design Decisions

- Structured output (Pydantic) for Triage and Reviewer guarantees valid, typed fields.
- FAISS over a hosted vector DB — small local knowledge base, no operational overhead needed.
- Escalation as deterministic rules, not an LLM call — safety-critical decisions need consistency.
- escalation_check always runs, not only on REJECTED.
- Low temperature (0.2) for all LLM calls.

## Limitations

- No conversational follow-up loop to collect missing information.
- No persistent storage of tickets/audit logs beyond the current session.
- No authentication/authorization on escalation approval.

## Production Improvements

- Human-in-the-loop UI for approving escalated tickets.
- Persist tickets and logs to a database.
- Follow-up question loop for missing information.
- Category-specific confidence thresholds.
- Observability/tracing (e.g. LangSmith).

## Technologies Used

Python, LangChain, LangGraph, OpenAI (gpt-4o-mini + text-embedding-3-small), FAISS, Streamlit, python-dotenv, Pydantic, pytest.
