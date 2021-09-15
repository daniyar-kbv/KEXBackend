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
    Position,
    BranchPosition,
    ModifierGroup,
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
    class Meta:
        model = Lead
        fields = (
            "branch",
            "delivery_type",
            "order_zone",
            "estimated_duration",
        )


class IIKOModifierGroupCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="outer_id", required=True, write_only=True)
    name = serializers.CharField()

    class Meta:
        model = ModifierGroup
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        modifier_group, created = ModifierGroup.objects.get_or_create(
            outer_id=validated_data['outer_id'],
            local_brand=self.context['local_brand'],
        )

        if modifier_group.name is None:
            modifier_group.name = create_multi_language_char(validated_data['name'])
            modifier_group.save(update_fields=['name'])

        return modifier_group


class IIKOCategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="outer_id", required=True, write_only=True)
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        category, created = Category.objects.get_or_create(
            outer_id=validated_data['outer_id'],
            local_brand=self.context['local_brand'],
        )

        if category.name is None:
            category.name = create_multi_language_char(validated_data["name"])
            category.save(update_fields=["name"])

        return category


class IIKOModifierSerializer(serializers.Serializer):  # noqa
    outer_id = serializers.CharField(required=True)


class IIKOModifierGroupSerializer(serializers.Serializer):
    outer_id = serializers.CharField(required=True)
    min_amount = serializers.IntegerField(required=False, default=0)
    max_amount = serializers.IntegerField(required=False, default=1)
    is_required = serializers.BooleanField(default=False)
    modifiers = IIKOModifierSerializer(many=True, required=False, allow_null=True)


class IIKONomenclatureSerializer(serializers.ModelSerializer):
    iiko_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    iiko_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    modifier_groups = IIKOModifierGroupSerializer(many=True, required=False, allow_null=True)
    category_outer_id = serializers.UUIDField(required=True, allow_null=True, write_only=True)

    class Meta:
        model = Position
        fields = "__all__"

    @staticmethod
    def get_category(outer_id):
        return Category.objects.filter(outer_id=outer_id).first()

    def create(self, validated_data):
        position, created = Position.objects.get_or_create(
            outer_id=validated_data["outer_id"],
            local_brand=validated_data["local_brand"],
        )
        position.position_type = validated_data["position_type"]
        position.category = self.get_category(validated_data["category_outer_id"])

        if validated_data["iiko_name"] and position.name is None:
            position.name = create_multi_language_char(validated_data["iiko_name"])

        if validated_data["iiko_description"] and position.description is None:
            position.description = create_multi_language_text(validated_data["iiko_description"])

        position.save()

        for branch in validated_data["local_brand"].branches.all():
            BranchPosition.register_branch_position(
                branch=branch,
                position=position,
                modifier_groups=validated_data["modifier_groups"],
            )

        return position
