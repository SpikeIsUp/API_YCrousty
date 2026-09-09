"""Configuration lue dans les variables d'environnement."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Parametres de l'application."""

    database_url: str = "postgresql+psycopg://ytasty:ytasty@db:5432/ytasty"


settings = Settings()
