
from google.adk.agents import Agent

from .component_agent.agent import component_agent
from .rag_agent.agent import rag_agent
from .prompts.root_prompt import ROOT_PROMPT

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="firmware_assistant",
    description=(
        "A personal assistant for firmware and embedded "
        "systems engineers."
    ),
    instruction=ROOT_PROMPT,
    sub_agents=[
        component_agent,
        rag_agent,
    ],
)