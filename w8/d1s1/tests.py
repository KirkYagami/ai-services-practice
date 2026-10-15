import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def content_result():
    """
    Fixture: Run content review workflow with a test blog topic
    Uses student's graph, state, nodes, and agents
    """
    from graph import build_workflow
    from langchain_core.messages import HumanMessage

    test_topic = "Artificial Intelligence in Healthcare"

    graph = build_workflow()

    initial_state = {
        "messages": [HumanMessage(content=f"Write about: {test_topic}")],
        "topic": test_topic,
        "draft": "",
        "edited_version": "",
        "status": "drafting",
    }

    return graph.invoke(initial_state)


def test_output_is_dict(content_result):
    """Test: Workflow returns a dictionary"""
    assert isinstance(content_result, dict)


def test_has_all_required_fields(content_result):
    """Test: Output has all required state fields"""
    required_fields = ["messages", "topic", "draft", "edited_version", "status"]
    for field in required_fields:
        assert field in content_result, f"Missing field: {field}"


def test_topic_preserved(content_result):
    """Test: Topic is preserved through workflow"""
    assert content_result["topic"] == "Artificial Intelligence in Healthcare"


def test_draft_not_empty(content_result):
    """Test: Draft is created by writer"""
    assert isinstance(content_result["draft"], str)
    assert len(content_result["draft"]) > 0


def test_edited_version_not_empty(content_result):
    """Test: Edited version is created by editor"""
    assert isinstance(content_result["edited_version"], str)
    assert len(content_result["edited_version"]) > 0


def test_status_is_final(content_result):
    """Test: Final status is published or rejected"""
    assert content_result["status"] in ["published", "rejected"]


def test_messages_accumulated(content_result):
    """Test: Messages list grows with workflow execution"""
    messages = content_result["messages"]
    assert isinstance(messages, list)
    assert len(messages) > 1


def test_draft_before_edited(content_result):
    """Test: Draft content exists before editing"""
    assert len(content_result["draft"]) > 0


def test_workflow_completes_all_stages(content_result):
    """Test: Workflow executes all three stages"""
    assert content_result["draft"]  # Writer executed
    assert content_result["edited_version"]  # Editor executed
    assert content_result["status"] in ["published", "rejected"]  # Publisher executed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
