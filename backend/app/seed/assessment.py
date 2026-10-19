from sqlalchemy import select

from app.extensions import db
from app.models import AssessmentCategory, AssessmentQuestion, QuestionOption
from app.seed.data.assessment import AGREEMENT_OPTIONS, CATEGORIES, QUESTIONS


def seed_assessment() -> dict[str, int]:
    """Insert any missing categories/questions/options by natural key.

    Natural keys: category `key`; question (category_id, question_order).
    Existing rows are never modified, so admin edits survive re-runs.
    """
    categories_inserted = 0
    questions_inserted = 0
    options_inserted = 0

    for spec in CATEGORIES:
        exists = (
            db.session.scalar(
                select(AssessmentCategory).where(AssessmentCategory.key == spec["key"])
            )
            is not None
        )
        if not exists:
            db.session.add(AssessmentCategory(**spec))  # type: ignore[arg-type]
            categories_inserted += 1
    db.session.flush()

    for position, (category_key, question_text) in enumerate(QUESTIONS, start=1):
        category = db.session.scalar(
            select(AssessmentCategory).where(AssessmentCategory.key == category_key)
        )
        if category is None:
            raise RuntimeError(
                f"Assessment category '{category_key}' missing; cannot seed question."
            )
        exists = (
            db.session.scalar(
                select(AssessmentQuestion).where(
                    AssessmentQuestion.category_id == category.id,
                    AssessmentQuestion.question_order == position,
                )
            )
            is not None
        )
        if exists:
            continue
        question = AssessmentQuestion(
            category_id=category.id,
            text=question_text,
            question_order=position,
        )
        db.session.add(question)
        db.session.flush()
        for option_order, (option_text, score) in enumerate(AGREEMENT_OPTIONS, start=1):
            db.session.add(
                QuestionOption(
                    question_id=question.id,
                    text=option_text,
                    score_value=score,
                    option_order=option_order,
                )
            )
            options_inserted += 1
        questions_inserted += 1

    db.session.commit()
    return {
        "categories_inserted": categories_inserted,
        "questions_inserted": questions_inserted,
        "options_inserted": options_inserted,
    }
