
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR / "dataset" / "generated" / "human_review_scored.xlsx"
)

OUTPUT_PATH = (
    BASE_DIR / "dataset" / "processed" / "human_validated_dataset.csv"
)

print("Loading human-reviewed dataset...")

df = pd.read_excel(INPUT_PATH)

# Keep only approved records
approved = df[
    df["review_decision"].astype(str).str.strip().str.upper()
    == "APPROVED"
].copy()

# Remove records without human scores
approved["human_final_score"] = pd.to_numeric(
    approved["human_final_score"],
    errors="coerce"
)

approved = approved.dropna(subset=["human_final_score"])

# Validate score range
approved = approved[
    approved["human_final_score"].between(0, 10)
]

# Validate required fields
approved = approved.dropna(
    subset=["question", "answer", "human_feedback"]
)

# Save validated data
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

approved.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

print("\n========== VALIDATION COMPLETE ==========")
print("Original records:", len(df))
print("Approved records:", len(approved))
print("Rejected records:", len(df) - len(approved))
print("Saved file:", OUTPUT_PATH)
