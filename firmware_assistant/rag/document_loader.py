
from pathlib import Path
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "project_documents"

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_documents(directory=DOCUMENTS_DIR):
    documents = []

    if not directory.exists():
        raise FileNotFoundError(
            f"Document folder not found: {directory}"
        )

    for file_path in sorted(directory.rglob("*")):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        source = file_path.relative_to(directory).as_posix()

        try:
            if file_path.suffix.lower() == ".pdf":
                reader = PdfReader(str(file_path))

                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""

                    if text.strip():
                        documents.append({
                            "text": text,
                            "source": source,
                            "page": page_number,
                        })

            else:
                text = file_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )

                if text.strip():
                    documents.append({
                        "text": text,
                        "source": source,
                        "page": None,
                    })

        except Exception as error:
            print(f"Skipping {source}: {error}")

    return documents