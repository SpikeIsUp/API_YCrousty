"""Schemas d'entree et de sortie du module orders."""

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

OrderStatus = Literal[
    "pending",
    "validated",
    "preparing",
    "ready",
    "collected",
    "cancelled",
]
PickupMode = Literal["onsite", "takeaway"]


class OrderItemCreate(BaseModel):
    """Produit demande dans une commande."""

    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CustomerCreate(BaseModel):
    """Coordonnees du client."""

    name: str = Field(min_length=1, max_length=150)
    email: str = Field(min_length=3, max_length=320)


class OrderCreate(BaseModel):
    """Corps attendu par POST /orders."""

    restaurant_id: int = Field(gt=0)
    items: list[OrderItemCreate] = Field(min_length=1)
    pickup_mode: PickupMode
    customer: CustomerCreate


class OrderItemResponse(BaseModel):
    """Article renvoye dans une commande."""

    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
    unit_price: Decimal


class CustomerResponse(BaseModel):
    """Client renvoye dans une commande."""

    name: str
    email: str


class OrderResponse(BaseModel):
    """Representation publique d'une commande."""

    model_config = ConfigDict(from_attributes=True)

    order_number: str
    restaurant_id: int
    created_at: datetime
    items: list[OrderItemResponse]
    total_price: Decimal
    status: OrderStatus
    pickup_mode: PickupMode
    customer: CustomerResponse


class OrderStatusUpdate(BaseModel):
    """Corps attendu par PATCH /orders/{order_number}/status."""

    status: OrderStatus
