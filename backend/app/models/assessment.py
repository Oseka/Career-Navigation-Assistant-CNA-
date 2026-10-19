from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class AssessmentCategory(db.Model):
    __tablename__ = "assessment_categories"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    key: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=sa_text("0"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sa_text("1"))

    questions: Mapped[list["AssessmentQuestion"]] = relationship(
        back_populates="category", order_by="AssessmentQuestion.question_order"
    )


class AssessmentQuestion(db.Model):
    __tablename__ = "assessment_questions"
    __table_args__ = (
        Index(
            "ix_assessment_questions_category_order",
            "category_id",
            "question_order",
        ),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("assessment_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sa_text("1"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=sa_text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=sa_text("CURRENT_TIMESTAMP"), onupdate=func.now()
    )

    category: Mapped[AssessmentCategory] = relationship(back_populates="questions")
    options: Mapped[list["QuestionOption"]] = relationship(
        back_populates="question",
        order_by="QuestionOption.option_order",
        cascade="all, delete-orphan",
    )


class QuestionOption(db.Model):
    __tablename__ = "question_options"
    __table_args__ = (
        UniqueConstraint("question_id", "option_order", name="uq_question_options_order"),
        CheckConstraint(
            "score_value BETWEEN 0 AND 3", name="ck_question_options_score_value"
        ),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    question_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("assessment_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    score_value: Mapped[int] = mapped_column(TINYINT, nullable=False)
    option_order: Mapped[int] = mapped_column(TINYINT, nullable=False)

    question: Mapped[AssessmentQuestion] = relationship(back_populates="options")
