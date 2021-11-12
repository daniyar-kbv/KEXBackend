from rest_framework import serializers

from apps.location.serializers import AddressSerializer
from apps.partners.serializers import UserLocalBrandsSerializer
from apps.notifications.tasks import register_token_in_firebase

from .models import User, UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    is_current = serializers.BooleanField()
    local_brand = UserLocalBrandsSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = "__all__"


class AccountInfoSerializer(serializers.ModelSerializer):
    current_address = serializers.IntegerField(source="current_address_pk", required=False, read_only=True)
    current_debit_card = serializers.IntegerField(source="current_debit_card_pk", required=False, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "mobile_phone",
            "current_address",
            "current_debit_card",
            "last_payment_type",
            "language"
        ]
        extra_kwargs = {
            "id": {'read_only': True},
            "last_payment_type": {"read_only": True, "required": False}
        }

    def validate_language(self, value):
        if self.instance.fb_tokens:
            register_token_in_firebase.delay(topic=value, registration_tokens=self.instance.fb_tokens)

        return value


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name", "middle_name", "last_name",
            "email", "is_active", "branch",
        ]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name", "middle_name", "last_name",
            "email", "password", "is_active", "branch",
        ]

        extra_kwargs = {field: {"required": True} for field in fields if not field == "id"}
        extra_kwargs["password"] = {"write_only": True}

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            instance.set_password(validated_data.pop("password"))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["partner"] = request.user.partner
        return User.objects.create(**validated_data)
