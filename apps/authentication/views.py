from uuid import uuid4

import requests
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)

from apps.sms.services import send_otp
from apps.sms.serializers import VerifyOTPSerializer
from apps.common.mixins import JSONRendererMixin, PublicAPIMixin
from django.conf import settings
from .serializers import (
    TokenObtainPairSerializer,
    RegisterAccountSerializer,
    OTPResendSerializer,
)
from ..promotions.models import Participation, Promotion

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
        print(request.headers)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(self.queryset, mobile_phone=serializer.validated_data.pop("mobile_phone"))
        user.secret_key = uuid4()
        user.save(update_fields=["secret_key"])

        token_serializer = TokenObtainPairSerializer(data={}, context={"user": user})
        token_serializer.is_valid(raise_exception=True)

        return Response(data=token_serializer.validated_data)


class OTPResendView(PublicAPIMixin, JSONRendererMixin, GenericAPIView):
    """
    Запрос на повторную отправку otp
    """
    serializer_class = OTPResendSerializer

    def post(self, request, *args, **kwargs): # noqa
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_otp(serializer.validated_data['mobile_phone'])

        return Response(data={})


class InstagramAuthView(PublicAPIMixin, JSONRendererMixin, APIView):
    """
    Получение кода авторизации
    """

    def get(self, request, promo_type):  # noqa
        username = None
        # print('instagram view')
        code = request.GET.get('code')
        if code:
            code = code.split('#')[0]
            # print("auth code: ", code)
            data = {
                'client_id': settings.INSTAGRAM_CLIENT_ID,
                'client_secret': settings.INSTAGRAM_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': request.build_absolute_uri(settings.INSTAGRAM_REDIRECT_URI + promo_type)
            }
            response = requests.post(
                url='https://api.instagram.com/oauth/access_token/',
                data=data,
            )
            # print("getting access token:")
            # print("response: ", response)
            # print("response content: ", response.content)
            # print(response.json())
            # print(response.text)
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                # print("access_token: ", access_token)
                if access_token:
                    resp = requests.get(
                        f'https://graph.instagram.com/me?fields=id,username&access_token={access_token}'
                    )
                    # print("getting user profile:")
                    # print("response: ", response)
                    # print("response content: ", response.content)
                    if resp.status_code == 200:
                        # print(resp.content)
                        Participation.objects.create(
                            user=request.user,
                            promotion=Promotion.objects.filter(promo_type=promo_type).first(),
                            instagram_username=resp.json().get('username')
                        )
                        # print(username)

        return redirect('promotions:promotion_contest_render_view', promo_type=promo_type)
