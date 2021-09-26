from rest_framework import serializers
from django.core.cache import cache

from apps.orders.models import Lead, Cart
from apps.location.models import Address
from apps.partners.models import Branch
from apps.common.utils import (
    create_multi_language_char, create_multi_language_text,
)
from apps.nomenclature.models import (
    Category,
    Position,
    BranchPosition,
    ModifierGroup,
)

from .. import ApplyTypes


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
    change_type = serializers.CharField(write_only=True, required=False, allow_null=True)
    is_open = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Lead
        fields = (
            "is_open",
            "branch",
            "change_type",
            "order_zone",
            "estimated_duration",
        )

    def update(self, instance, validated_data):
        print('FindOrganization validated_data', validated_data)
        user = instance.user
        change_type = validated_data.pop('change_type')

        lead = super().update(instance, validated_data)

        if not lead.cart:
            lead.cart = Cart.objects.create()
            lead.save(update_fields=['cart'])

        if validated_data.get('is_open'):
            lead.set_delivery_params()

        if user:
            if self.change_type == ApplyTypes.CHANGE_USER_ADDRESS_BRAND:
                user.change_address_brand(
                    lead.user.addresses.get(address=lead.address),
                    lead.local_brand,
                )
            elif change_type in [
                ApplyTypes.SWITCH_BETWEEN_USER_ADDRESSES,
                ApplyTypes.EXISTING_NEW_USER_ADDRESS,
            ]:
                user.set_current_address(
                    user.addresses.get(address=lead.address)
                )
            elif change_type == ApplyTypes.NEW_USER_ADDRESS:
                user.add_new_address(
                    lead.address, lead.local_brand
                )

        """
        add branch to cache
        for frequent updating of "stop list"
        p.s. expires in 1 hour
        """
        cache.set(str(lead.branch.outer_id), True, 60 * 60)

        return lead


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
        position.position_type = position.position_type or validated_data["position_type"]
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
