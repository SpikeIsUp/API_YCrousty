"""Point d'entree de l'API Ytasty Crousty."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import (
    Base,
    SessionLocal,
    engine,
    ensure_restaurant_schema,
    ensure_user_schema,
)
from app.modules.auth.router import router as auth_router
from app.modules.auth.service import seed_admin
from app.modules.health.router import router as health_router
from app.modules.orders.router import restaurant_orders_router
from app.modules.orders.router import router as orders_router
from app.modules.products.router import router as products_router
from app.modules.restaurants.router import router as restaurants_router
from app.modules.restaurants.service import seed_restaurants
from app.modules.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cree les tables et le compte admin au demarrage."""
    Base.metadata.create_all(bind=engine)
    ensure_restaurant_schema()
    ensure_user_schema()
    db = SessionLocal()
    try:
        seed_admin(db)
        seed_restaurants(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Ytasty Crousty API", version="0.1.0", lifespan=lifespan)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(restaurants_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(restaurant_orders_router)
