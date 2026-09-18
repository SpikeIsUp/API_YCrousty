"""Routes HTTP du module health."""

from fastapi import APIRouter

from app.modules.health import service
from app.modules.health.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() :
    """Verifie que l'API repond."""
    return service.get_status()
