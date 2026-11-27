
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app import models

router = APIRouter(
    prefix="/interviews",
    tags=["Interview History"]
)


@router.get("/history")
def get_interview_history(
    db: Session = Depends(get_db)
):
    interviews = (
        db.query(models.Interview)
        .order_by(models.Interview.created_at.desc())
        .all()
    )

    history = []

    for interview in interviews:
        questions = interview.questions

        total_questions = len(questions)
        answered_questions = 0
        scores = []

        for question in questions:
            if question.answer:
                answered_questions += 1

                evaluation = question.answer.evaluation

                if evaluation and evaluation.ml_score is not None:
                    scores.append(evaluation.ml_score)

        average_score = (
            round(sum(scores) / len(scores), 2)
            if scores else None
        )

        status = (
            "Completed"
            if total_questions > 0
            and answered_questions == total_questions
            else "In Progress"
        )

        history.append({
            "interview_id": interview.id,
            "role": interview.role,
            "interview_type": interview.interview_type,
            "difficulty": interview.difficulty,
            "date": (
                interview.created_at.isoformat()
                if interview.created_at else None
            ),
            "status": status,
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "average_score": average_score
        })

    return {
        "total_interviews": len(history),
        "interviews": history
    }
