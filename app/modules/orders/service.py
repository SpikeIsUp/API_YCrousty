"""Regles metier du module orders."""

from decimal import Decimal
from secrets import token_hex

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.orders.models import Order, OrderItem
from app.modules.orders.schemas import OrderCreate
from app.modules.products.models import Product
from app.modules.restaurants.models import Restaurant


class OrderError(Exception):
    """Erreur metier lors de la creation ou de la modification d'une commande."""

    def __init__(self, detail: str, status_code: int) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


def create_order(db: Session, data: OrderCreate) -> Order:
    """Valide les donnees et cree une commande avec son total calcule en base."""
    restaurant = db.get(Restaurant, data.restaurant_id)
    if restaurant is None:
        raise OrderError("restaurant introuvable", 404)
    if not restaurant.is_open:
        raise OrderError("le restaurant est ferme", 400)

    products: list[tuple[Product, int]] = []
    total = Decimal("0.00")
    for requested_item in data.items:
        product = db.get(Product, requested_item.product_id)
        if product is None:
            raise OrderError("produit introuvable", 404)
        if product.restaurant_id != data.restaurant_id:
            raise OrderError("le produit appartient a un autre restaurant", 400)
        if not product.is_available:
            raise OrderError("le produit est indisponible", 400)
        products.append((product, requested_item.quantity))
        total += product.price * requested_item.quantity

    order = Order(
        order_number=f"CMD-{token_hex(6).upper()}",
        restaurant_id=data.restaurant_id,
        total_price=total,
        status="pending",
        pickup_mode=data.pickup_mode,
        customer_name=data.customer.name,
        customer_email=str(data.customer.email),
    )
    order.items = [
        OrderItem(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
        )
        for product, quantity in products
    ]
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_number: str) -> Order | None:
    """Retourne une commande par son numero."""
    return db.scalar(
        select(Order).where(Order.order_number == order_number)
    )


def update_status(db: Session, order: Order, status: str) -> Order:
    """Modifie le statut d'une commande."""
    order.status = status
    db.commit()
    db.refresh(order)
    return order
