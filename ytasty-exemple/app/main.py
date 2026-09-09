"""Point d'entree de l'API Ytasty Crousty."""

from fastapi import FastAPI

from app.modules.health.router import router as health_router

app = FastAPI(title="Ytasty Crousty API", version="0.1.0")

app.include_router(health_router)
