
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Locate the project root
BASE_DIR = Path(__file__).resolve().parents[3]

# Load environment variables
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash"
EVALUATION_MODEL_NAME = "gemini-2.5-flash"

def generate_interview_questions(
    role: str,
    difficulty: str,
    interview_type: str,
    question_count: int
):

    prompt = f"""
You are an experienced technical and HR interviewer.

Generate exactly {question_count} interview questions.

Candidate details:
Job Role: {role}
Difficulty: {difficulty}
Interview Type: {interview_type}

Instructions:

1. Generate relevant questions for the selected job role.
2. Questions must match the selected difficulty.
3. For Technical interviews, generate technical questions.
4. For HR interviews, generate behavioral and situational questions.
5. For Mixed interviews, alternate between technical and HR questions.
6. Avoid generic or repetitive questions.
7. Make questions realistic for actual job interviews.

Return ONLY valid JSON in this exact format:

{{
    "questions": [
        {{
            "question": "Question text",
            "category": "Technical"
        }},
        {{
            "question": "Question text",
            "category": "HR"
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model=EVALUATION_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    result = json.loads(response.text)

    questions = result.get("questions")

    if not isinstance(questions, list):
        raise ValueError("Invalid question format returned by Gemini.")

    if len(questions) != question_count:
        raise ValueError(
            f"Expected {question_count} questions, received {len(questions)}."
        )

    for item in questions:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("question"), str)
            or not item["question"].strip()
            or item.get("category") not in ["Technical", "HR"]
        ):
            raise ValueError("Gemini returned an invalid question.")

    return questions

def evaluate_interview_answer(
    role: str,
    question: str,
    answer: str,
    category: str = "Technical"
):
    """
    Evaluate a candidate's interview answer using Gemini.
    Returns structured feedback and scores.
    """

    prompt = f"""
You are an experienced professional interviewer.

Evaluate the candidate's answer objectively.

Candidate's job role: {role}
Question category: {category}
Interview question: {question}
Candidate's answer: {answer}

Evaluate the answer on these four dimensions:

1. Technical accuracy: Is the information correct?
2. Relevance: Does the answer address the question?
3. Completeness: Does the answer cover important points?
4. Clarity: Is the answer understandable and well structured?

Scoring:
- Give each dimension a score between 0 and 10.
- Do not reward length alone.
- Do not invent experience or facts.
- For HR answers, evaluate relevance, authenticity,
  completeness, and clarity rather than technical correctness.
- Provide constructive and specific feedback.

Return ONLY valid JSON in this format:

{{
    "technical_accuracy": 0,
    "relevance": 0,
    "completeness": 0,
    "clarity": 0,
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "improvements": [
        "Improvement 1",
        "Improvement 2"
    ],
    "improved_answer": "A stronger example answer",
    "overall_feedback": "Brief overall evaluation"
}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty evaluation.")

    result = json.loads(response.text)

    score_fields = [
        "technical_accuracy",
        "relevance",
        "completeness",
        "clarity"
    ]

    for field in score_fields:
        score = result.get(field)

        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 10
        ):
            raise ValueError(f"Invalid evaluation score: {field}")

    for field in ["strengths", "improvements"]:
        if (
            not isinstance(result.get(field), list)
            or not all(
                isinstance(item, str) for item in result[field]
            )
        ):
            raise ValueError(f"Invalid evaluation field: {field}")

    if not isinstance(result.get("improved_answer"), str):
        raise ValueError("Invalid improved answer.")

    if not isinstance(result.get("overall_feedback"), str):
        raise ValueError("Invalid overall feedback.")

    return result
