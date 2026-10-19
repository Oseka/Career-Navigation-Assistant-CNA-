from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("student", "admin", name="user_role"),
        nullable=False,
        server_default="student",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sa_text("1"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=sa_text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=sa_text("CURRENT_TIMESTAMP"), onupdate=func.now()
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="scrypt")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
