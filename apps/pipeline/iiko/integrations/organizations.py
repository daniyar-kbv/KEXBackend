from typing import Any

from .base import BaseIIKOService


class GetOrganizations(BaseIIKOService):
    """Получение списка организации"""
    endpoint = "api/1/organizations"
    save_serializer = None

    def run_service(self) -> Any:
        return self.fetch(json={})
