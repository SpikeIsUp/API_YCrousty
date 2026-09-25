"""Routes HTTP du module orders."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.orders import service
from app.modules.orders.models import Order
from app.modules.orders.schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatus,
    OrderStatusUpdate,
)

router = APIRouter(prefix="/orders", tags=["orders"])
restaurant_orders_router = APIRouter(prefix="/restaurants", tags=["orders"])


def _to_response(order: Order) -> OrderResponse:
    """Transforme le stockage plat du client en schema public imbrique."""
    return OrderResponse(
        order_number=order.order_number,
        restaurant_id=order.restaurant_id,
        created_at=order.created_at,
        items=order.items,
        total_price=order.total_price,
        status=order.status,
        pickup_mode=order.pickup_mode,
        customer={"name": order.customer_name, "email": order.customer_email},
    )


def _can_access_order(order: Order, user: dict) -> bool:
    """Verifie l'acces d'un utilisateur a une commande."""
    return user.get("role") in {"admin", "direction"} or (
        user.get("role") == "staff"
        and user.get("restaurant_id") is not None
        and int(user["restaurant_id"]) == order.restaurant_id
    )


def _list_orders(
    restaurant_id: int | None,
    status_filter: OrderStatus | None,
    user: dict,
    db: Session,
) -> list[OrderResponse]:
    """Liste les commandes selon le role et le restaurant demande."""
    if user.get("role") not in {"admin", "direction", "staff"}:
        raise HTTPException(status_code=403, detail="role non autorise")
    if user.get("role") == "staff":
        user_restaurant_id = user.get("restaurant_id")
        if user_restaurant_id is None or (
            restaurant_id is not None
            and int(user_restaurant_id) != restaurant_id
        ):
            raise HTTPException(
                status_code=403,
                detail="acces aux commandes de ce restaurant interdit",
            )
        restaurant_id = int(user_restaurant_id)

    query = select(Order)
    if restaurant_id is not None:
        query = query.where(Order.restaurant_id == restaurant_id)
    if status_filter is not None:
        query = query.where(Order.status == status_filter)
    orders = db.scalars(query.order_by(Order.created_at.desc())).unique().all()
    return [_to_response(order) for order in orders]


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderResponse:
    """Cree une commande publique."""
    try:
        return _to_response(service.create_order(db, data))
    except service.OrderError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/{order_number}", response_model=OrderResponse)
def read_order(
    order_number: str,
    db: Session = Depends(get_db),
) -> OrderResponse:
    """Retourne une commande publique pour son suivi."""
    order = service.get_order(db, order_number)
    if order is None:
        raise HTTPException(status_code=404, detail="commande introuvable")
    return _to_response(order)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    status_filter: OrderStatus | None = Query(default=None, alias="status"),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[OrderResponse]:
    """Liste les commandes accessibles a l'utilisateur authentifie."""
    return _list_orders(None, status_filter, user, db)


@restaurant_orders_router.get(
    "/{restaurant_id}/orders",
    response_model=list[OrderResponse],
)
def list_restaurant_orders(
    restaurant_id: int,
    status_filter: OrderStatus | None = Query(default=None, alias="status"),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[OrderResponse]:
    """Liste les commandes d'un restaurant pour un utilisateur autorise."""
    return _list_orders(restaurant_id, status_filter, user, db)


@router.patch("/{order_number}/status", response_model=OrderResponse)
def change_status(
    order_number: str,
    data: OrderStatusUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OrderResponse:
    """Modifie le statut d'une commande avec controle d'acces."""
    order = service.get_order(db, order_number)
    if order is None:
        raise HTTPException(status_code=404, detail="commande introuvable")
    if not _can_access_order(order, user):
        raise HTTPException(status_code=403, detail="acces a cette commande interdit")
    return _to_response(service.update_status(db, order, data.status))


@router.post("/{order_number}/cancel", response_model=OrderResponse)
def cancel_order(
    order_number: str,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OrderResponse:
    """Annule une commande avec controle d'acces."""
    order = service.get_order(db, order_number)
    if order is None:
        raise HTTPException(status_code=404, detail="commande introuvable")
    if not _can_access_order(order, user):
        raise HTTPException(status_code=403, detail="acces a cette commande interdit")
    return _to_response(service.update_status(db, order, "cancelled"))
