from sqlalchemy import select

from app.extensions import db
from app.models import Skill
from app.seed.data.skills import SKILLS


def seed_skills() -> dict[str, int]:
    """Insert any missing skills; existing rows are left untouched."""
    inserted = 0
    skipped = 0
    for name, category in SKILLS:
        exists = db.session.scalar(select(Skill).where(Skill.name == name)) is not None
        if exists:
            skipped += 1
        else:
            db.session.add(Skill(name=name, category=category))
            inserted += 1
    db.session.commit()
    return {"inserted": inserted, "skipped": skipped}
