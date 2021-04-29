from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .services import verify_otp


class VerifyOTPSerializer(serializers.Serializer):  # noqa
    code = serializers.CharField(label="OTP код")
    mobile_phone = PhoneNumberField(label="Номер телефона")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        verify_otp(code=attrs.pop("code"), mobile_phone=attrs["mobile_phone"], save=True)

        return attrs
