from google.adk.agents import Agent

from ..project_rag import search_projects

# ==========================================
# SPECIALIST AGENT 2: PROJECTS
# ==========================================

project_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="project_agent",
    description=(
        "Answers questions about completed firmware, "
        "embedded systems, and digital design projects."
    ),
    instruction="""
    You are a project portfolio assistant.

    Use search_projects to find relevant projects.

    Answer questions about which projects were completed,
    which microcontrollers were used, and what each project did.

    Base answers on the returned project records.
    Do not invent project details.

    If no matching project is found, say so.
    This is basic keyword search, not semantic RAG.
    """,
    tools=[search_projects],
)