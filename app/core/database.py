"""Connexion a PostgreSQL avec SQLAlchemy."""

from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Classe de base de tous les modeles."""


def get_db() -> Generator[Session, None, None]:
    """Ouvre une session, la fournit a la route, puis la ferme."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_user_schema() -> None:
    """Ajoute les colonnes utilisateurs manquantes dans une base existante."""
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        return

    existing = {column["name"] for column in inspector.get_columns("users")}
    missing = {
        "first_name": "VARCHAR(100)",
        "last_name": "VARCHAR(100)",
    }

    with engine.begin() as connection:
        for name, definition in missing.items():
            if name not in existing:
                connection.execute(
                    text(f"ALTER TABLE users ADD COLUMN {name} {definition}")
                )


def ensure_restaurant_schema() -> None:
    """Ajoute les colonnes restaurants manquantes dans une base existante."""
    inspector = inspect(engine)
    if not inspector.has_table("restaurants"):
        return

    existing = {
        column["name"] for column in inspector.get_columns("restaurants")
    }
    missing = {
        "city": "VARCHAR(100)",
        "address": "VARCHAR(255)",
        "is_open": "BOOLEAN DEFAULT TRUE",
        "opening_hours": "JSON",
        "contact": "VARCHAR(20)",
    }

    with engine.begin() as connection:
        for name, definition in missing.items():
            if name not in existing:
                connection.execute(
                    text(f"ALTER TABLE restaurants ADD COLUMN {name} {definition}")
                )
