from decimal import Decimal
from typing import TYPE_CHECKING, List, Dict

from rest_framework import serializers
from django.db.transaction import atomic

from apps.orders.models import Lead
from apps.location.models import Address
from apps.partners.models import Branch
from apps.nomenclature.models import LocalPosition, BranchPosition, BranchPositionModifier

if TYPE_CHECKING:
    from ..python_entities.positions import (
            Modifier as PythonModifier,
    )


class IIKOAddressSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField()
    latitude = serializers.CharField()
    # city = serializers.CharField()

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


class IIKOModifierSerializer(serializers.Serializer):
    outer_id = serializers.CharField(required=True)
    min_amount = serializers.IntegerField(required=False, default=0)
    max_amount = serializers.IntegerField(required=False, default=1)
    required = serializers.BooleanField(default=False)


class IIKONomenclatureSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    iiko_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    iiko_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    modifiers = IIKOModifierSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = LocalPosition
        fields = "__all__"

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        modifiers: List[Dict] = validated_data.pop('modifiers') or list()

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
                "price": validated_data.get('price') or Decimal(0),
                "outer_id": local_position.outer_id,
                "iiko_name": validated_data.get("iiko_name"),
                "iiko_description": validated_data.get("iiko_description"),
                "name": local_position.name,
            }
        )

        print("modifier:", modifiers)

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
