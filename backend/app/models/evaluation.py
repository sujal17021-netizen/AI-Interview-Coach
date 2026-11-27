
from sqlalchemy import (
    Column, Integer, Float,String, Text, ForeignKey, JSON, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    answer_id = Column(
        Integer,
        ForeignKey("answers.id"),
        nullable=False,
        unique=True
    )

    # Experimental PyTorch model score
    ml_score = Column(Float, nullable=True)

    # Gemini evaluation scores
    technical_accuracy = Column(Float, nullable=True)
    relevance = Column(Float, nullable=True)
    completeness = Column(Float, nullable=True)
    clarity = Column(Float, nullable=True)

    # AI-generated feedback
    strengths = Column(JSON, nullable=True)
    improvements = Column(JSON, nullable=True)
    improved_answer = Column(Text, nullable=True)
    overall_feedback = Column(Text, nullable=True)

    evaluation_status = Column(String(30), default="Completed")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    answer = relationship("Answer", back_populates="evaluation")
