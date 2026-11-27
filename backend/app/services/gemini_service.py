
import os
import json
import time
import logging
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# CONFIGURATION
# ==========================================

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[3]

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)


# Separate models for different tasks

QUESTION_MODEL = "gemini-3.5-flash"

EVALUATION_MODELS = [
     "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite"
]


# ==========================================
# COMMON GEMINI GENERATION WITH FALLBACK
# ==========================================



def generate_json_with_fallback(
    prompt: str,
    models: list[str],
    temperature: float = 0.3
):
    """
    Generate JSON using Gemini models.

    Retries temporary 503 and 429 errors using
    exponential backoff, then switches models.
    """

    last_error = None
    max_retries = 2

    for model in models:

        for attempt in range(max_retries + 1):

            try:
                logger.warning(
                    "Trying Gemini model %s, attempt %s",
                    model,
                    attempt + 1
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        response_mime_type="application/json"
                    )
                )

                if not response.text:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                return json.loads(response.text)
                logger.warning(
                     "GEMINI SUCCESS: model=%s, attempt=%s",
    model,
    attempt + 1
)
                return result

            except Exception as error:

                last_error = error
                error_text = str(error)

                logger.warning(
                    "Gemini model %s failed: %s",
                    model,
                    error
                )

                is_temporary = (
                    "503" in error_text
                    or "429" in error_text
                )

                if is_temporary and attempt < max_retries:

                    # Calculate wait time BEFORE logging it
                    wait_time = 2 ** (attempt + 1)

                    logger.warning(
                        "RETRYING GEMINI: model=%s, "
                        "attempt=%s, waiting=%s seconds",
                        model,
                        attempt + 1,
                        wait_time
                    )

                    time.sleep(wait_time)
                    continue

                logger.warning(
                    "Moving to the next Gemini model."
                )

                break

    raise RuntimeError(
        "All configured Gemini models failed."
    ) from last_error




# ==========================================
# GENERATE INTERVIEW QUESTIONS
# ==========================================

def generate_interview_questions(
    role: str,
    difficulty: str,
    interview_type: str,
    question_count: int,
    context: str = ""
):

    prompt = f"""
You are an experienced technical and HR interviewer.

Generate exactly {question_count} interview questions.

Candidate details:
Job Role: {role}
Difficulty: {difficulty}
Interview Type: {interview_type}
Relevant Knowledge Retrieved from RAG:
{context}

Use the retrieved knowledge when relevant to generate accurate,
role-specific technical questions. Do not force unrelated
knowledge into the questions.

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

    result = generate_json_with_fallback(
        prompt=prompt,
        models=[QUESTION_MODEL],
        temperature=0.7
    )

    questions = result.get("questions")

    if not isinstance(questions, list):
        raise ValueError(
            "Invalid question format returned by Gemini."
        )

    if len(questions) != question_count:
        raise ValueError(
            f"Expected {question_count} questions, "
            f"received {len(questions)}."
        )

    for item in questions:

        if (
            not isinstance(item, dict)
            or not isinstance(item.get("question"), str)
            or not item["question"].strip()
            or item.get("category") not in ["Technical", "HR"]
        ):
            raise ValueError(
                "Gemini returned an invalid question."
            )

    # Validate category distribution
    categories = [item["category"] for item in questions]

    if interview_type == "Technical":
        if any(c != "Technical" for c in categories):
            raise ValueError("Invalid technical question categories.")

    elif interview_type == "HR":
        if any(c != "HR" for c in categories):
            raise ValueError("Invalid HR question categories.")

    elif interview_type == "Mixed":

        expected_technical = (question_count + 1) // 2
        expected_hr = question_count // 2

        if (
            categories.count("Technical") != expected_technical
            or categories.count("HR") != expected_hr
        ):
            raise ValueError(
                "Gemini returned an incorrect Mixed question distribution."
            )

    return questions


# ==========================================
# EVALUATE INTERVIEW ANSWER
# ==========================================

def evaluate_interview_answer(
    role: str,
    question: str,
    answer: str,
    category: str = "Technical"
):
    """
    Evaluate candidate answers using Gemini.
    Supports Technical and HR interviews.
    """

    if category not in ["Technical", "HR"]:
        raise ValueError("Invalid interview category.")

    if category == "Technical":

        evaluation_criteria = """
1. Technical accuracy: Is the technical information correct?
2. Relevance: Does the answer address the question?
3. Completeness: Does the answer cover important technical points?
4. Clarity: Is the explanation understandable and structured?
"""

        accuracy_description = (
            "Evaluate technical correctness and conceptual understanding."
        )

    else:

        evaluation_criteria = """
1. Authenticity: Does the answer sound realistic and credible?
2. Relevance: Does the answer address the behavioral question?
3. Completeness: Does it explain the situation, action and result?
4. Clarity: Is the answer understandable and well structured?
"""

        accuracy_description = (
            "Evaluate authenticity and credibility rather than "
            "technical knowledge."
        )

    prompt = f"""
You are an experienced professional interviewer.

Evaluate the candidate's answer objectively.

Candidate's job role: {role}
Question category: {category}

Interview question:
{question}

Candidate's answer:
{answer}

Evaluation criteria:

{evaluation_criteria}

Scoring instructions:

- Give each dimension a score between 0 and 10.
- Do not reward answer length alone.
- Do not invent experience or facts.
- {accuracy_description}
- Provide constructive and specific feedback.
- Evaluate only the answer provided by the candidate.

For Technical questions, use:
technical_accuracy, relevance, completeness, clarity.

For HR questions, use:
technical_accuracy as the authenticity and credibility score,
relevance, completeness, clarity.

Return ONLY valid JSON in this exact format:

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

    result = generate_json_with_fallback(
        prompt=prompt,
        models=EVALUATION_MODELS,
        temperature=0.3
    )

    # Validate scores
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
            raise ValueError(
                f"Invalid evaluation score: {field}"
            )

    # Validate feedback lists
    for field in ["strengths", "improvements"]:

        if (
            not isinstance(result.get(field), list)
            or not all(
                isinstance(item, str)
                for item in result[field]
            )
        ):
            raise ValueError(
                f"Invalid evaluation field: {field}"
            )

    # Validate text feedback
    for field in [
        "improved_answer",
        "overall_feedback"
    ]:

        if (
            not isinstance(result.get(field), str)
            or not result[field].strip()
        ):
            raise ValueError(
                f"Invalid evaluation field: {field}"
            )

    return result
