from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, GenericAPIView

from apps.common.mixins import JSONRendererMixin

from .models import UserAddress
from .serializers import (
    AccountInfoSerializer,
    UserAddressSerializer,
    UpdateUserAddressSerializer,
)


class AccountInfoView(JSONRendererMixin, RetrieveAPIView):
    serializer_class = AccountInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)


class AccountUpdateView(JSONRendererMixin, GenericAPIView):
    serializer_class = AccountInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data)


class UserAddressViewSet(JSONRendererMixin, ModelViewSet):
    queryset = UserAddress.objects.all()
    http_method_names = ["put", "get", "delete"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserAddressSerializer

        return UpdateUserAddressSerializer
