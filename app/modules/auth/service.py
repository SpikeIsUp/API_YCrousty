"""Regles metier du module auth."""

from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def authenticate_user(db: Session, credentials: LoginRequest) -> TokenResponse | None:
    """Verifie les identifiants et retourne un token si valides."""
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        return None
    token = create_access_token(
        subject=user.username, role=user.role, restaurant_id=user.restaurant_id
    )
    return TokenResponse(access_token=token)


def seed_admin(db: Session) -> None:
    """Cree le compte admin par defaut s'il n'existe pas deja."""
    exists = db.query(User).filter(User.username == settings.admin_username).first()
    if exists is None:
        admin = User(
            username=settings.admin_username,
            hashed_password=hash_password(settings.admin_password),
            role="admin",
        )
        db.add(admin)
        db.commit()