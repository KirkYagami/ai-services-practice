"""Workflow nodes: each reads the state, calls one agent, and returns updates."""

from langchain_core.messages import AIMessage

from agents import edit_blog_content, make_publish_decision, write_blog_draft
from state import ContentState


def write_draft(state: ContentState) -> dict:
    """Ask the writer agent for a first draft of the topic."""
    draft = write_blog_draft(state["topic"])
    return {
        "draft": draft,
        "messages": [AIMessage(content="Writer: Initial draft created")],
        "status": "editing",
    }


def edit_content(state: ContentState) -> dict:
    """Ask the editor agent to improve the draft."""
    edited_version = edit_blog_content(state["draft"])
    return {
        "edited_version": edited_version,
        "messages": [AIMessage(content="Editor: Content refined for clarity and quality")],
        "status": "reviewing",
    }


def publish_decision(state: ContentState) -> dict:
    """Ask the publisher agent whether to publish the edited post."""
    decision, reasoning = make_publish_decision(state["edited_version"])
    return {
        "status": decision,
        "messages": [AIMessage(content=f"Publisher: {reasoning}")],
    }
