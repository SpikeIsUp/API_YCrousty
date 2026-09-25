"""Schemas d'entree et de sortie du module restaurants."""

from pydantic import BaseModel, ConfigDict, Field


class RestaurantResponse(BaseModel):
    """Representation publique d'un restaurant."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    address: str
    is_open: bool
    opening_hours: dict[str, str]
    contact: str


class RestaurantUpdate(BaseModel):
    """Corps attendu par PATCH /restaurants/{restaurant_id}."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    address: str | None = Field(default=None, min_length=1, max_length=255)
    opening_hours: dict[str, str] | None = None
    contact: str | None = Field(default=None, min_length=1, max_length=20)


class RestaurantAvailabilityUpdate(BaseModel):
    """Corps attendu pour modifier la disponibilite d'un restaurant."""

    is_open: bool