"""Messages et exceptions communs a toute l'application."""

NOT_FOUND_MESSAGE = "{resource} avec l'id {resource_id} est introuvable"


class AppError(Exception):
    """Erreur de base de l'application : toutes nos erreurs en heritent."""


class NotFoundError(AppError):
    """Ressource demandee inexistante."""

    def __init__(self, resource: str, resource_id: int) -> None:
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(
            NOT_FOUND_MESSAGE.format(resource=resource, resource_id=resource_id)
        )
