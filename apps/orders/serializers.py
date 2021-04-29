from rest_framework import serializers

from apps.location.models import Address

from .models import Lead


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ApplyLeadSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Lead
        fields = (
            "address",
            "brand_api_login",
        )

    def create(self, validated_data):
        validated_data["address"] = Address.objects.create(
            **validated_data.pop("address")
        )

        return super().create(validated_data)
