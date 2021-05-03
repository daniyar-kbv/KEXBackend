from typing import TYPE_CHECKING

from constance import config

from apps.pipeline.services import BaseService

from ..celery_tasks.auth import fetch_auth_token

if TYPE_CHECKING:
    from apps.partners.models import IIKOBrand


class BaseIIKOService(BaseService):  # noqa
    auth_token: str = None
    instance: 'IIKOBrand' = None
    host = config.IIKO_SERVICE_HOST

    def get_iiko_brand_pk(self):  # noqa
        return self.instance.pk

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.auth_token}"
        }

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.auth_token = fetch_auth_token(self.get_iiko_brand_pk())
