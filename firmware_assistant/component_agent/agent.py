from google.adk.agents import Agent

from ..prompts.component_prompt import COMPONENT_PROMPT

from ..database import (
    list_components,
    search_components,
    get_component_by_id,
    add_component,
    update_quantity,
    update_component_notes,
)

# ==========================================
# SPECIALIST AGENT 1: COMPONENTS
# ==========================================


component_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="component_agent",
    description=(
        "Manages and searches the firmware engineer's local "
        "hardware inventory, including component names, "
        "categories, quantities, manufacturers, models, "
        "interfaces, and recorded specifications."
    ),
    instruction=COMPONENT_PROMPT,
    tools=[
        list_components,
        search_components,
        get_component_by_id,
        add_component,
        update_quantity,
        update_component_notes,
    ],
)
