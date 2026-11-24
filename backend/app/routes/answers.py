
from fastapi import APIRouter, HTTPException
import logging

from backend.app.schemas.answer import AnswerSubmission
from backend.app.services.ml_evaluator import evaluate_answer
from backend.app.services.gemini_service import (
    evaluate_interview_answer
)

router = APIRouter(
    prefix="/answers",
    tags=["Answer Evaluation"]
)

logger = logging.getLogger(__name__)


@router.post("/submit")
def submit_answer(submission: AnswerSubmission):

    word_count = len(submission.answer.split())

    # 1. Evaluate using the experimental PyTorch model
    try:
        ml_evaluation = evaluate_answer(
            question=submission.question,
            answer=submission.answer
        )
    except Exception:
        logger.exception("ML evaluation failed.")
        ml_evaluation = {
            "error": "ML evaluation unavailable"
        }

    # 2. Evaluate using Gemini AI
    try:
        ai_evaluation = evaluate_interview_answer(
            role=submission.role,
            question=submission.question,
            answer=submission.answer,
            category=submission.category
        )

        ai_status = "Completed"

    except Exception:
        logger.exception("Gemini evaluation failed.")
        ai_evaluation = {
            "error": "AI evaluation temporarily unavailable"
        }
        ai_status = "Failed"

    # 3. Return both evaluation results
    return {
        "message": "Answer submitted and evaluated successfully!",
        "candidate_name": submission.candidate_name,
        "role": submission.role,
        "question": submission.question,
        "answer": submission.answer,
        "word_count": word_count,

        "evaluation_status": {
            "ml": "Completed" if "error" not in ml_evaluation else "Failed",
            "gemini": ai_status
        },

        "evaluation": {
            "ml_evaluation": ml_evaluation,
            "ai_evaluation": ai_evaluation
        }
    }
