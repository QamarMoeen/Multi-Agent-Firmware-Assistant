
from google.adk.agents import Agent

from .database import (
    list_components,
    search_components,
    get_component_by_id,
)

# Placeholder project records.
# Replace these descriptions with your actual projects.
PROJECTS = [
    {
        "name": "ESP32 Home Automation",
        "description": (
            "A home automation project using ESP32, "
            "DHT11, an IR receiver and Blynk."
        ),
        "microcontrollers": ["ESP32"],
    },
    {
        "name": "MIPS32 Processor",
        "description": (
            "A single-cycle MIPS32 processor implemented "
            "using VHDL on an FPGA."
        ),
        "microcontrollers": [],
    },
]


# ==========================================
# PROJECT SEARCH TOOL
# ==========================================

def search_projects(keyword: str) -> dict:
    """Search project names, descriptions, and microcontroller names."""

    keyword = keyword.strip().lower()

    matches = [
        project
        for project in PROJECTS
        if keyword in project["name"].lower()
        or keyword in project["description"].lower()
        or any(
            keyword in controller.lower()
            for controller in project["microcontrollers"]
        )
    ]

    return {
        "search_term": keyword,
        "matches": matches,
        "count": len(matches),
    }


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
    instruction="""
    You are a hardware inventory specialist for a firmware engineer.

    Available tools:
    - list_components: retrieve all components in the inventory.
    - search_components: search by component name, category,
      manufacturer, model, interface, or notes.
    - get_component_by_id: retrieve a specific inventory record.

    Select the tool appropriate for the user's request.
    Base inventory answers on returned database records.
    Never invent components, quantities, or specifications.
    If a field is missing, say that it has not been recorded.
    If no component matches, explain that it was not found.
    Do not claim that two components are electrically compatible
    unless the required specifications have been verified.
    """,
    tools=[
        list_components,
        search_components,
        get_component_by_id,
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


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
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


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