"""Modele SQLAlchemy des produits."""

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    """Produit disponible dans un restaurant."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    available: Mapped[bool] = mapped_column(Boolean, default=True)
