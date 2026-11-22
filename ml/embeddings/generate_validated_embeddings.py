
import pandas as pd
import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR / "dataset" / "processed"
    / "human_validated_dataset.csv"
)

OUTPUT_DIR = BASE_DIR / "dataset" / "processed"

EMBEDDING_PATH = OUTPUT_DIR / "validated_embeddings.npy"
SCORE_PATH = OUTPUT_DIR / "validated_scores.npy"

print("Loading human-reviewed dataset...")

df = pd.read_csv(DATA_PATH)

# Use the human score, NOT the Gemini score
texts = (
    "Question: " + df["question"].astype(str)
    + " Answer: " + df["answer"].astype(str)
).tolist()

scores = df["human_final_score"].to_numpy(dtype=np.float32)

print("Loading Sentence Transformer...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

np.save(EMBEDDING_PATH, embeddings)
np.save(SCORE_PATH, scores)

print("\n========== EMBEDDING GENERATION COMPLETE ==========")
print("Total answers:", len(texts))
print("Embedding shape:", embeddings.shape)
print("Score shape:", scores.shape)
print("Saved embeddings:", EMBEDDING_PATH)
print("Saved scores:", SCORE_PATH)
