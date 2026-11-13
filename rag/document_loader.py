from pathlib import Path

def load_policy_documents(directory: str = "data/policies") -> list[dict]:
    docs = []
    for path in Path(directory).glob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".txt":
            text = path.read_text(encoding="utf-8")
        elif path.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader
                text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
            except Exception as exc:
                print(f"Skipping {path.name}: {exc}")
                continue
        else:
            continue
        for idx, chunk in enumerate([p.strip() for p in text.split("\n") if p.strip()]):
            docs.append({"source": path.name, "chunk_id": idx, "text": chunk})
    return docs
