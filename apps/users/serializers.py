from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import Permission

from apps.location.models import Address

from .models import User, UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    extra_kwargs = {
        "country": {"required": True},
        "city": {"required": True},
        "longitude": {"required": True},
        "latitude": {"required": True},
    }


class AddUserAddressSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer(required=True)

    class Meta:
        model = UserAddress
        fields = "address",
        extra_kwargs = {
            "user": {"read_only": True},
            "is_current": {"read_only": True},
        }

    def create(self, validated_data):
        user_address = UserAddress.objects.create(
            is_current=True,
            user=self.context["request"].user,
            address=Address.objects.create(**validated_data["address"])
        )

        UserAddress.objects.exclude(pk=user_address.pk).update(
            is_current=False,
        )

        return user_address


class AccountInfoSerializer(serializers.ModelSerializer):
    current_address = UserAddressSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "mobile_phone",
            "current_address",
        ]


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
