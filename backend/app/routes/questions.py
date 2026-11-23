
from fastapi import APIRouter, HTTPException, Query
import random
import logging

from backend.app.services.question_bank import question_bank
from backend.app.services.gemini_service import (
    generate_interview_questions
)

router = APIRouter(
    prefix="/questions",
    tags=["Interview Questions"]
)

logger = logging.getLogger(__name__)


@router.get("/")
def get_questions(
    role: str = "Python Developer",
    difficulty: str = "easy",
    interview_type: str = "Technical",
    question_count: int = Query(default=3, ge=1, le=20),
    duration: int = Query(default=30, ge=5, le=180),
    use_ai: bool = True
):

    difficulty = difficulty.lower()
    interview_type = interview_type.capitalize()

    if role not in question_bank:
        raise HTTPException(
            status_code=404,
            detail="Role not found."
        )

    if difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid difficulty."
        )

    if interview_type not in ["Technical", "HR", "Mixed"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid interview type."
        )

    role_data = question_bank[role]

    technical_questions = role_data["technical"][difficulty]
    hr_questions = role_data["hr"]

    # Try Gemini first
    if use_ai:
        try:
            selected_questions = generate_interview_questions(
                role=role,
                difficulty=difficulty,
                interview_type=interview_type,
                question_count=question_count
            )

            # Verify question categories
            if interview_type == "Technical":
                valid = all(
                    q["category"] == "Technical"
                    for q in selected_questions
                )
            elif interview_type == "HR":
                valid = all(
                    q["category"] == "HR"
                    for q in selected_questions
                )
            else:
                categories = [
                    q["category"] for q in selected_questions
                ]
                valid = (
                    categories.count("Technical")
                    == (question_count + 1) // 2
                    and categories.count("HR")
                    == question_count // 2
                )

            if not valid:
                raise ValueError(
                    "Gemini returned incorrect question categories."
                )

            source = "Gemini AI"

        except Exception:
            logger.exception(
                "Gemini question generation failed. Using fallback."
            )
            selected_questions = None

    else:
        selected_questions = None

    # Fallback to predefined question bank
    if selected_questions is None:

        if interview_type == "Technical":
            available_questions = technical_questions

        elif interview_type == "HR":
            available_questions = hr_questions

        else:
            available_questions = (
                technical_questions + hr_questions
            )

        if question_count > len(available_questions):
            raise HTTPException(
                status_code=503,
                detail=(
                    "AI generation is unavailable and the "
                    "predefined question bank does not contain "
                    "enough questions for this selection."
                )
            )

        if interview_type == "Technical":
            selected_questions = random.sample(
                technical_questions, question_count
            )
            selected_questions = [
                {
                    "question": q,
                    "category": "Technical"
                }
                for q in selected_questions
            ]

        elif interview_type == "HR":
            selected_questions = random.sample(
                hr_questions, question_count
            )
            selected_questions = [
                {
                    "question": q,
                    "category": "HR"
                }
                for q in selected_questions
            ]

        else:
            technical_count = (question_count + 1) // 2
            hr_count = question_count // 2

            selected_technical = random.sample(
                technical_questions, technical_count
            )

            selected_hr = random.sample(
                hr_questions, hr_count
            )

            selected_questions = []

            for i in range(question_count):
                if i % 2 == 0:
                    selected_questions.append({
                        "question": selected_technical[i // 2],
                        "category": "Technical"
                    })
                else:
                    selected_questions.append({
                        "question": selected_hr[i // 2],
                        "category": "HR"
                    })

        source = "Predefined Question Bank"

    return {
        "role": role,
        "difficulty": difficulty,
        "interview_type": interview_type,
        "duration": duration,
        "requested_questions": question_count,
        "total_questions": len(selected_questions),
        "generation_source": source,
        "questions": selected_questions
    }
