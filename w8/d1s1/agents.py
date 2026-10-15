"""Gemini agents that write, edit, and review a blog post."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(Path(__file__).resolve().parent / ".env")


def ask_gemini(prompt: str) -> str:
    """Send one prompt to the Gemini model and return its text reply."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.environ["GEMINI_MODEL"], contents=prompt
    )
    return response.text or ""


def write_blog_draft(topic: str) -> str:
    """Write a 150-200 word blog draft about the topic."""
    prompt = (
        "You are a professional blog writer. Write a blog post of 150-200 words "
        "with a title, a short introduction, 3 key points, and a conclusion.\n\n"
        f"Topic: {topic}"
    )
    return ask_gemini(prompt)


def edit_blog_content(draft: str) -> str:
    """Improve the draft's grammar, clarity, flow, word choices, and tone."""
    prompt = (
        "You are a professional editor. Improve this blog post's grammar, clarity, "
        "flow, word choices, and tone. Keep the same structure. "
        "Return only the improved blog post without explanations.\n\n"
        f"Blog post:\n{draft}"
    )
    return ask_gemini(prompt)


def make_publish_decision(edited_content: str) -> tuple[str, str]:
    """Decide whether to publish the post and return (decision, reasoning)."""
    prompt = (
        "You are a publisher. Review this blog post for quality, clarity, "
        "structure, engagement, and completeness.\n"
        "Reply in exactly this format:\n"
        "DECISION: [PUBLISH or REJECT]\n"
        "REASONING: [One sentence explanation]\n\n"
        f"Blog post:\n{edited_content}"
    )
    response = ask_gemini(prompt).strip()

    decision = "published" if "DECISION: PUBLISH" in response else "rejected"

    reasoning = "Content review complete"
    for line in response.splitlines():
        if "REASONING:" in line:
            reasoning = line.split("REASONING:", 1)[1].strip()
            break

    return decision, reasoning
