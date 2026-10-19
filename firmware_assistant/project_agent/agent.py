from google.adk.agents import Agent

from ..project_rag import search_projects
from ..prompts.project_prompt import PROJECT_PROMPT

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
    instruction=PROJECT_PROMPT,
    tools=[search_projects],
)