# Firmware Personal Assistant

A local AI-powered assistant for firmware and embedded systems engineers, built with **Google Agent Development Kit (ADK)**. It manages hardware inventory using SQLite and answers questions about completed projects by retrieving relevant information from technical documents using Retrieval-Augmented Generation (RAG).

## Features

* **Multi-agent architecture:** A root agent routes requests to specialized agents.
* **Hardware inventory management:** Search, add, and update component records stored in SQLite.
* **Project knowledge retrieval:** Search project documentation to answer questions about completed projects, embedded systems, firmware, and digital design.
* **Local semantic search:** Use Sentence Transformers to generate embeddings and FAISS to retrieve relevant document passages.
* **Document support:** Load `.txt`, `.md`, and text-based `.pdf` files.
* **Source-aware responses:** Retain source filenames and PDF page numbers to help identify supporting information.
* **Modular codebase:** Keep agent definitions, prompts, database operations, document processing, embeddings, and retrieval logic separate.

## Architecture

The system uses a hierarchical multi-agent design.

```text
User
 |
 v
Root Agent (Google ADK)
 |
 +-----------------------+
 |                       |
 v                       v
Component Agent        RAG Agent
 |                       |
 v                       v
SQLite Database       Document Retriever
                         |
                         v
                    FAISS Index
                         |
                         v
                 Retrieved Passages
                         |
                         v
                    Final Answer
```

### Root Agent

Routes incoming requests to the appropriate specialist.

* Inventory-related requests go to the Component Agent.
* Project and document-related requests go to the RAG Agent.

### Component Agent

Manages the hardware inventory through database functions.

Supported operations include:

* Listing all components.
* Searching components by relevant fields.
* Retrieving a component by ID.
* Adding components.
* Updating component quantities.
* Updating component notes.

### RAG Agent

Answers questions using relevant passages retrieved from the project document collection. It uses the `search_documents` function as a tool.

The RAG Agent does not directly implement the retrieval pipeline; the retrieval logic is maintained in separate modules.

## Technology Stack

| Technology            | Purpose                                       |
| --------------------- | --------------------------------------------- |
| Python                | Application development                       |
| Google ADK            | Multi-agent framework and agent orchestration |
| Gemini                | Language model used by the agents             |
| SQLite                | Hardware inventory storage                    |
| Sentence Transformers | Text embedding generation                     |
| `all-MiniLM-L6-v2`    | Local embedding model                         |
| FAISS                 | Vector similarity search                      |
| PyPDF                 | PDF text extraction                           |
| NumPy                 | Embedding array operations                    |

LangChain is not used.

## Project Structure

```text
Firmware_Personal_Assistant/
├── .env
├── .gitignore
├── README.md
├── ingest_projects.py
├── project_documents/
│   ├── coin_vending_machine.txt
│   ├── esp32_home_automation.txt
│   ├── iot_security_ids.txt
│   └── mips32_processor.txt
├── data/
│   └── components.db
└── firmware_assistant/
    ├── __init__.py
    ├── agent.py
    ├── database.py
    ├── init_db.py
    ├── component_agent/
    │   ├── __init__.py
    │   └── agent.py
    ├── rag_agent/
    │   ├── __init__.py
    │   └── agent.py
    ├── prompts/
    │   ├── __init__.py
    │   └── rag_prompt.py
    └── rag/
        ├── __init__.py
        ├── document_loader.py
        ├── chunker.py
        ├── embeddings.py
        ├── vector_store.py
        └── retriever.py
```

The `data/` directory contains the SQLite database and generated RAG index files. The exact location of the SQLite database depends on the path configured in `database.py`.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Firmware_Personal_Assistant
```

Replace `<repository-url>` with the actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the Google ADK package if it is not already installed in your environment:

```bash
pip install google-adk
```

Install the RAG dependencies:

```bash
pip install sentence-transformers pypdf faiss-cpu
```

NumPy is used by the embedding pipeline and is generally installed as a dependency. If needed, install it explicitly:

```bash
pip install numpy
```

### 4. Configure the Gemini API

Create a `.env` file in the outer project directory.

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key
```

Replace `your_google_api_key` with your own API key.

Keep `.env` private and never commit API keys to version control.

### 5. Initialize the inventory database

If your database has not been initialized, run the initialization script from the project root:

```bash
python -m firmware_assistant.init_db
```

This assumes the initialization script is located at `firmware_assistant/init_db.py` and supports module execution. If your current `init_db.py` is in the outer project root instead, run `python init_db.py`.

Follow the initialization script's behavior regarding existing records to avoid accidentally duplicating seed data.

## Building the RAG Index

The RAG pipeline uses a separate ingestion script to prepare documents for retrieval.

From the outer project directory, run:

```bash
python ingest_projects.py
```

