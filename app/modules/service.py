"""Regles metier du module health."""

from app.modules.health.schemas import HealthResponse


def get_status() -> HealthResponse:
    """Retourne l'etat de l'API."""
    return HealthResponse(status="ok")
