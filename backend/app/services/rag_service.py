from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[3]
VECTOR_STORE_DIR = BASE_DIR / "knowledge_base" / "vector_store"

_model = None
_collection = None


def get_rag_resources():
    global _model, _collection

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    if _collection is None:
        client = chromadb.PersistentClient(
            path=str(VECTOR_STORE_DIR)
        )
        _collection = client.get_collection(
            name="interview_knowledge"
        )

    return _model, _collection


def retrieve_context(query: str, top_k: int = 3) -> str:
    model, collection = get_rag_resources()

    if collection.count() == 0:
        return ""

    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(top_k, collection.count())
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)
