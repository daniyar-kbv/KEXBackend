from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import Permission

from .models import User


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(required=False)
    branch = serializers.SerializerMethodField(required=False)
    role = serializers.SerializerMethodField(required=False)

    def get_role(self, instance):
        if instance.is_supervisor:
            return "supervisor"

        if instance.is_superuser:
            return "superuser"

        elif instance.is_credit_manager:
            return "credit_manager"

    def get_branch(self, instance) -> str:
        return instance.branch.address if instance.branch else ""

    class Meta:
        model = User
        fields = (
            "email",
            "role",
            "full_name",
            "merchant",
            "branch"
        )


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
