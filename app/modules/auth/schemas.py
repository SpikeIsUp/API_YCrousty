"""Schemas d'entree et de sortie du module auth."""

import re

from pydantic import BaseModel, field_validator

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]{8,12}$")


class LoginRequest(BaseModel):
    """Corps attendu par POST /auth/login."""

    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_format(cls, v: str) -> str:
        """Verifie que l'identifiant est alphanumerique (8 a 12 caracteres)."""
        if not USERNAME_PATTERN.match(v):
            raise ValueError(
                "l'identifiant doit etre alphanumerique (8 a 12 caracteres)"
            )
        return v

    @field_validator("password")
    @classmethod
    def password_format(cls, v: str) -> str:
        """Verifie la robustesse du mot de passe."""
        if not (12 <= len(v) <= 64):
            raise ValueError("le mot de passe doit contenir entre 12 et 64 caracteres")
        if not re.search(r"\d", v):
            raise ValueError("le mot de passe doit contenir au moins un chiffre")
        if not re.search(r"[A-Z]", v):
            raise ValueError("le mot de passe doit contenir au moins une majuscule")
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("le mot de passe doit contenir au moins un caractere special")
        return v


class TokenResponse(BaseModel):
    """Reponse renvoyee par POST /auth/login."""

    access_token: str
    token_type: str = "bearer"
    