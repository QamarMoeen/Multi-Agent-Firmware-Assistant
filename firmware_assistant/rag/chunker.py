
def chunk_documents(
    documents,
    chunk_size=1000,
    overlap=150,
):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    chunks = []

    for document in documents:
        text = document["text"].strip()
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                # Prefer a paragraph or sentence boundary.
                minimum_boundary = start + chunk_size // 2

                boundary = max(
                    text.rfind("\n", minimum_boundary, end),
                    text.rfind(". ", minimum_boundary, end),
                    text.rfind("? ", minimum_boundary, end),
                    text.rfind("! ", minimum_boundary, end),
                )

                if boundary > start:
                    end = boundary + 1

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"],
                })

            if end >= len(text):
                break

            start = max(end - overlap, start + 1)

    return chunks