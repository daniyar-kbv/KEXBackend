from .base import BaseIIKOService


class GetOrganizations(BaseIIKOService):
    """Получение списка организации"""
    endpoint = "api/1/organizations"
    save_serializer = None
