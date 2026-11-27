
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        nullable=False
    )

    question_text = Column(Text, nullable=False)
    category = Column(String(30), nullable=False)
    order_index = Column(Integer, nullable=False)

    interview = relationship("Interview", back_populates="questions")

    answer = relationship(
        "Answer",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan"
    )
