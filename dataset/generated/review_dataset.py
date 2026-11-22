
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = BASE_DIR / "dataset" / "generated" / "interview_dataset.csv"
OUTPUT_PATH = BASE_DIR / "dataset" / "generated" / "human_review.xlsx"

df = pd.read_csv(INPUT_PATH)

# Add human review columns
df["human_final_score"] = ""
df["human_feedback"] = ""
df["review_decision"] = "PENDING"

# Reorder important columns
columns = [
    "topic",
    "question",
    "quality_level",
    "answer",
    "correctness",
    "completeness",
    "clarity",
    "relevance",
    "final_score",
    "feedback",
    "human_final_score",
    "human_feedback",
    "review_decision"
]

df = df[columns]

df.to_excel(OUTPUT_PATH, index=False)

print("Human review spreadsheet created!")
print("Total records:", len(df))
print("File:", OUTPUT_PATH)
