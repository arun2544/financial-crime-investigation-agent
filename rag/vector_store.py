from pathlib import Path
import joblib
from rag.document_loader import load_policy_documents
from rag.embeddings import fit_text_vectors

INDEX_DIR = Path("rag/index")
INDEX_FILE = INDEX_DIR / "policy_index.joblib"

def build_policy_index():
    docs = load_policy_documents()
    texts = [doc["text"] for doc in docs]
    if not texts:
        raise ValueError("No .txt or .pdf policy documents found in data/policies")
    vectorizer, matrix = fit_text_vectors(texts)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"docs": docs, "vectorizer": vectorizer, "matrix": matrix}, INDEX_FILE)
    return len(docs)

def load_policy_index():
    if not INDEX_FILE.exists():
        build_policy_index()
    return joblib.load(INDEX_FILE)
