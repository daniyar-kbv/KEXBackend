from rest_framework.permissions import AllowAny

from .pagination import CustomPagination
from .renderers import JSONRenderer


class JSONRendererMixin:
    renderer_classes = [JSONRenderer]
    pagination_class = CustomPagination


class PublicAPIMixin:
    permission_classes = [AllowAny]


class PublicJSONRendererMixin(JSONRendererMixin, PublicAPIMixin):
    ...
