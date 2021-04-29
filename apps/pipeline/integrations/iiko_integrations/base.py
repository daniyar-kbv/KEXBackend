from constance import config

from apps.pipeline.services import BaseService
from apps.pipeline.celery_tasks.auth import fetch_auth_token


class BaseIIKOService(BaseService):  # noqa
    host = config.IIKO_SERVICE_HOST
    auth_token: str = None

    def get_brand_api_pk(self):
        return self.instance.pk

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.auth_token = fetch_auth_token(self.get_brand_api_pk())
