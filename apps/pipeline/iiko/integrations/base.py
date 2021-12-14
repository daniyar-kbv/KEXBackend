from typing import TYPE_CHECKING

from constance import config
from requests.models import Response

from apps.pipeline.services import BaseService

from ..celery_tasks.auth import fetch_auth_token, remove_auth_token

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand


class BaseIIKOService(BaseService):  # noqa
    auth_token: str = None
    instance: 'LocalBrand' = None
    host = config.IIKO_SERVICE_HOST

    def get_local_brand_pk(self):  # noqa
        return self.instance.pk

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.auth_token}"
        }

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.auth_token = fetch_auth_token(self.get_local_brand_pk())

    def operate_401(self, response: Response, json, params, **kwargs):
        remove_auth_token(self.get_local_brand_pk())
        headers = {
            'Authorization': f"Bearer {fetch_auth_token(self.get_local_brand_pk())}"
        }

        return self.session.request(
            method=self.method,
            url=self.url,
            auth=self.auth,
            headers=headers,
            params=params,
            json=json,
            timeout=self.timeout,
            verify=self.host_verify,
            **kwargs
        )
