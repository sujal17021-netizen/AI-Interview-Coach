
from fastapi import APIRouter

router = APIRouter(
    prefix="/questions",
    tags=["Interview Questions"]
)

question_bank = {
    "Python Developer": {
        "easy": [
            "What are Python's main features?",
            "What is the difference between a list and a tuple?",
            "What are Python dictionaries?"
        ],
        "medium": [
            "Explain decorators in Python.",
            "What are generators and how do they work?",
            "Explain Python's memory management."
        ],
        "hard": [
            "Explain Python's Global Interpreter Lock (GIL).",
            "How does asynchronous programming work in Python?",
            "Explain metaclasses in Python."
        ]
    },
    "Machine Learning Engineer": {
        "easy": [
            "What is machine learning?",
            "What is supervised learning?",
            "What is the difference between classification and regression?"
        ],
        "medium": [
            "Explain overfitting and underfitting.",
            "What is gradient descent?",
            "Explain the bias-variance tradeoff."
        ],
        "hard": [
            "Explain how a Random Forest works.",
            "How would you handle class imbalance?",
            "Explain backpropagation in neural networks."
        ]
    }
}


@router.get("/")
def get_questions(
    role: str = "Python Developer",
    difficulty: str = "easy"
):
    role_questions = question_bank.get(role)

    if not role_questions:
        return {
            "error": "Role not found",
            "available_roles": list(question_bank.keys())
        }

    questions = role_questions.get(difficulty.lower())

    if not questions:
        return {
            "error": "Difficulty not found",
            "available_difficulties": list(role_questions.keys())
        }

    return {
        "role": role,
        "difficulty": difficulty,
        "total_questions": len(questions),
        "questions": questions
    }
