from rag.vector_store import build_policy_index

if __name__ == "__main__":
    count = build_policy_index()
    print(f"Indexed {count} policy text chunks.")
