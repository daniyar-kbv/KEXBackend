from rest_framework import serializers

from apps.location.models import Address
from apps.partners.exceptions import BrandNotFound
from apps.orders.models import Cart, CartPosition, CartPositionModifier
from apps.nomenclature.models import (
    BranchCategory,
    BranchPosition,
    ModifierGroup,
    BranchPositionModifier,
)

from .models import Lead


class LeadAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "city",
            "longitude",
            "latitude",
            "district",
            "street",
            "building",
            "corpus",
            "flat",
        )

    extra_kwargs = {
        "longitude": {"required": True},
        "latitude": {"required": True},
        "city": {"required": True},
    }


class ApplyLeadSerializer(serializers.ModelSerializer):
    address = LeadAddressSerializer(write_only=True, required=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "address",
            "local_brand",
        )
        extra_kwargs = {
            "uuid": {"read_only": True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not attrs["local_brand"].city == attrs["address"]["city"]:
            raise BrandNotFound

        return attrs

    def create(self, validated_data):
        print('validated_data is', validated_data)
        validated_data["address"], created = Address.objects.get_or_create(  # noqa
            **validated_data.pop("address")
        )
        print("created address", created, validated_data["address"])
        print("validated_data is:", validated_data)
        lead = super().create(validated_data)
        print("lead_is, ", lead)

        if lead.cart is None:
            lead.cart = Cart.objects.create()
            lead.save(update_fields=["cart"])

        return lead


class NomenclatureCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = BranchCategory
        fields = (
            "name",
            "uuid"
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])


class NomenclaturePositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.UUIDField(source="branch_category_id")

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "description",
            "image",
            "category",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])

    def get_description(self, obj):
        if not obj.description:
            return

        return obj.description.text(lang=self.context["language"])

    def get_image(self, obj):
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


class LeadNomenclatureSerializer(serializers.ModelSerializer):
    categories = NomenclatureCategorySerializer(source="branch_categories", many=True, read_only=True)
    positions = NomenclaturePositionSerializer(source="branch_positions", many=True, read_only=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "categories",
            "positions",
        )
        extra_kwargs = {
            "uuid": {"read_only": True}
        }

    def to_representation(self, instance):
        # todo: add select relates
        data = super().to_representation(instance)
        data["categories"] = NomenclatureCategorySerializer(
            instance=instance.branch.branch_categories.filter(
                name__isnull=False,
                is_active=True,
            ),
            many=True, context=self.context,
        ).data
        data["positions"] = NomenclaturePositionSerializer(
            instance=instance.branch.branch_positions.filter(
                branch_category__isnull=False,
                name__isnull=False,
            ),
            many=True, context=self.context,
        ).data

        return data


class ModifierSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="modifier.uuid")
    name = serializers.SerializerMethodField()

    class Meta:
        model = BranchPositionModifier
        fields = (
            "uuid",
            "name",
        )

    def get_name(self, obj):
        if not obj.modifier.name:
            return

        return obj.modifier.name.text(lang=self.context["language"])


class ModifierGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    modifiers = ModifierSerializer(many=True, required=False)

    class Meta:
        model = ModifierGroup
        fields = (
            "uuid",
            "name",
            "modifiers",
            "min_amount",
            "max_amount",
            "is_required",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])


class BranchPositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    modifier_groups = ModifierGroupSerializer(many=True, required=False)

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "description",
            "image",
            "price",
            "branch_category",
            "modifier_groups",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])

    def get_description(self, obj):
        if not obj.description:
            return

        return obj.description.text(lang=self.context["language"])

    def get_image(self, obj):
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


class BranchPositionShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.UUIDField(source="branch_category_id")

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "image",
            "price",
            "category",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context.get("language", "ru"))

    def get_image(self, obj):
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


class CartPositionModifierSerializer(serializers.ModelSerializer):
    position_uuid = serializers.UUIDField(required=True, write_only=True)
    position = BranchPositionShortSerializer(source="branch_position", read_only=True)

    class Meta:
        model = CartPositionModifier
        fields = (
            "position",
            "position_uuid",
            "count",
        )


class CartPositionSerializer(serializers.ModelSerializer):
    modifiers = CartPositionModifierSerializer(many=True, required=False)
    position_uuid = serializers.UUIDField(required=True, write_only=True)
    position = BranchPositionShortSerializer(source="branch_position", read_only=True)

    class Meta:
        model = CartPosition
        fields = (
            "position_uuid",
            "count",
            "position",
            "comment",
            "modifiers",
        )


class UpdateCartSerializer(serializers.ModelSerializer):
    positions = CartPositionSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = (
            "positions",
        )

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")

        for position in positions:
            print("position is", position)
            cart_position, created = instance.positions.update_or_create(
                branch_position_id=position["position_uuid"],
                defaults={
                    "comment":position["comment"],
                    "count": position["count"],
                }
            )

            for modifier in position.get("modifiers", list()):
                cart_position.modifiers.update_or_create(
                    branch_position_id=modifier["position_uuid"],
                    defaults={
                        "count": modifier["count"],
                    }
                )

        return instance
