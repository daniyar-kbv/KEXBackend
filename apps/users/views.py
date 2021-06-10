# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.common.mixins import JSONRendererMixin

from .models import User
from .serializers import (
    AccountInfoSerializer,
)


class AccountInfoView(JSONRendererMixin, GenericAPIView):
    serializer_class = AccountInfoSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)
