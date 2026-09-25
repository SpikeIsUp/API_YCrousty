"""Routes HTTP du module products."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import check_restaurant_access, require_staff_or_admin
from app.modules.auth.models import User
from app.modules.products import service
from app.modules.products.schemas import (
    AvailabilityUpdate,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def list_products(
    category: str | None = None,
    q: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
    db: Session = Depends(get_db),
) -> list[ProductResponse]:
    """Liste les produits, avec filtres combinables."""
    return service.list_products(db, category, q, restaurant_id, is_available)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponse:
    """Recupere un produit par son id."""
    product = service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="produit introuvable")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin),
) -> ProductResponse:
    """Cree un produit. Admin : tous restaurants. Staff : son propre restaurant uniquement."""
    check_restaurant_access(current_user, data.restaurant_id)
    return service.create_product(db, data)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin),
) -> ProductResponse:
    """Met a jour un produit existant."""
    product = service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="produit introuvable")
    check_restaurant_access(current_user, product.restaurant_id)
    return service.update_product(db, product, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin),
) -> None:
    """Supprime un produit."""
    product = service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="produit introuvable")
    check_restaurant_access(current_user, product.restaurant_id)
    service.delete_product(db, product)


@router.patch("/{product_id}/availability", response_model=ProductResponse)
def update_availability(
    product_id: int,
    data: AvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin),
) -> ProductResponse:
    """Change la disponibilite d'un produit."""
    product = service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="produit introuvable")
    check_restaurant_access(current_user, product.restaurant_id)
    return service.set_availability(db, product, data.is_available)