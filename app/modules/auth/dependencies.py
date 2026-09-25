"""Dependances d'authentification partagees par les routes protegees."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError

from app.modules.auth.security import decode_access_token

bearer_scheme = HTTPBearer()


def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Verifie qu'un JWT valide appartient a un administrateur."""
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Verifie qu'un JWT valide est fourni et retourne son contenu."""
    try:
        payload = decode_access_token(credentials.credentials)
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalide ou expire",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return payload


def require_admin(
    payload: dict = Depends(get_current_user),
) -> dict:
    """Verifie qu'un JWT valide appartient a un administrateur."""

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="droits administrateur requis",
        )
        return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Decode le JWT et retourne son contenu (sub, role, restaurant_id)."""
    try:
        payload = decode_access_token(credentials.credentials)
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalide ou expire",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return payload


def require_staff_or_admin(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Autorise uniquement les roles admin et staff."""
    if current_user.get("role") not in ("admin", "staff"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="reserve aux membres du staff ou aux administrateurs",
        )
    return current_user


def check_restaurant_access(current_user: dict, restaurant_id: int) -> None:
    """Verifie qu'un staff agit uniquement sur son propre restaurant."""
    if current_user.get("role") == "admin":
        return
    if current_user.get("role") == "staff" and current_user.get("restaurant_id") == restaurant_id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="vous n'avez pas le droit d'agir sur ce restaurant",
    )
