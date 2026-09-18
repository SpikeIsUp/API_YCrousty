"""Schemas d'entree et de sortie du module health."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Reponse renvoyee par GET /health."""

    status: str
