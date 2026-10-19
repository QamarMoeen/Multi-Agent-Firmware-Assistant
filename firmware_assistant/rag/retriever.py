
from .document_loader import load_documents
from .chunker import chunk_documents
from .embeddings import embed_texts, embed_query
from .vector_store import save_vector_store, load_vector_store


def build_index():
    documents = load_documents()

    if not documents:
        return (
            "No readable documents were found in project_documents/. "
            "Add TXT, Markdown, or text-based PDF files first."
        )

    chunks = chunk_documents(documents)

    if not chunks:
        return "No text chunks were generated from the documents."

    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    save_vector_store(embeddings, chunks)

    return (
        f"Index built successfully. "
        f"Loaded {len(documents)} document sections "
        f"and indexed {len(chunks)} chunks."
    )


def search_documents(query: str, top_k: int = 4) -> str:
    """Search project documents for passages relevant to a question."""

    if not query.strip():
        return "Please provide a question to search for."

    if top_k < 1:
        return "top_k must be at least 1."

    index, chunks = load_vector_store()

    if index is None:
        return (
            "The document index does not exist yet. "
            "Run python ingest_projects.py from the project root first."
        )

    query_embedding = embed_query(query)
    number_to_search = min(top_k, index.ntotal)

    scores, indices = index.search(
        query_embedding,
        number_to_search,
    )

    results = []

    for score, chunk_index in zip(scores[0], indices[0]):
        if chunk_index < 0:
            continue

        chunk = chunks[int(chunk_index)]
        source = chunk["source"]
        page = chunk.get("page")

        location = f"{source}, page {page}" if page else source

        results.append(
            f"Source: {location}\n"
            f"Similarity: {float(score):.3f}\n"
            f"Passage:\n{chunk['text']}"
        )

    if not results:
        return "No matching passages were found in the indexed documents."

    return "\n\n---\n\n".join(results)