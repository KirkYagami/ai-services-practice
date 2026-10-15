"""Build the three-step LangGraph workflow: write -> edit -> publish."""

from langgraph.graph import END, START, StateGraph

from nodes import edit_content, publish_decision, write_draft
from state import ContentState


def build_workflow():
    """Return the compiled workflow, ready to invoke with an initial state."""
    workflow = StateGraph(ContentState)
    workflow.add_node("write", write_draft)
    workflow.add_node("edit", edit_content)
    workflow.add_node("publish", publish_decision)

    workflow.add_edge(START, "write")
    workflow.add_edge("write", "edit")
    workflow.add_edge("edit", "publish")
    workflow.add_edge("publish", END)
    return workflow.compile()
