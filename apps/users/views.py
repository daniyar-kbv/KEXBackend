from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet


from .models import User
from .serializers import (
    UserViewSerializer,
    UserCreateUpdateSerializer,
)


class UserViewSet(FilterByPartnerMixin, ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["is_active"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserCreateUpdateSerializer

        return UserViewSerializer


from .serializers import TestSerializer
class Test(ListAPIView):
    queryset = User.objects.all()
    serializer_class = TestSerializer
