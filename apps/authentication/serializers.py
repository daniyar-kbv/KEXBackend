from uuid import uuid4

from phonenumber_field.serializerfields import PhoneNumberField
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

User = get_user_model()


class RegisterAccountSerializer(serializers.ModelSerializer):
    mobile_phone = PhoneNumberField(
        required=True, write_only=True, label="Мобильный телефон"
    )

    class Meta:
        model = User
        fields = "mobile_phone",

    @transaction.atomic
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
