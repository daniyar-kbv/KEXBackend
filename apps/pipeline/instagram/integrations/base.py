from django.conf import settings

from apps.pipeline.instagram.integrations import InstagramCode, InstagramAccessToken
from apps.pipeline.services import BaseService
from constance import config


class GetAccessTokenByCode(BaseService):  # noqa
    instance: 'InstagramCode' = None
    host = "https://api.instagram.com"
    endpoint = "/oauth/access_token"

    def get_instagram_code(self):
        return self.instance.code

    def get_redirect_uri(self):
        return self.kwargs.get('redirect_uri')

    def run_service(self):

        data = {
            'client_id': settings.INSTAGRAM_CLIENT_ID,
            'client_secret': settings.INSTAGRAM_CLIENT_SECRET,
            'code': self.get_instagram_code(),
            'grant_type': 'authorization_code',
            'redirect_uri': self.get_redirect_uri(),
        }

        return self.fetch(data=data)

    def finalize_response(self, response):
        return response.get("access_token")


class GetUsername(BaseService):  # noqa
    instance: 'InstagramAccessToken' = None
    host = "https://graph.instagram.com/me"
    endpoint = ""
    method = "GET"

    def get_access_token(self):
        return self.instance.access_token

    def run_service(self):
        params = {
            "fields": "id,username",
            "access_token": self.get_access_token()
        }

        return self.fetch(params=params)

    def finalize_response(self, response):
        print(response)
        return response.get("username")
