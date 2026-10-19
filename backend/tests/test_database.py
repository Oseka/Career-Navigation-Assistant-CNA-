from sqlalchemy import text

from app.extensions import db


def test_tests_run_against_cna_test_schema(app):
    with app.app_context():
        schema_name = db.session.execute(text("SELECT DATABASE()")).scalar()

    assert schema_name == "cna_test"


def test_database_roundtrip(app):
    with app.app_context():
        assert db.session.execute(text("SELECT 1")).scalar() == 1


def test_session_time_zone_is_utc(app):
    with app.app_context():
        now, utc = db.session.execute(text("SELECT NOW(), UTC_TIMESTAMP()")).one()
    assert now == utc
