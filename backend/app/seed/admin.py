import os

from sqlalchemy import select

from app.extensions import db
from app.models import User


def seed_admin() -> dict[str, bool | str]:
    """Create the bootstrap admin, or refresh the existing account.

    The environment is the source of truth: re-running resets the admin's
    password to ADMIN_PASSWORD and forces the admin role.
    """
    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not email or not password:
        raise RuntimeError(
            "ADMIN_EMAIL and ADMIN_PASSWORD must be set (see backend/.env.example)."
        )
    if len(password) < 10:
        raise RuntimeError("ADMIN_PASSWORD must be at least 10 characters long.")

    user = db.session.scalar(select(User).where(User.email == email))
    created = user is None
    if created:
        user = User(email=email, full_name="CNA Administrator")
    user.role = "admin"
    user.set_password(password)
    if created:
        db.session.add(user)
    db.session.commit()
    return {"created": created, "email": email}
