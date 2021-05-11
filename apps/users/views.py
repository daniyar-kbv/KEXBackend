# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.common.mixins import JSONRendererMixin

from .models import User
from .serializers import (
    UserViewSerializer,
    UserCreateUpdateSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # filter_backends = [DjangoFilterBackend]
    filter_fields = ["is_active"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserCreateUpdateSerializer

        return UserViewSerializer
