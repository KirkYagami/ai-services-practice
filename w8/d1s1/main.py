"""Run the content review pipeline from the terminal."""

from langchain_core.messages import HumanMessage

from graph import build_workflow


def run_content_review_pipeline() -> None:
    """Ask for a topic, run the workflow, and print each stage's result."""
    topic = input("Enter blog topic: ").strip()

    workflow = build_workflow()
    initial_state = {
        "messages": [HumanMessage(content=f"Write about: {topic}")],
        "topic": topic,
        "draft": "",
        "edited_version": "",
        "status": "drafting",
    }
    final_state = workflow.invoke(initial_state)

    print("=" * 70)
    print("CONTENT REVIEW PIPELINE COMPLETE")
    print("=" * 70)
    print(f"Topic: {final_state['topic']}")

    print("\nWRITER'S DRAFT:")
    print("-" * 70)
    print(final_state["draft"])

    print("\nEDITOR'S IMPROVEMENTS:")
    print("-" * 70)
    print(final_state["edited_version"])

    print("\nPUBLISHER'S DECISION:")
    print("-" * 70)
    print(f"Status: {final_state['status'].upper()}")

    print("\nMessage Trail:")
    for message in final_state["messages"]:
        print(f"  • {message.content}")


if __name__ == "__main__":
    run_content_review_pipeline()