The ingestion process performs the following steps:

1. Loads supported documents from `project_documents/`.
2. Extracts text from text files, Markdown files, and PDFs.
3. Splits document text into overlapping chunks.
4. Generates embeddings using `all-MiniLM-L6-v2`.
5. Builds a FAISS similarity-search index.
6. Saves the index and chunk metadata under `data/`.

The generated files are:

```text
data/
├── project_index.faiss
└── project_chunks.json
```

The first run may download the embedding model and therefore requires an internet connection. Subsequent embedding operations can generally run locally once the model is available.

### Adding or updating documents

1. Place the new document in `project_documents/`.
2. Supported extensions are `.txt`, `.md`, and `.pdf`.
3. Rebuild the index:

```bash
python ingest_projects.py
```

The current implementation does not automatically detect file changes. Rebuild the index after adding, modifying, or removing documents.

## Running the Assistant

From the outer project directory, start ADK Web:

```bash
adk web
```

Open the local address shown in the terminal and select the `firmware_assistant` application.

You can then submit requests through the chat interface.

## Example Queries

### Hardware inventory

* List all components in my inventory.
* Do I have an ESP32 development board?
* How many DHT11 sensors do I have?
* Add a component to my inventory.
* I used two components; update the quantity accordingly.

### Project knowledge

* Explain my ESP32 home automation project.
* Which microcontroller was used in the home automation system?
* What approach did I explore for IoT security?
* Explain my MIPS32 single-cycle processor project.
* What information is documented about the coin vending machine?
* What final accuracy is recorded for my intrusion detection project?

The assistant should acknowledge missing information rather than inventing project details.

## How the RAG Pipeline Works

### 1. Document loading

`document_loader.py` reads supported files and records their source information. PDF page numbers are retained when available.

### 2. Chunking

`chunker.py` divides extracted text into smaller, overlapping passages.

The initial configuration uses approximately 1,000 characters per chunk with 150 characters of overlap. These values can be adjusted as retrieval quality is evaluated.

### 3. Embedding generation

`embeddings.py` uses the `all-MiniLM-L6-v2` Sentence Transformers model to represent text as numerical vectors.

The same embedding model is used for both stored passages and user queries.

### 4. Vector storage

`vector_store.py` builds and persists a FAISS index using normalized embeddings and inner-product similarity search.

Chunk text and source metadata are stored separately in `project_chunks.json`.

### 5. Retrieval

`retriever.py` embeds the user's query, searches the FAISS index, and returns the highest-ranked passages along with source information.

### 6. Answer generation

The RAG Agent receives the retrieved passages and uses the Gemini language model to formulate a response based on the available evidence.

## Testing

Run the available inventory tests from the outer project directory:

```bash
pytest
```

If your RAG tests require the index to exist, build it before running those tests:

```bash
python ingest_projects.py
pytest
```

Test both inventory operations and document retrieval. Useful checks include:

* Inventory searches return database-backed records.
* Inventory changes update the stored database correctly.
* Relevant document passages are retrieved for project questions.
* Retrieved passages retain their source metadata.
* Questions about undocumented facts do not lead to fabricated claims.
* Adding a new document and rebuilding the index makes its contents searchable.

## Current Limitations

* **Document updates:** The index must be rebuilt manually after document changes.
* **Scanned PDFs:** PyPDF extracts embedded text but does not perform OCR on scanned pages.
* **Retrieval quality:** Results depend on document quality, chunking choices, embedding similarity, and the relevance of the available information.
* **Source verification:** Source metadata helps locate evidence, but similarity scores alone do not prove that a passage supports a claim.
* **Knowledge coverage:** The assistant can only retrieve information available in the indexed documents.
* **Model access:** Agent responses require a working Gemini API configuration.
* **Local storage:** The SQLite database, FAISS index, and chunk metadata are stored locally; generated files should be protected if they contain private information.

## Future Improvements

* Add automatic document-change detection and index updates.
* Add OCR support for scanned PDFs.
* Improve retrieval with metadata filters, hybrid keyword and semantic search, and reranking.
* Add datasheet-specific retrieval and hardware compatibility checks.
* Add bill of materials generation based on project requirements and inventory.
* Add inventory-low alerts and component recommendations.
* Add more comprehensive automated tests for retrieval and agent routing.
* Improve source citations and answer evaluation.

## Security and Data Management

* Never commit `.env` or API credentials.
* Avoid committing private documents or generated chunk files containing their extracted content.
* Keep database backups before making substantial inventory changes.
* Validate component quantities and database operations.
* Review retrieved evidence before relying on safety-critical electrical or hardware compatibility recommendations.

## License

Add a license before publicly distributing the project. Until a license is specified, the repository should not be assumed to grant permissions for reuse or redistribution.
