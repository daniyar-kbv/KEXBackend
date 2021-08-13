from typing import List, Dict

from rest_framework import serializers

from apps.orders.models import Lead
from apps.location.models import Address
from apps.partners.models import Branch
from apps.common.utils import (
    create_multi_language_char,
    create_multi_language_text,
)
from apps.nomenclature.models import (
    Category,
    BranchCategory,
    LocalPosition,
    BranchPosition,
    ModifierGroup,
    PositionModifierGroup,
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
    id = serializers.UUIDField(source="uuid", required=True, write_only=True)
    name = serializers.CharField(source="iiko_name")

    class Meta:
        model = ModifierGroup
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        instance, created = ModifierGroup.objects.get_or_create(
            uuid=validated_data["uuid"],
            local_brand_id=self.context["local_brand_id"],
        )
        instance.iiko_name = validated_data["iiko_name"]
        instance.save(update_fields=["iiko_name"])

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

        category, _ = Category.objects.get_or_create(
            outer_id=outer_id,
            brand_id=branch.local_brand.brand_id,
        )

        if category.name is None:
            category.name = create_multi_language_char(name)
            category.save(update_fields=["name"])

        local_category, _ = Category.objects.get_or_create(
            outer_id=outer_id,
            category=category,
            defaults={"local_brand_id": branch.local_brand_id},
        )

        if local_category.name is None:
            local_category.name = category.name
            local_category.save(update_fields=["name"])

        branch_category, _ = BranchCategory.objects.get_or_create(
            outer_id=outer_id,
            local_category=local_category,
            defaults={"branch_id": branch.id},
        )

        if branch_category.name is None:
            branch_category.name = category.name
            branch_category.save(update_fields=["name"])

        return branch_category


class IIKOModifierSerializer(serializers.Serializer):  # noqa
    outer_id = serializers.CharField(required=True)


class IIKOModifierGroupSerializer(serializers.Serializer):
    outer_id = serializers.CharField(required=True)
    min_amount = serializers.IntegerField(required=False, default=0)
    max_amount = serializers.IntegerField(required=False, default=1)
    is_required = serializers.BooleanField(default=False)
    modifiers = IIKOModifierSerializer(many=True, required=False, allow_null=True)


class IIKONomenclatureSerializer(serializers.ModelSerializer):
    position_type = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
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
            Category.objects.filter(outer_id=outer_id).first(),
            BranchCategory.objects.filter(outer_id=outer_id).first(),
        )

    def create(self, validated_data):
        modifier_groups: List[Dict] = validated_data.pop("modifier_groups") or list()
        local_category, branch_category = self.get_local_branch_categories(
            validated_data.pop("category_outer_id")
        )

        local_position, local_position_created = LocalPosition.objects.get_or_create(  # noqa
            outer_id=validated_data.get("outer_id"),
            local_brand=validated_data.get("local_brand"),
        )

        local_position.local_category = local_category

        if local_position.name is None and validated_data.get("iiko_name"):
            local_position.name = create_multi_language_char(validated_data["iiko_name"])

        if local_position.description is None and validated_data.get("iiko_description"):
            local_position.description = create_multi_language_text(validated_data["iiko_description"])

        local_position.save(update_fields=["local_category", "name", "description"])

        branch_position, branch_position_created = BranchPosition.objects.get_or_create(  # noqa
            branch=self.context["branch"],
            local_position=local_position,
            outer_id=local_position.outer_id,
        )
        branch_position.name = local_position.name
        branch_position.price = validated_data.get("price")
        branch_position.description = local_position.description
        branch_position.iiko_name=validated_data.get("iiko_name")
        branch_position.position_type = validated_data.get("position_type")
        branch_position.iiko_description=validated_data.get("iiko_description")
        branch_position.is_additional=validated_data.get("is_additional")
        branch_position.save()

        for modifier_group in modifier_groups:
            position_modifier_group, _ = PositionModifierGroup.objects.update_or_create(
                modifier_group_id=modifier_group["outer_id"],
                branch_position_id=branch_position.id,
                defaults={
                    "is_required": modifier_group["is_required"],
                    "min_amount": modifier_group["min_amount"],
                    "max_amount": modifier_group["max_amount"],
                }
            )

            for modifier in modifier_group["modifiers"] or list():
                BranchPositionModifier.objects.update_or_create(
                    modifier=BranchPosition.objects.get(
                        outer_id=modifier["outer_id"],
                    ),
                    defaults={
                        "position_modifier_group": position_modifier_group,
                    }
                )

        return local_position
