from sentence_transformers import SentenceTransformer
import numpy as np


# Replace these example records with your existing project records.
PROJECTS = [
    {
        "name": "ESP32 Home Automation",
        "description": (
            "A home automation project using an ESP32 microcontroller, "
            "DHT11 temperature and humidity sensor, IR remote control, "
            "and Blynk for monitoring and control."
        ),
        "technologies": "ESP32, DHT11, IR, Blynk",
    },
    {
        "name": "MIPS32 Single-Cycle Processor",
        "description": (
            "A single-cycle MIPS32 processor implemented in VHDL "
            "for FPGA hardware."
        ),
        "technologies": "VHDL, MIPS32, FPGA",
    },
    {
        "name": "Coin Vending Machine",
        "description": (
            "A digital coin vending machine designed and implemented "
            "using VHDL."
        ),
        "technologies": "VHDL, digital logic",
    },
]


# Load a local embedding model.
model = SentenceTransformer("all-MiniLM-L6-v2")


def make_project_text(project):
    """Combine a project's searchable information into one text."""
    return (
        f"Project: {project['name']}. "
        f"Description: {project['description']} "
        f"Technologies: {project['technologies']}"
    )


# Embed project records once when this module loads.
project_texts = [make_project_text(p) for p in PROJECTS]

project_embeddings = model.encode(
    project_texts,
    normalize_embeddings=True,
)


def search_projects(query: str) -> str:
    """Retrieve project records most relevant to a question."""

    if not query.strip():
        return "Please provide a project-related question."

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )[0]

    # Normalized vectors: dot product gives cosine similarity.
    scores = np.dot(project_embeddings, query_embedding)

    # Return the three highest-scoring projects.
    top_indices = np.argsort(scores)[::-1][:3]

    results = []

    for index in top_indices:
        project = PROJECTS[index]
        score = float(scores[index])

        results.append(
            f"Project: {project['name']}\n"
            f"Description: {project['description']}\n"
            f"Technologies: {project['technologies']}\n"
            f"Similarity score: {score:.3f}"
        )

    return "\n\n".join(results)