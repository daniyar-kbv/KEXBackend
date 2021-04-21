from apps.pipeline.services import BaseService


class BaseIIKOService(BaseService):  # noqa
    host = "https://api-ru.iiko.services"
    host_verify = False


class GetAuthToken(BaseIIKOService):
    """Получение токена брэнда"""
    endpoint = "/api/1/access_token"

    def run_service(self):
        data = {
            "apiLogin": self.instance.api_login
        }

        return self.fetch(json=data)

    def save(self, prepared_data):
        print("prepared_data is", prepared_data)
