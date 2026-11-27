
from typing import Literal
from pydantic import BaseModel, Field


class AnswerSubmission(BaseModel):

    candidate_name: str = Field(
        min_length=2,
        max_length=100
    )

    role: str

    question_id: int = Field(gt=0)

    question: str = Field(min_length=5)

    answer: str = Field(min_length=10)

    category: Literal["Technical", "HR"] = "Technical"
