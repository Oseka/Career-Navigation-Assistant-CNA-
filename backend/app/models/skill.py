from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sa_text("1"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=sa_text("CURRENT_TIMESTAMP")
    )
