"""Configuration lue dans les variables d'environnement."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Parametres de l'application."""

    database_url: str = "postgresql+psycopg://ytasty:ytasty@db:5432/ytasty"

    secret_key: str = "change-me-in-dotenv"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    admin_username: str = "admin123"
    admin_password: str = "Admin@123456"


settings = Settings()
