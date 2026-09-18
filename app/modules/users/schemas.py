"""Schemas d'entree et de sortie du module users."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.modules.auth.schemas import LoginRequest

UserRole = Literal["admin", "staff", "direction"]


class UserCreate(LoginRequest):
    """Corps attendu par POST /users."""

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: UserRole
    restaurant_id: int = Field(gt=0)


class UserResponse(BaseModel):
    """Representation publique d'un utilisateur."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    role: UserRole
    restaurant_id: int
