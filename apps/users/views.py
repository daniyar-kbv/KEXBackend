from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
    UpdateAPIView,
)

from apps.common.mixins import JSONRendererMixin

from .models import UserAddress
from .serializers import (
    AccountInfoSerializer,
    AddUserAddressSerializer,
    ChangeCurrentAddressSerializer,
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


class AddUserAddressView(JSONRendererMixin, CreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = AddUserAddressSerializer


class ChangeCurrentAddressView(JSONRendererMixin, UpdateAPIView):
    http_method_names = ["put"]
    queryset = UserAddress.objects.all()
    serializer_class = ChangeCurrentAddressSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)




