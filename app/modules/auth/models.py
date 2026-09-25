"""Modele SQLAlchemy du module auth."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """Compte utilisateur."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")
    restaurant_id: Mapped[int | None] = mapped_column(
        ForeignKey("restaurants.id"), nullable=True, default=None
    )