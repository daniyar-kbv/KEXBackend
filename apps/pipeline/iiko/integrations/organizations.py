from typing import Any

from .base import BaseIIKOService

from .serializers import UpdateBrandSerializer


class GetOrganizations(BaseIIKOService):
    """Получение списка организации"""
    endpoint = "api/1/organizations"
    save_serializer = UpdateBrandSerializer

    def run_service(self) -> Any:
        return self.fetch(json={})

    def finalize_response(self, response):
        return None
