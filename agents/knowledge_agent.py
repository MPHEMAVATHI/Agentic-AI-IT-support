"""
Agent 2 - Knowledge Retrieval Agent
--------------------------------------
Responsibility: search the local Markdown knowledge base and return ONLY
the most relevant chunks (not the whole knowledge base) plus their source
filenames, so downstream agents can generate a grounded answer.

This agent does not call the LLM at all - it purely does a vector
similarity search (see utils/retrieval.py for the RAG pipeline details).
"""

from utils.retrieval import retrieve_relevant_knowledge


def run_knowledge_agent(state):
    # Combine category + intent + raw ticket into one retrieval query.
    # Category and intent (from Triage) sharpen the query beyond the
    # user's raw wording, improving retrieval accuracy.
    query = f"{state['category']} {state['intent']} {state['ticket']}"

    sources, contents = retrieve_relevant_knowledge(query, k=3)

    log = state.get("execution_log", [])
    if sources:
        log.append(f"Knowledge: {', '.join(sources)}")
    else:
        log.append("Knowledge: no relevant documents found")

    return {
        "retrieved_documents": sources,
        "retrieved_content": contents,
        "execution_log": log,
    }
