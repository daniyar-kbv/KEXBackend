from decimal import Decimal
from typing import List, Dict

from rest_framework import serializers

from apps.orders.models import Lead
from apps.location.models import Address
from apps.partners.models import Branch
from apps.common.utils import create_multi_language_char
from apps.nomenclature.models import (
    Category,
    LocalCategory,
    BranchCategory,
    LocalPosition,
    BranchPosition,
    ModifierGroup,
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


class IIKOModifierGroupCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="outer_id", required=True, write_only=True)
    name = serializers.CharField(source="iiko_name")

    class Meta:
        model = ModifierGroup
        fields = (
            "id",
            "name",
            "min_amount",
            "max_amount",
        )

    def create(self, validated_data):
        instance, created = ModifierGroup.objects.get_or_create(
            outer_id=validated_data["outer_id"],
            local_brand_id=self.context["local_brand_id"],
        )

        if instance.name is None:
            instance.name = create_multi_language_char(validated_data["iiko_name"])
            instance.save(update_fields=["name"])

        return instance


class IIKOCategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="outer_id", required=True, write_only=True)
    name = serializers.CharField(source="iiko_name")

    class Meta:
        model = BranchCategory
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        branch = self.context["branch"]

        outer_id, name = (
            validated_data["outer_id"],
            validated_data["iiko_name"],
        )

        category, created = Category.objects.get_or_create(
            outer_id=outer_id,
            brand_id=branch.local_brand.brand_id,
        )

        if category.name is None:
            category.name = create_multi_language_char(name)
            category.save(update_fields=["name"])

        local_category, created = LocalCategory.objects.update_or_create(
            outer_id=outer_id,
            category=category,
            local_brand_id=branch.local_brand_id,
            defaults={
                "name": category.name,
            }
        )

        branch_category, created = BranchCategory.objects.update_or_create(
            outer_id=outer_id,
            local_category=local_category,
            branch_id=branch.id,
            defaults={
                "name": category.name,
            }
        )

        return branch_category


class IIKOModifierSerializer(serializers.Serializer):  # noqa
    outer_id = serializers.CharField(required=True)


class IIKOModifierGroupSerializer(serializers.Serializer):
    outer_id = serializers.CharField(required=True)
    min_amount = serializers.IntegerField(required=False, default=0)
    max_amount = serializers.IntegerField(required=False, default=1)
    required = serializers.BooleanField(default=False)
    modifiers = IIKOModifierSerializer(many=True, required=False, allow_null=True)


class IIKONomenclatureSerializer(serializers.ModelSerializer):
    iiko_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    iiko_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    modifier_groups = IIKOModifierGroupSerializer(many=True, required=False, allow_null=True)
    category_outer_id = serializers.UUIDField(required=False, allow_null=True, write_only=True)
    is_additional = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = LocalPosition
        fields = "__all__"

    def validate(self, attrs):
        return super().validate(attrs)

    @staticmethod
    def get_local_branch_categories(outer_id):
        if outer_id is None:
            return None, None

        return (
            LocalCategory.objects.filter(outer_id=outer_id).first(),
            BranchCategory.objects.filter(outer_id=outer_id).first(),
        )

    def create(self, validated_data):
        modifier_groups: List[Dict] = validated_data.pop("modifier_groups") or list()
        local_category, branch_category = self.get_local_branch_categories(
            validated_data.pop("category_outer_id")
        )

        local_position, created = LocalPosition.objects.update_or_create(  # noqa
            outer_id=validated_data.get("outer_id"),
            defaults={
                "local_brand": validated_data.get("local_brand"),
                "local_category": local_category,
            }
        )
        if local_position.name is None and validated_data.get("iiko_name"):
            local_position.name = create_multi_language_char(validated_data["iiko_name"])
            local_position.save(update_fields=["name"])

        branch_position, created = BranchPosition.objects.update_or_create(  # noqa
            branch=self.context["branch"],
            local_position=local_position,
            defaults={
                "name": local_position.name,
                "outer_id": local_position.outer_id,
                "iiko_name": validated_data.get("iiko_name"),
                "iiko_description": validated_data.get("iiko_description"),
                "is_additional": validated_data.get("is_additional"),
            }
        )

        for modifier_group in modifier_groups:
            group = ModifierGroup.objects.get(outer_id=modifier_group["outer_id"])
            branch_position.modifier_groups.add(group)

            for modifier in modifier_group["modifiers"] or list():
                BranchPositionModifier.objects.update_or_create(
                    main_position_id=branch_position.uuid,
                    modifier=BranchPosition.objects.get(
                        outer_id=modifier["outer_id"],
                    ),
                    defaults={
                        "modifier_group": group,
                    }
                )

        return local_position
