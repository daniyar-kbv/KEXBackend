from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from rest_framework import serializers

from apps.orders.models import Lead
from apps.location.models import Address
from apps.partners.models import Organization
from apps.nomenclature.models import Position, PositionInfoByOrganization

if TYPE_CHECKING:
    from ..python_entities.positions import (
            Modifier as PythonModifier,
            Position as PythonPosition,
    )


class IIKOAddressSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField()
    latitude = serializers.CharField()

    class Meta:
        model = Address
        fields = "__all__"


class IIKOOrganizationSerializer(serializers.ModelSerializer):
    address = IIKOAddressSerializer(required=False)

    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        address = validated_data.pop("address", None)

        instance, created = Organization.objects.update_or_create(
            outer_id=validated_data.pop("outer_id"),
            defaults={
                "is_active": True,
                **validated_data,
            }
        )

        address_serializer = IIKOAddressSerializer(
            instance=instance.address,
            data=address,
        )
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save()

        return instance


class IIKOLeadOrganizationSerializer(serializers.ModelSerializer):
    organization_outer_id = serializers.CharField(required=True)

    class Meta:
        model = Lead
        fields = (
            "order_zone",
            "estimated_duration",
            "organization_outer_id",
        )

    def update(self, instance, validated_data):
        validated_data["organization"] = Organization.objects.get(  # noqa
            outer_id=validated_data.pop("organization_outer_id")
        )

        return super().update(instance, validated_data)


class IIKONomenclatureSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)

    class Meta:
        model = Position
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        modifiers: List['PythonModifier'] = validated_data.pop('modifiers', None)
        price: Decimal = validated_data.pop("price", Decimal(0))

        position, created = Position.objects.update_or_create(
            outer_id=validated_data.pop("outer_id"),
            defaults={
                **validated_data
            }
        )

        PositionInfoByOrganization.objects.get_or_create(
            organization=self.context["organization"],
            position=position,
            defaults={
                "price": price,
            }
        )

        return position
