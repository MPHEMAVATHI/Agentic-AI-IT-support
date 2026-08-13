"""
Streamlit UI for the Agentic AI IT Support Resolution System.

This file only handles PRESENTATION. All the actual multi-agent logic
lives in graph/workflow.py and the agents/ folder - this keeps concerns
cleanly separated.
"""

import streamlit as st
from graph.workflow import run_ticket

st.set_page_config(page_title="AI IT Support Resolution System", page_icon="🛠️", layout="wide")

st.title("AI IT Support Resolution System")
st.caption("Multi-Agent IT Support powered by LangChain and LangGraph")

ticket_text = st.text_area(
    "Describe your IT issue",
    placeholder="My VPN stopped working after I changed my password.",
    height=120,
)

run_clicked = st.button("Analyze Ticket", type="primary")

if run_clicked:
    if not ticket_text.strip():
        st.warning("Please enter a ticket description first.")
    else:
        with st.spinner("Running Triage → Knowledge Retrieval → Resolution → Review..."):
            try:
                result = run_ticket(ticket_text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        # ---------- Ticket Analysis ----------
        st.subheader("Ticket Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", result["category"])
        col2.metric("Severity", result["severity"])
        col3.metric("Security Related", "Yes" if result["is_security_related"] else "No")

        st.write(f"**Intent:** {result['intent']}")
        if result["missing_information"]:
            st.write(f"**Missing Information:** {', '.join(result['missing_information'])}")
        else:
            st.write("**Missing Information:** None")

        # ---------- Knowledge Retrieved ----------
        st.subheader("Knowledge Retrieved")
        if result["retrieved_documents"]:
            st.write("**Source documents:** " + ", ".join(result["retrieved_documents"]))
            with st.expander("View retrieved knowledge base content"):
                for i, chunk in enumerate(result["retrieved_content"], start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.text(chunk)
        else:
            st.warning("No relevant knowledge base documents were found.")

        # ---------- Proposed Resolution ----------
        st.subheader("Proposed Resolution")
        st.markdown(result["proposed_resolution"])

        # ---------- Reviewer Result ----------
        st.subheader("Reviewer Result")
        rcol1, rcol2 = st.columns(2)
        with rcol1:
            if result["review_status"] == "APPROVED":
                st.success(f"Status: {result['review_status']}")
            else:
                st.error(f"Status: {result['review_status']}")
        with rcol2:
            st.metric("Confidence", f"{result['confidence']:.2f}")
        st.write(f"**Reason:** {result['review_reason']}")

        # ---------- Escalation Status ----------
        st.subheader("Escalation Status")
        if result["requires_human"]:
            st.error("HUMAN APPROVAL REQUIRED")
            st.write(f"**Reason:** {result['escalation_reason']}")
        else:
            st.success("No escalation needed - safe to return automatically.")

        # ---------- Final Response ----------
        st.subheader("Final Response")
        if result["requires_human"]:
            st.warning(result["final_response"])
        else:
            st.info(result["final_response"])

        # ---------- Execution Trace ----------
        st.subheader("Execution Trace")
        trace_str = "\n↓\n".join(result["execution_log"])
        st.code(trace_str, language=None)
