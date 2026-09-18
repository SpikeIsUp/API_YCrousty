"""Regles metier du module users."""

from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.auth.security import hash_password
from app.modules.users.schemas import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User | None:
    """Cree un utilisateur, ou retourne None si le username existe deja."""
    if db.query(User).filter(User.username == user_data.username).first() is not None:
        return None

    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        restaurant_id=user_data.restaurant_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
