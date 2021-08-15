import jwt
from django.conf import settings
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as BaseJWTAuthentication,
    AuthenticationFailed,
)


class JWTAuthentication(BaseJWTAuthentication):
    @classmethod
    def get_device_uuid_from_payload(self, validated_token):
        payload = jwt.decode(
            jwt=str(validated_token),
            key=settings.SECRET_KEY,
            algorithms=settings.SIMPLE_JWT['ALGORITHM']
        )

        if not payload.get("device_uuid"):
            raise AuthenticationFailed('Token should have device_uuid', code='bad_authorization_header')

        return payload["device_uuid"]

    @classmethod
    def validate_device_uuid(self, user, payload_device_uuid):
        if str(user.device_uuid) != payload_device_uuid:
            raise AuthenticationFailed('Bad device uuid', code='user_not_found')

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        self.validate_device_uuid(user, self.get_device_uuid_from_payload(str(validated_token)))

        return user
