from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

from apps.sms.exceptions import OTPResendTimeLimit
from apps.sms.models import OTP

from .exceptions import UserNotFound

User = get_user_model()


class RegisterAccountSerializer(serializers.ModelSerializer):
    mobile_phone = PhoneNumberField(
        required=True, write_only=True, label="Мобильный телефон"
    )

    class Meta:
        model = User
        fields = "mobile_phone",

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            mobile_phone=validated_data.pop("mobile_phone"),
        )

        return user


class TokenObtainPairSerializer(serializers.Serializer): # noqa
    def validate(self, attrs):
        user = self.context["user"]
        refresh = BaseTokenObtainPairSerializer.get_token(user)

        return {
            "secret_key": user.secret_key,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class OTPResendSerializer(serializers.Serializer):  # noqa
    mobile_phone = PhoneNumberField(
        required=True, write_only=True, label="Мобильный телефон"
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not User.objects.filter(mobile_phone=attrs["mobile_phone"]).exists():
            raise UserNotFound

        # todo check otp time limit
        if OTP.objects.active().filter(mobile_phone=attrs["mobile_phone"]).exists():
            raise OTPResendTimeLimit

        return attrs
