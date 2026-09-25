"""Modele SQLAlchemy des restaurants."""

from sqlalchemy import Boolean, JSON, String
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Restaurant(Base):
    """Restaurant Ytasty Crousty."""
    """Restaurant pouvant recevoir des commandes."""

    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    city: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(255))
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    opening_hours: Mapped[dict] = mapped_column(JSON)
    contact: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(150))
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
