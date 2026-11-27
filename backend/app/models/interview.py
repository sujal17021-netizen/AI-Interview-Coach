
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    role = Column(String(100), nullable=False)
    interview_type = Column(String(30), nullable=False)
    difficulty = Column(String(20), nullable=False)

    status = Column(String(30), default="Completed")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="interviews")
    questions = relationship(
        "Question",
        back_populates="interview",
        cascade="all, delete-orphan"
    )
