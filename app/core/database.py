"""Connexion a PostgreSQL avec SQLAlchemy."""

from collections.abc import Generator

from sqlalchemy import create_engine
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
