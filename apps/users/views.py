from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.common.mixins import JSONRendererMixin

from .serializers import (
    AccountInfoSerializer,
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


# class AddUserAddress(JSONRendererMixin, GenericAPIView):
