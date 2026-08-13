"""
Tests for the full LangGraph workflow.

These are integration tests - they make real LLM calls, so they require
a valid OPENAI_API_KEY in your .env file, and they cost a small amount
of API credit to run. They are skipped automatically if no key is set,
so the test suite doesn't crash in an environment without credentials.

Run with:
    pytest tests/test_workflow.py -v
"""

import os
import pytest
from dotenv import load_dotenv

load_dotenv()

from graph.workflow import run_ticket

requires_api_key = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set - skipping live LLM tests",
)


@requires_api_key
def test_normal_vpn_scenario():
    """A clear, well-formed VPN ticket should be triaged correctly,
    retrieve the VPN knowledge doc, and NOT require human escalation
    (unless the reviewer finds an issue)."""
    result = run_ticket("My VPN stopped working after I changed my password.")

    assert result["category"] == "VPN"
    assert "vpn_troubleshooting.md" in result["retrieved_documents"]
    assert result["proposed_resolution"] != ""
    assert result["review_status"] in ("APPROVED", "REJECTED")
    if result["review_status"] == "APPROVED" and not result["missing_information"]:
        assert result["requires_human"] is False


@requires_api_key
def test_ambiguous_laptop_scenario():
    """A vague ticket should trigger missing_information detection and
    should NOT be confidently auto-resolved without flags."""
    result = run_ticket("My laptop isn't working properly.")

    assert result["category"] in ("Laptop Performance", "Other")
    assert len(result["missing_information"]) > 0 or result["requires_human"] is True


@requires_api_key
def test_phishing_security_scenario():
    """A phishing/credential-exposure ticket must ALWAYS be escalated to
    a human, regardless of how the reviewer scores the resolution."""
    result = run_ticket(
        "I received an email asking me to reset my Microsoft password. "
        "I clicked the link and entered my password."
    )

    assert result["is_security_related"] is True
    assert result["severity"] == "High"
    assert result["requires_human"] is True
    assert "HUMAN APPROVAL REQUIRED" in result["final_response"]


def test_state_shape_after_run_without_api_key():
    """A lightweight structural test that doesn't require an API key:
    confirms run_ticket raises a clear error (not a silent failure) when
    no key is configured. Only meaningful when no key is set."""
    if os.getenv("OPENAI_API_KEY"):
        pytest.skip("API key is set - this test only applies when it's missing")

    with pytest.raises(ValueError):
        run_ticket("My VPN stopped working after I changed my password.")
