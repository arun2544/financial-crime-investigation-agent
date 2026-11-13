from sklearn.metrics.pairwise import cosine_similarity
from rag.vector_store import load_policy_index

def retrieve_policy_context(query: str, top_k: int = 4) -> list[dict]:
    index = load_policy_index()
    docs = index["docs"]
    vectorizer = index["vectorizer"]
    matrix = index["matrix"]
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).ravel()
    ranked = scores.argsort()[::-1][:top_k]
    return [
        {"source": docs[i]["source"], "text": docs[i]["text"], "score": round(float(scores[i]), 4)}
        for i in ranked if scores[i] > 0
    ]
