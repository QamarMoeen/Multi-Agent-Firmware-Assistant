
from google.adk.agents import Agent

from .component_agent.agent import component_agent
from .rag_agent.agent import rag_agent


root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="firmware_assistant",
    description=(
        "A personal assistant for firmware and embedded "
        "systems engineers."
    ),
    instruction="""
    You are a personal assistant for a firmware engineer.

    Route requests to the appropriate specialist:

    - Component Agent:
      Hardware inventory, component quantities, owned parts,
      inventory searches, adding components, and quantity changes.

    - RAG Agent:
      Completed projects, project descriptions, technical documents,
      microcontrollers used, project implementations, and questions
      requiring information from the project document collection.

    Do not invent inventory records or project history.
    For specialist requests, let the appropriate agent handle the task.
    """,
    sub_agents=[
        component_agent,
        rag_agent,
    ],
)