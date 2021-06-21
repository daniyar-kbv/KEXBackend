from decimal import Decimal
from typing import List, Dict

from rest_framework import serializers

from apps.orders.models import Lead
from apps.location.models import Address
from apps.partners.models import Branch
from apps.common.utils import create_multi_language_char
from apps.nomenclature.models import (
    PositionSize,
    LocalPosition,
    BranchPosition,
    BranchPositionPrice,
    BranchPositionModifier,
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
        model = Branch
        fields = "__all__"

    def create(self, validated_data):
        address = validated_data.pop("address", None)
        if address:
            address["city"] = address["city"].id

        # print('validated_data', address)

        instance, created = Branch.objects.update_or_create(
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
        validated_data["branch"] = Branch.objects.get(  # noqa
            outer_id=validated_data.pop("organization_outer_id")
        )

        return super().update(instance, validated_data)


class IIKOPositionSizeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", required=True, write_only=True)
    name = serializers.CharField(source="iiko_name")
    isDefault = serializers.BooleanField(source="is_default", default=False)

    class Meta:
        model = PositionSize
        fields = (
            "id",
            "name",
            "priority",
            "isDefault",
        )

    def create(self, validated_data):
        instance, created = PositionSize.objects.update_or_create(
            uuid=validated_data.pop("uuid"),
            defaults={
                **validated_data,
            }
        )

        if instance.name is None:
            instance.name = create_multi_language_char(instance.iiko_name)
            instance.save(update_fields=["name"])

        return instance


class IIKOModifierSerializer(serializers.Serializer):  # noqa
    outer_id = serializers.CharField(required=True)
    min_amount = serializers.IntegerField(required=False, default=0)
    max_amount = serializers.IntegerField(required=False, default=1)
    required = serializers.BooleanField(default=False)


class PricesSerializer(serializers.Serializer):  # noqa
    outer_id = serializers.UUIDField(allow_null=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)


class IIKONomenclatureSerializer(serializers.ModelSerializer):
    iiko_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    iiko_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    modifiers = IIKOModifierSerializer(many=True, required=False, allow_null=True)
    size_prices = PricesSerializer(many=True, required=True, allow_null=False)

    class Meta:
        model = LocalPosition
        fields = "__all__"

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        modifiers: List[Dict] = validated_data.pop('modifiers') or list()
        size_prices: List[Dict] = validated_data.pop('size_prices')
        print("prices in serializer:", size_prices)

        local_position, created = LocalPosition.objects.update_or_create(  # noqa
            outer_id=validated_data.get("outer_id"),
            defaults={
                "local_brand": validated_data.get("local_brand"),
            }
        )

        branch_position, created = BranchPosition.objects.update_or_create(  # noqa
            branch=self.context["branch"],
            local_position=local_position,
            defaults={
                "outer_id": local_position.outer_id,
                "iiko_name": validated_data.get("iiko_name"),
                "iiko_description": validated_data.get("iiko_description"),
                "name": local_position.name,
            }
        )
        for size_price in size_prices:
            branch_position.prices.update_or_create(
                size_id=size_price["outer_id"],
                defaults={
                    "price": size_price["price"],
                }
            )

        for modifier in modifiers:
            BranchPositionModifier.objects.update_or_create(
                main_position_id=branch_position.uuid,
                modifier=BranchPosition.objects.get(
                    branch=self.context["branch"],
                    outer_id=modifier["outer_id"],
                ),
                defaults={
                    "min_amount": modifier["min_amount"],
                    "max_amount": modifier["max_amount"],
                }
            )

        return local_position
