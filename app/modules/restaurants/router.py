"""Routes HTTP du module restaurants."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import require_admin
from app.modules.restaurants import service
from app.modules.restaurants.schemas import (
    RestaurantAvailabilityUpdate,
    RestaurantResponse,
    RestaurantUpdate,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get(
    "",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    db: Session = Depends(get_db),
) -> list[RestaurantResponse]:
    """Retourne la liste des restaurants."""
    return service.get_restaurants(db)


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
) -> RestaurantResponse:
    """Retourne un restaurant."""

    restaurant = service.get_restaurant(db, restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="restaurant introuvable",
        )

    return restaurant


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    dependencies=[Depends(require_admin)],
)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
) -> RestaurantResponse:
    """Modifie un restaurant. Cette route est reservee aux administrateurs."""

    restaurant = service.get_restaurant(db, restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="restaurant introuvable",
        )

    return service.update_restaurant(
        db,
        restaurant,
        restaurant_data,
    )


@router.patch(
    "/{restaurant_id}/availability",
    response_model=RestaurantResponse,
    dependencies=[Depends(require_admin)],
)
def update_restaurant_availability(
    restaurant_id: int,
    availability_data: RestaurantAvailabilityUpdate,
    db: Session = Depends(get_db),
) -> RestaurantResponse:
    """Modifie la disponibilite d'un restaurant."""

    restaurant = service.get_restaurant(db, restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="restaurant introuvable",
        )

    return service.update_availability(
        db,
        restaurant,
        availability_data,
    )