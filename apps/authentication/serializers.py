from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):  # noqa
    def validate(self, attrs):
        try:
            attrs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**attrs) # noqa

        if self.user is None or not self.user.is_active:
            raise AuthenticationFailed(
                self.error_messages["no_active_account"], "no_active_account",
            )

        refresh = self.get_token(self.user)  # noqa

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # if user.is_staff or user.is_credit_manager or user.is_supervisor:
        #     serializer = UserInfoSerializer(instance=user)
        #     token["email"] = user.email
        #     token["full_name"] = serializer.data["full_name"]
        #     token["merchant"] = serializer.data["merchant"]
        #     token["branch"] = serializer.data["branch"]
        #     token["role"] = serializer.data["role"]
        #
        # else:
        #     token["iin"] = user.person.iin
        #     record = user.person.records.last()
        #
        #     if record:
        #         token["first_name"] = record.first_name
        #         token["last_name"] = record.last_name
        #         token["middle_name"] = record.middle_name
        #
        #     else:
        #         token["first_name"] = token["last_name"] = token["middle_name"] = None
        #
        return token


class TokenOutputSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
