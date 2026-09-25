"""Modele SQLAlchemy du module restaurants."""

from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Restaurant(Base):
    """Restaurant proposant des produits."""

    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    opening_hours: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    contact: Mapped[str | None] = mapped_column(String(20), nullable=True)
