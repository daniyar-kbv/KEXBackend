from django.conf import settings

from apps.pipeline.instagram.integrations import InstagramCode
from apps.pipeline.services import BaseService
from constance import config


class GetAccessTokenByCode(BaseService):  # noqa
    instance: 'InstagramCode' = None
    redirect_uri: str = None
    host = "https://api.instagram.com"
    endpoint = "/oauth/access_token"

    def get_instagram_code(self):
        return self.instance.code

    def run_service(self):

        data = {
            'client_id': settings.INSTAGRAM_CLIENT_ID,
            'client_secret': settings.INSTAGRAM_CLIENT_SECRET,
            'code': self.get_instagram_code(),
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }

        return self.fetch(json=data)

    def finalize_response(self, response):
        return response.get("access_token")


class GetUsername(BaseService):  # noqa
    access_token: str = None
    redirect_uri: str = None
    host = "https://graph.instagram.com"
    endpoint = "/me"

    def get_instagram_code(self):
        return self.instance

    def run_service(self):
        params = {
            "fields": "id,username",
            "access_token": self.access_token
        }

        return self.fetch(params=params)

    def finalize_response(self, response):
        return response.get("access_token")
