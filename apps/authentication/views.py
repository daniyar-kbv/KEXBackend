from uuid import uuid4

from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)

from apps.sms.services import send_otp
from apps.sms.serializers import VerifyOTPSerializer
from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .serializers import TokenObtainPairSerializer, RegisterAccountSerializer

User = get_user_model()


class RegisterAccountView(
    PublicAPIMixin, JSONRendererMixin, CreateAPIView
):
    """
    Авторизация/регистрация в системе
    """

    serializer_class = RegisterAccountSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        mobile_phone = serializer.validated_data["mobile_phone"]
        serializer.save()
        transaction.on_commit(lambda: send_otp(mobile_phone))


class VerifyAccountView(
    PublicAPIMixin, JSONRendererMixin, BaseTokenObtainPairView
):
    """
    Подтверждение otp для регистрации/авторизации
    """

    queryset = User.objects.all()
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(self.queryset, mobile_phone=serializer.validated_data.pop("mobile_phone"))
        user.secret_key = uuid4()
        user.save(update_fields=["secret_key"])

        token_serializer = TokenObtainPairSerializer(data={}, context={"user": user})
        token_serializer.is_valid(raise_exception=True)

        return Response(data=token_serializer.validated_data)
