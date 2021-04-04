from typing import Dict, Tuple, Optional, TYPE_CHECKING

from rest_framework.renderers import JSONRenderer as DefaultJSONRenderer

from .dataclasses import CustomError, CustomResponse

if TYPE_CHECKING:
    from rest_framework.response import Response


class JSONRenderer(DefaultJSONRenderer):
    client_error_code = "CLIENT_ERROR"
    iiko_unavailable_code = "IIKO_ERROR"  # noqa

    def handle_200(self, data: Dict) -> Tuple[
        Optional[Dict], Optional[CustomError]
    ]:
        return data, None

    def handle_401(self, data):
        return None, CustomError(self.client_error_code, "user not found").__dict__

    def get_handler(self, status_code: str):
        if status_code.startswith("2"):
            return self.handle_200

        if hasattr(self, f"handle_{status_code}"):
            return getattr(self, f"handle_{status_code}")

    def distribute_by_status_code(self, data: Dict, raw_response: 'Response'):
        status_code = str(raw_response.status_code)

        handler_func = self.get_handler(status_code)

        if handler_func is None:
            return data

        data, error = handler_func(data)  # noqa

        return CustomResponse(data, error).__dict__

    def render(self, data, accepted_media_type=None, renderer_context=None):
        formatted_response = self.distribute_by_status_code(data, renderer_context['response'])

        return super(JSONRenderer, self).render(formatted_response, accepted_media_type, renderer_context)
