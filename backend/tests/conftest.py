import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import pytest
from dotenv import dotenv_values
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent


def _test_database_url() -> str:
    url = os.environ.get("DATABASE_URL") or dotenv_values(BASE_DIR / ".env").get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Copy backend/.env.example to backend/.env and "
            "point it at your MySQL server (tests always run against the cna_test schema)."
        )
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, "/cna_test", parts.query, parts.fragment))


os.environ["FLASK_ENV"] = "testing"
os.environ["DATABASE_URL"] = _test_database_url()


from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        from flask_migrate import upgrade

        upgrade()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def clean_tables(app):
    """Empty the tables created so far so seed tests start from a known state."""
    with app.app_context():
        tables = (
            "question_options",
            "assessment_questions",
            "assessment_categories",
            "skills",
            "users",
        )
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        for table in tables:
            db.session.execute(text(f"DELETE FROM {table}"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()
    yield
