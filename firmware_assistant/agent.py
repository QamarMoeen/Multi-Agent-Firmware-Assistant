
from google.adk.agents import Agent


# ==========================================
# SAMPLE DATA
# ==========================================

# Temporary inventory data.
# Later, we will store this in SQLite.
COMPONENTS = [
    {
        "name": "ESP32 DevKit",
        "category": "microcontroller",
        "quantity": 2,
        "notes": "Development board"
    },
    {
        "name": "DHT11",
        "category": "sensor",
        "quantity": 1,
        "notes": "Temperature and humidity sensor"
    },
    {
        "name": "IR Receiver",
        "category": "sensor",
        "quantity": 2,
        "notes": "Infrared receiver module"
    },
    {
        "name": "16x2 LCD",
        "category": "display",
        "quantity": 1,
        "notes": "Character display"
    },
]


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
# COMPONENT TOOLS
# ==========================================

def list_components() -> dict:
    """List all components in the hardware inventory."""

    return {
        "components": COMPONENTS,
        "total_component_types": len(COMPONENTS),
    }


def search_components(keyword: str) -> dict:
    """Search the component inventory by name, category, or notes."""

    keyword = keyword.strip().lower()

    matches = [
        component
        for component in COMPONENTS
        if keyword in component["name"].lower()
        or keyword in component["category"].lower()
        or keyword in component["notes"].lower()
    ]

    return {
        "search_term": keyword,
        "matches": matches,
        "count": len(matches),
    }


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
    model="gemini-2.5-flash",
    name="component_agent",
    description=(
        "Answers questions about hardware owned, "
        "including component names, categories, "
        "quantities, and inventory searches."
    ),
    instruction="""
    You are a hardware inventory assistant for a firmware engineer.

    Use list_components to list the inventory.
    Use search_components to find specific components.

    Base inventory answers on tool results.
    Do not invent components or quantities.

    If a component is not found, say that it was not found
    in the current inventory.
    """,
    tools=[list_components, search_components],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


# ==========================================
# SPECIALIST AGENT 2: PROJECTS
# ==========================================

project_agent = Agent(
    model="gemini-2.5-flash",
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
    model="gemini-2.5-flash",
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