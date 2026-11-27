
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        unique=True
    )

    answer_text = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    question = relationship("Question", back_populates="answer")

    evaluation = relationship(
        "Evaluation",
        back_populates="answer",
        uselist=False,
        cascade="all, delete-orphan"
    )
