from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)

from apps.common.mixins import JSONRendererMixin

from .serializers import TokenObtainPairSerializer


class TokenObtainPairView(
    JSONRendererMixin, BaseTokenObtainPairView
):
    serializer_class = TokenObtainPairSerializer
