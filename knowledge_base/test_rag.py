from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

BASE_DIR = Path(__file__).resolve().parents[1]
VECTOR_STORE_DIR = BASE_DIR / "knowledge_base" / "vector_store"

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
collection = client.get_collection("interview_knowledge")

query = "Explain Python lists and tuples and their differences"

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\nRAG SEARCH RESULTS")
print("=================")

for i, document in enumerate(results["documents"][0], start=1):
    print(f"\nResult {i}:")
    print(document)
    print("Source:", results["metadatas"][0][i - 1]["source"])
