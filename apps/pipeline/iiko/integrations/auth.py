from typing import TYPE_CHECKING

from constance import config
from django.core.cache import cache

from apps.pipeline.services import BaseService

if TYPE_CHECKING:
    from apps.partners.models import IIKOBrand


class GetAuthToken(BaseService):
    """Получение токена брэнда"""
    instance: 'IIKOBrand' = None

    host = config.IIKO_SERVICE_HOST
    endpoint = "/api/1/access_token"

    def run_service(self):
        cached_token = cache.get(self.instance.cache_mask)

        if cached_token is not None:
            return {"token": cached_token}

        data = {
            "apiLogin": self.instance.api_login
        }

        return self.fetch(json=data)

    def prepare_to_save(self, data):
        return data.get("token")

    def finalize_response(self, response):
        return response.get("token")

    def save(self, prepared_data):
        token = self.prepare_to_save(prepared_data)
        cache.set(
            self.instance.cache_mask, token,
            timeout=config.IIKO_AUTH_TOKEN_LIFETIME,
        )
