"""Regles metier du module products."""

from sqlalchemy.orm import Session

from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate, ProductUpdate


def list_products(
    db: Session,
    category: str | None = None,
    q: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
) -> list[Product]:
    """Liste les produits, filtres combinables."""
    query = db.query(Product)

    if category is not None:
        query = query.filter(Product.category == category)
    if q is not None:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    if restaurant_id is not None:
        query = query.filter(Product.restaurant_id == restaurant_id)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)

    return query.all()


def get_product(db: Session, product_id: int) -> Product | None:
    """Recupere un produit par son id."""
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, data: ProductCreate) -> Product:
    """Cree un nouveau produit."""
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    """Met a jour partiellement un produit existant."""
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    """Supprime un produit."""
    db.delete(product)
    db.commit()


def set_availability(db: Session, product: Product, is_available: bool) -> Product:
    """Change la disponibilite d'un produit."""
    product.is_available = is_available
    db.commit()
    db.refresh(product)
    return product