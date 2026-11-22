
import os
import csv
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Project configuration
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

OUTPUT_PATH = (
    BASE_DIR / "dataset" / "generated" / "interview_dataset.csv"
)

MODEL_NAME = "gemini-3.5-flash"

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Interview questions
QUESTIONS = [
    {
        "topic": "Python",
        "question": "What is the difference between a list and a tuple in Python?"
    },
    {
        "topic": "Python",
        "question": "What are decorators in Python?"
    },
    {
        "topic": "DSA",
        "question": "Explain the difference between an array and a linked list."
    },
    {
        "topic": "DSA",
        "question": "What is the time complexity of binary search?"
    },
    {
        "topic": "Machine Learning",
        "question": "Explain overfitting in machine learning."
    },
    {
        "topic": "Machine Learning",
        "question": "What is the difference between supervised and unsupervised learning?"
    },
    {
        "topic": "Deep Learning",
        "question": "What is the role of an activation function in a neural network?"
    },
    {
        "topic": "SQL",
        "question": "Explain the difference between INNER JOIN and LEFT JOIN."
    }
]

FIELDS = [
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
    "review_status"
]


def generate_answers(topic, question):

    prompt = f"""
You are an expert technical interview evaluator.

Generate exactly FOUR realistic candidate answers to this interview question.

Topic: {topic}
Question: {question}

The four quality levels must be:

1. Poor: Major conceptual mistakes or missing understanding.
2. Average: Some correct understanding but important gaps.
3. Good: Mostly correct and sufficiently explained.
4. Excellent: Technically accurate, complete and clearly explained.

IMPORTANT:
- Make all four answers genuinely different in quality.
- Answers should sound like real candidates speaking in an interview.
- Do not make poor answers artificially absurd.
- Do not include the question in the answer.
- Do not invent facts or misleading technical explanations.

Evaluate each answer using scores from 0 to 10:

correctness: Technical accuracy (40% weight)
completeness: Coverage of important concepts (30% weight)
clarity: Explanation quality (20% weight)
relevance: How directly it answers the question (10% weight)

Return ONLY valid JSON in this exact structure:

{{
  "answers": [
    {{
      "quality_level": "Poor",
      "answer": "Candidate answer here",
      "correctness": 2,
      "completeness": 2,
      "clarity": 4,
      "relevance": 3,
      "feedback": "Explanation of strengths and weaknesses"
    }}
  ]
}}

Include exactly four objects, one for each quality level.
All scores must be numbers between 0 and 10.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    data = json.loads(response.text)

    if len(data["answers"]) != 4:
        raise ValueError("Expected exactly four generated answers.")

    return data["answers"]


def main():

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    records = []

    print("Starting LLM dataset generation...\n")

    for index, item in enumerate(QUESTIONS, start=1):

        print(
            f"Generating {index}/{len(QUESTIONS)}: "
            f"{item['question']}"
        )

        try:
            answers = generate_answers(
                item["topic"],
                item["question"]
            )

            for answer_data in answers:

                # Validate rubric scores
                score_names = [
                    "correctness",
                    "completeness",
                    "clarity",
                    "relevance"
                ]

                scores = {}

                for name in score_names:
                    value = float(answer_data[name])

                    if not 0 <= value <= 10:
                        raise ValueError(f"Invalid {name} score")

                    scores[name] = value

                # Calculate weighted score locally
                final_score = (
                    0.40 * scores["correctness"]
                    + 0.30 * scores["completeness"]
                    + 0.20 * scores["clarity"]
                    + 0.10 * scores["relevance"]
                )

                records.append({
                    "topic": item["topic"],
                    "question": item["question"],
                    "quality_level": answer_data["quality_level"],
                    "answer": answer_data["answer"],
                    **scores,
                    "final_score": round(final_score, 2),
                    "feedback": answer_data["feedback"],
                    "review_status": "PENDING"
                })

        except Exception as error:
            print(f"Error generating this question: {error}")

    # Save generated records
    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    print("\n========== GENERATION COMPLETE ==========")
    print("Total generated answers:", len(records))
    print("Output file:", OUTPUT_PATH)
    print("Human review status: PENDING")


if __name__ == "__main__":
    main()
