
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging

from backend.app.database import get_db
from backend.app import models
from backend.app.schemas.answer import AnswerSubmission
from backend.app.services.ml_evaluator import evaluate_answer
from backend.app.services.gemini_service import evaluate_interview_answer

router = APIRouter(
    prefix="/answers",
    tags=["Answer Evaluation"]
)

logger = logging.getLogger(__name__)


@router.post("/submit")
def submit_answer(
    submission: AnswerSubmission,
    db: Session = Depends(get_db)
):
    # Verify that the question exists
    question_record = db.query(models.Question).filter(
        models.Question.id == submission.question_id
    ).first()

    if not question_record:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    # Verify the supplied question matches the database record
    if question_record.question_text != submission.question:
        raise HTTPException(
            status_code=400,
            detail="Submitted question does not match question ID."
        )

    if question_record.category != submission.category:
        raise HTTPException(
            status_code=400,
            detail="Submitted category does not match question record."
        )

    # Prevent duplicate submissions
    existing_answer = db.query(models.Answer).filter(
        models.Answer.question_id == submission.question_id
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=409,
            detail="An answer has already been submitted for this question."
        )

    word_count = len(submission.answer.split())

    # PyTorch evaluation
    try:
        ml_evaluation = evaluate_answer(
            question=submission.question,
            answer=submission.answer
        )
    except Exception:
        logger.exception("ML evaluation failed.")
        ml_evaluation = {"error": "ML evaluation unavailable"}

    # Gemini evaluation
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

    # Save answer and evaluation together
    try:
        new_answer = models.Answer(
            question_id=submission.question_id,
            answer_text=submission.answer,
            word_count=word_count
        )

        db.add(new_answer)
        db.flush()

        ml_score = ml_evaluation.get("predicted_score")

        ai_scores = ai_evaluation if "error" not in ai_evaluation else {}

        new_evaluation = models.Evaluation(
            answer_id=new_answer.id,
            ml_score=ml_score,
            technical_accuracy=ai_scores.get("technical_accuracy"),
            relevance=ai_scores.get("relevance"),
            completeness=ai_scores.get("completeness"),
            clarity=ai_scores.get("clarity"),
            strengths=ai_scores.get("strengths"),
            improvements=ai_scores.get("improvements"),
            improved_answer=ai_scores.get("improved_answer"),
            overall_feedback=ai_scores.get("overall_feedback"),
            evaluation_status=(
                "Completed" if ai_status == "Completed" else "Partial"
            )
        )

        db.add(new_evaluation)
        db.commit()

    except Exception:
        db.rollback()
        logger.exception("Failed to save answer and evaluation.")

        raise HTTPException(
            status_code=500,
            detail="Failed to save answer and evaluation."
        )

    return {
        "message": "Answer submitted and evaluated successfully!",
        "candidate_name": submission.candidate_name,
        "role": submission.role,
        "question": submission.question,
        "answer": submission.answer,
        "word_count": word_count,

        "evaluation_status": {
            "ml": (
                "Completed"
                if "error" not in ml_evaluation
                else "Failed"
            ),
            "gemini": ai_status
        },

        "evaluation": {
            "ml_evaluation": ml_evaluation,
            "ai_evaluation": ai_evaluation
        }
    }
