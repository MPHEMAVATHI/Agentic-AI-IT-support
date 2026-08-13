"""Streamlit interface for the Agentic AI IT Support system."""

import streamlit as st
from graph.workflow import run_ticket

st.set_page_config(
    page_title="AI IT Support Resolution System",
    page_icon="🛠️",
    layout="wide",
)

st.title("AI IT Support Resolution System")
st.caption("Multi-stage IT Support powered by LangChain, LangGraph and local Ollama models")

ticket_text = st.text_area(
    "Describe your IT issue",
    value="My VPN stopped working after I changed my password.",
    height=150,
)

if st.button("Analyze Ticket", type="primary"):
    if not ticket_text.strip():
        st.warning("Please describe the IT issue first.")
    else:
        try:
            with st.spinner(
                "Running Triage → Knowledge Retrieval → Resolution → Review → Escalation..."
            ):
                result = run_ticket(ticket_text)

            st.success("Ticket analysis completed.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Category", result.get("category", "-"))
            col2.metric("Severity", result.get("severity", "-"))
            col3.metric(
                "Human escalation",
                "Yes" if result.get("requires_human") else "No",
            )

            st.subheader("Triage")
            st.write("**Intent:**", result.get("intent", "-"))
            st.write(
                "**Security related:**",
                "Yes" if result.get("is_security_related") else "No",
            )
            missing = result.get("missing_information", [])
            st.write("**Missing information:**", ", ".join(missing) if missing else "None")

            st.subheader("Knowledge Retrieval")
            docs = result.get("retrieved_documents", [])
            if docs:
                for doc in docs:
                    st.write(f"- {doc}")
            else:
                st.write("No documents retrieved.")

            st.subheader("Proposed Resolution")
            st.write(result.get("proposed_resolution", "No resolution generated."))

            st.subheader("Review")
            st.write("**Status:**", result.get("review_status", "-"))
            st.write("**Reason:**", result.get("review_reason", "-"))
            st.write("**Confidence:**", f"{result.get('confidence', 0.0):.2f}")

            st.subheader("Escalation")
            st.write("**Reason:**", result.get("escalation_reason", "-"))

            st.subheader("Final Response")
            st.info(result.get("final_response", "No final response."))

            with st.expander("Execution Trace"):
                for item in result.get("execution_log", []):
                    st.write(f"- {item}")

        except Exception as exc:
            message = str(exc)
            if "11434" in message or "Connection refused" in message or "Failed to establish" in message:
                st.error(
                    "Cannot connect to Ollama. Start it with `ollama serve`, then make sure "
                    "`llama3.2:3b` and `nomic-embed-text` are installed."
                )
            else:
                st.error(f"Something went wrong: {message}")
