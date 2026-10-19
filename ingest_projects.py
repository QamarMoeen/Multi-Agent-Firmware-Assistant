
from firmware_assistant.rag.retriever import build_index


if __name__ == "__main__":
    result = build_index()
    print(result)