
from google.adk.agents import Agent
from .project_agent.agent import project_agent
from .component_agent.agent import component_agent

# ==========================================
# ROOT AGENT
# ==========================================

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="firmware_assistant",
    description=(
        "A personal assistant for firmware and embedded "
        "systems engineers."
    ),
    instruction="""
    You are a personal assistant for a firmware engineer.

    Route every new request to the appropriate specialist.

    - Questions about owned hardware, component quantities,
      or inventory searches go to component_agent.
    - Questions about completed projects, project descriptions,
      or which microcontrollers were used go to project_agent.

    If a question is unrelated to the inventory or projects,
    provide a brief general answer when appropriate.

    Do not invent inventory records or project history.
    """,
    sub_agents=[component_agent, project_agent],
)