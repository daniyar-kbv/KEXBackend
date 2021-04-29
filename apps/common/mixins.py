from rest_framework.permissions import AllowAny

from .renderers import JSONRenderer


class JSONRendererMixin:
    renderer_classes = [JSONRenderer]


class PublicAPIMixin:
    permission_classes = [AllowAny]
