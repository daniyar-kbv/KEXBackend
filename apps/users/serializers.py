from rest_framework import serializers

from apps.location.serializers import AddressSerializer

from .models import User, UserAddress
from ..notifications.firebase import subscribe_to_language_topic


class UserAddressListSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = "__all__"


class UpdateUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "local_brand",
        extra_kwargs = {
            "local_brand": {"required": False}
        }

    def update(self, instance, validated_data):
        user = self.context["request"].user
        user.set_current_address(instance)

        return super().update(instance, validated_data)


class AccountInfoSerializer(serializers.ModelSerializer):
    current_address = AddressSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "mobile_phone",
            "current_address",
            "language"
        ]

    def validate_language(self, value):
        subscribe_to_language_topic(value, [self.instance.fb_token])
        return value


class UserViewSerializer(serializers.ModelSerializer):
    """
    List, Retrieve serializer for User model
    """
    class Meta:
        model = User
        fields = [
            "id",
            "first_name", "middle_name", "last_name",
            "email", "is_active", "branch",
        ]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Create, Update serializer for User model
    """
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
