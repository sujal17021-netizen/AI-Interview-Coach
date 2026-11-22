
from pydantic import BaseModel, Field


class AnswerSubmission(BaseModel):
    candidate_name: str = Field(min_length=2, max_length=100)
    role: str
    question: str = Field(min_length=5)
    answer: str = Field(min_length=10)
