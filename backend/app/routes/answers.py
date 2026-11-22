
from fastapi import APIRouter
from backend.app.schemas.answer import AnswerSubmission
from backend.app.services.ml_evaluator import evaluate_answer

router = APIRouter(
    prefix="/answers",
    tags=["Answer Evaluation"]
)


@router.post("/submit")
def submit_answer(submission: AnswerSubmission):

    word_count = len(submission.answer.split())

    # Evaluate the candidate's answer using the trained ML model
    evaluation = evaluate_answer(
        question=submission.question,
        answer=submission.answer
    )

    return {
        "message": "Answer submitted and evaluated successfully!",
        "candidate_name": submission.candidate_name,
        "role": submission.role,
        "question": submission.question,
        "answer": submission.answer,
        "word_count": word_count,
        "evaluation_status": "ML evaluation completed",
        "evaluation": evaluation
    }
