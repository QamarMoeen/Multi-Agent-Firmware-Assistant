# Firmware Engineering Assistant

A personal assistant for firmware and embedded systems engineers, built with Python and Google's Agent Development Kit (ADK).

## Features

* **Component Agent:** Searches a local SQLite inventory of hardware components.
* **Project Agent:** Searches project descriptions using a basic keyword-matching tool.
* **Root Agent:** Routes user requests to the appropriate specialist.
* **Local storage:** Uses SQLite for component inventory data.

## Architecture

The root agent delegates requests to specialist agents. The component agent queries SQLite through predefined Python functions, while the project agent searches project records.

## Technology Stack

* Python
* Google ADK
* Gemini API
* SQLite
* Git

## Getting Started

1. Install Python and create a virtual environment.

2. Install the dependencies with `pip install google-adk`.

3. Copy `.env.example` to `.env` and configure your own API key.

4. Initialize the sample inventory database:

   `python -m firmware_assistant.init_db`

5. Start the development interface:

   `adk web`

6. Select the firmware assistant and test component queries.

## Data and Privacy

The database initialization script creates demonstration records. The generated local database is excluded from Git.

Do not commit API keys, private inventory records, confidential project documentation, or other sensitive information.

## Current Limitations

* Project search uses keyword matching, not semantic RAG.
* Component specifications may be incomplete and should be verified against official datasheets.
* The current inventory tools support reading and searching records; editing inventory will be added separately.

## Roadmap

* Add component creation, editing, and quantity updates.
* Add RAG over completed project descriptions.
* Retrieve component datasheets.
* Add troubleshooting knowledge and inventory-aware recommendations.
