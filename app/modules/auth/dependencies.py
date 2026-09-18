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
    try:
        payload = decode_access_token(credentials.credentials)
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalide ou expire",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="droits administrateur requis",
        )
    return payload
