"""Utilitaires de securite : hash de mot de passe et JWT."""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash un mot de passe en clair avec bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifie qu'un mot de passe correspond a son hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(
    subject: str,
    role: str,
    restaurant_id: int | None = None,
) -> str:
    """Cree un JWT signe contenant l'identifiant et le role."""
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "role": role, "restaurant_id": restaurant_id, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    """Decode et verifie un JWT. Leve une exception si invalide/expire."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])