import pytest
from sqlalchemy import func, select

from app.extensions import db
from app.models import AssessmentCategory, AssessmentQuestion, QuestionOption, Skill, User
from app.seed.admin import seed_admin
from app.seed.assessment import seed_assessment
from app.seed.data.skills import SKILLS
from app.seed.skills import seed_skills

EXPECTED_SKILL_CATEGORIES = {
    "programming_language",
    "framework",
    "data",
    "database",
    "cloud_devops",
    "security",
    "networking",
    "design",
    "testing",
    "tools",
}

EXPECTED_CATEGORY_KEYS = [
    "software_dev",
    "ai_ml",
    "data_analysis",
    "cloud",
    "security",
    "networking",
    "database",
    "uiux",
    "qa",
]

AGREEMENT_TEXTS = ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]


def test_seed_skills_idempotent(app, clean_tables):
    with app.app_context():
        first = seed_skills()
        second = seed_skills()
        total = db.session.scalar(select(func.count()).select_from(Skill))

    assert first == {"inserted": len(SKILLS), "skipped": 0}
    assert second == {"inserted": 0, "skipped": len(SKILLS)}
    assert total == len(SKILLS)


def test_skills_catalogue_integrity(app, clean_tables):
    with app.app_context():
        seed_skills()
        skills = db.session.scalars(select(Skill)).all()

    assert len(skills) == len(SKILLS)
    assert len({skill.name for skill in skills}) == len(skills)
    for skill in skills:
        assert skill.is_active is True
        assert skill.category in EXPECTED_SKILL_CATEGORIES
        assert skill.created_at is not None


def test_seed_assessment_idempotent(app, clean_tables):
    with app.app_context():
        first = seed_assessment()
        second = seed_assessment()
        categories = db.session.scalar(select(func.count()).select_from(AssessmentCategory))
        questions = db.session.scalar(select(func.count()).select_from(AssessmentQuestion))
        options = db.session.scalar(select(func.count()).select_from(QuestionOption))

    assert first == {
        "categories_inserted": 9,
        "questions_inserted": 27,
        "options_inserted": 108,
    }
    assert second == {
        "categories_inserted": 0,
        "questions_inserted": 0,
        "options_inserted": 0,
    }
    assert (categories, questions, options) == (9, 27, 108)


def test_assessment_structure(app, clean_tables):
    with app.app_context():
        seed_assessment()
        categories = db.session.scalars(
            select(AssessmentCategory).order_by(AssessmentCategory.display_order)
        ).all()
        questions = db.session.scalars(
            select(AssessmentQuestion).order_by(AssessmentQuestion.question_order)
        ).all()

        assert [category.key for category in categories] == EXPECTED_CATEGORY_KEYS

        assert [question.question_order for question in questions] == list(range(1, 28))
        assert all(question.is_active for question in questions)
        # Interleaved presentation: no two consecutive questions share a category.
        assert all(
            questions[i].category_id != questions[i + 1].category_id
            for i in range(len(questions) - 1)
        )

        for category in categories:
            active = [q for q in category.questions if q.is_active]
            assert len(active) == 3

        for question in questions:
            options = sorted(question.options, key=lambda option: option.option_order)
            assert [option.option_order for option in options] == [1, 2, 3, 4]
            assert [option.text for option in options] == AGREEMENT_TEXTS
            assert sorted(option.score_value for option in options) == [0, 1, 2, 3]


def test_seed_admin_creates_bootstrap_admin(app, clean_tables, monkeypatch):
    monkeypatch.setenv("ADMIN_EMAIL", "Root@CNA.Local")
    monkeypatch.setenv("ADMIN_PASSWORD", "correct-horse-battery")

    with app.app_context():
        result = seed_admin()
        user = db.session.scalar(select(User).where(User.email == "root@cna.local"))

    assert result == {"created": True, "email": "root@cna.local"}
    assert user is not None
    assert user.role == "admin"
    assert user.is_active is True
    assert user.check_password("correct-horse-battery") is True
    assert user.check_password("wrong-password") is False


def test_seed_admin_refreshes_existing_account(app, clean_tables, monkeypatch):
    with app.app_context():
        existing = User(email="admin@example.com", full_name="Existing Admin", role="student")
        existing.set_password("old-password-123")
        db.session.add(existing)
        db.session.commit()

    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "new-password-456")

    with app.app_context():
        result = seed_admin()
        user = db.session.scalar(select(User).where(User.email == "admin@example.com"))

    assert result == {"created": False, "email": "admin@example.com"}
    assert user.role == "admin"
    assert user.check_password("new-password-456") is True


def test_seed_admin_requires_env_credentials(app, clean_tables, monkeypatch):
    monkeypatch.delenv("ADMIN_EMAIL", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    with app.app_context(), pytest.raises(RuntimeError, match="ADMIN_EMAIL and ADMIN_PASSWORD"):
        seed_admin()


def test_seed_admin_rejects_short_password(app, clean_tables, monkeypatch):
    monkeypatch.setenv("ADMIN_EMAIL", "short@cna.local")
    monkeypatch.setenv("ADMIN_PASSWORD", "short")

    with app.app_context(), pytest.raises(RuntimeError, match="at least 10 characters"):
        seed_admin()


def test_seed_cli_runs_all_and_is_idempotent(app, clean_tables, monkeypatch):
    monkeypatch.setenv("ADMIN_EMAIL", "cli-admin@cna.local")
    monkeypatch.setenv("ADMIN_PASSWORD", "cli-password-12345")

    runner = app.test_cli_runner()
    first = runner.invoke(args=["seed"])
    second = runner.invoke(args=["seed"])

    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output
    assert f"skills: inserted {len(SKILLS)}, already present 0" in first.output
    assert f"skills: inserted 0, already present {len(SKILLS)}" in second.output

    with app.app_context():
        skills = db.session.scalar(select(func.count()).select_from(Skill))
        questions = db.session.scalar(select(func.count()).select_from(AssessmentQuestion))
        admins = db.session.scalar(
            select(func.count()).select_from(User).where(User.role == "admin")
        )

    assert (skills, questions, admins) == (len(SKILLS), 27, 1)
