from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

BASE_DIR = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = BASE_DIR / "knowledge_base" / "documents"
VECTOR_STORE_DIR = BASE_DIR / "knowledge_base" / "vector_store"

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))

collection = client.get_or_create_collection(
    name="interview_knowledge",
    metadata={"description": "Technical interview knowledge base"}
)

documents = []
ids = []
metadatas = []

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    content = file_path.read_text(encoding="utf-8")

    # Split content into paragraph-based chunks
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

    for index, chunk in enumerate(chunks):
        documents.append(chunk)
        ids.append(f"{file_path.stem}_{index}")
        metadatas.append({
            "source": file_path.name,
            "chunk": index
        })

if not documents:
    raise ValueError("No text documents found in the knowledge_base/documents folder.")

print(f"Found {len(documents)} knowledge chunks.")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
).tolist()

# Replace existing records to avoid duplicate IDs
existing = collection.get()
if existing["ids"]:
    collection.delete(ids=existing["ids"])

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("\nRAG knowledge base created successfully!")
print("Total chunks stored:", collection.count())
print("Vector store:", VECTOR_STORE_DIR)

