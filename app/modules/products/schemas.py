"""Schemas d'entree et de sortie du module products."""

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    """Corps attendu par POST /products."""

    name: str
    image: str
    description: str
    category: str
    price: float
    is_available: bool = True
    restaurant_id: int
    ingredients: list[str] = []


class ProductUpdate(BaseModel):
    """Corps attendu par PATCH /products/{id}. Tous les champs sont optionnels."""

    name: str | None = None
    image: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    is_available: bool | None = None
    ingredients: list[str] | None = None


class AvailabilityUpdate(BaseModel):
    """Corps attendu par PATCH /products/{id}/availability."""

    is_available: bool


class ProductResponse(BaseModel):
    """Reponse renvoyee pour un produit."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image: str
    description: str
    category: str
    price: float
    is_available: bool
    restaurant_id: int
    ingredients: list[str]