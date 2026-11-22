
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Find project directories
BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "dataset" / "raw" / "interview_answers.csv"
OUTPUT_PATH = BASE_DIR / "dataset" / "processed"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Load dataset
print("Loading interview dataset...")

df = pd.read_csv(DATASET_PATH)

print("Total records:", len(df))

# Combine question and answer
texts = (
    "Question: " + df["question"].astype(str)
    + " Answer: " + df["answer"].astype(str)
).tolist()

# Load Sentence Transformer
print("\nLoading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Generate embeddings
print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

# Save embeddings and labels
np.save(OUTPUT_PATH / "answer_embeddings.npy", embeddings)

np.save(
    OUTPUT_PATH / "answer_scores.npy",
    df["score"].to_numpy(dtype=np.float32)
)

print("\nEmbedding generation completed!")
print("Embedding shape:", embeddings.shape)
print("Score shape:", df["score"].to_numpy().shape)

print("\nFiles saved inside:", OUTPUT_PATH)
