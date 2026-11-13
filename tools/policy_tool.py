from rag.retriever import retrieve_policy_context

def get_policy_context(query: str, top_k: int = 4) -> list[dict]:
    return retrieve_policy_context(query, top_k=top_k)
