"""Point d'entree de l'API Ytasty Crousty."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, SessionLocal, engine
from app.modules.auth.router import router as auth_router
from app.modules.auth.service import seed_admin
from app.modules.health.router import router as health_router
from app.modules.restaurants.models import Restaurant  
from app.modules.products.router import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cree les tables et le compte admin au demarrage."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_admin(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Ytasty Crousty API", version="0.1.0", lifespan=lifespan)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(products_router)