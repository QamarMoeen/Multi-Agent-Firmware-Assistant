
import json
from pathlib import Path

import faiss


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

INDEX_PATH = DATA_DIR / "project_index.faiss"
CHUNKS_PATH = DATA_DIR / "project_chunks.json"


def save_vector_store(embeddings, chunks):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with CHUNKS_PATH.open("w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    return len(chunks)


def load_vector_store():
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        return None, []

    index = faiss.read_index(str(INDEX_PATH))

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if index.ntotal != len(chunks):
        raise ValueError(
            "FAISS index and chunk metadata do not match. "
            "Rebuild the index by running ingest_projects.py."
        )

    return index, chunks