from __future__ import annotations
from ..models.portal import Portal


def get_portal(client) -> Portal:
    """Получить информацию о текущем ивенте на платформе."""
    response = client.get("/api/v1/portal")
    response.raise_for_status()
    return Portal.model_validate(response.json())
