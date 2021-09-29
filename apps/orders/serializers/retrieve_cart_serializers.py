from rest_framework import serializers
from apps.orders.models import (
    Cart,
    CartPosition,
    CartPositionModifier,
)
from apps.nomenclature.models import BranchPosition


class BranchPositionShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    # image = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    category = serializers.UUIDField(source="branch_category_id", read_only=True)

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            # "image",
            "price",
            "position_type",
            "category",
            "is_available",
            "description",
        )
        extra_kwargs = {
            "price": {"read_only": True}
        }

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context.get("language", "ru"))

    # def get_image(self, obj):
    #     if not obj.position.image:
    #         return
    #
    #     request = self.context.get("request")
    #     if request:
    #         return request.build_absolute_uri(obj.position.image.url)

    def get_description(self, obj):
        if not obj.description:
            return

        return obj.description.text(lang=self.context.get("language", "ru"))


class RetrieveCartPositionModifiersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(required=False)
    position = BranchPositionShortSerializer(source="branch_position")

    class Meta:
        model = CartPositionModifier
        fields = (
            "name",
            "position",
            "count",
        )

    def get_name(self, obj):
        if not obj.position_modifier_group or not obj.position_modifier_group.name:
            return

        return obj.position_modifier_group.name.text(lang=self.context.get("language", "ru"))


class RetrieveCartPositionSerializer(serializers.ModelSerializer):
    position = BranchPositionShortSerializer(source="branch_position")
    modifiers = RetrieveCartPositionModifiersSerializer(
        many=True, required=False
    )

    class Meta:
        model = CartPosition
        fields = (
            "count",
            "position",
            "comment",
            "modifiers",
        )


class RetrieveCartSerializer(serializers.ModelSerializer):
    positions = RetrieveCartPositionSerializer(source='positions.exclude_delivery', many=True, required=False)
    min_price = serializers.DecimalField(source='lead.branch.min_price', max_digits=12, decimal_places=2)
    delivery_type = serializers.CharField(source='lead.delivery_type', required=False, allow_null=True)

    class Meta:
        model = Cart
        fields = (
            'total_price',
            'delivery_type',
            'delivery_price',
            'positions_price',
            'positions_count',
            'positions',
            'min_price',
            'has_unavailable_positions',
        )
