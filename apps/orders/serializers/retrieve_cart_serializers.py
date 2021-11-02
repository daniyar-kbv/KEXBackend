from rest_framework import serializers
from apps.orders.models import (
    Cart,
    CartPosition,
    CartPositionModifier,
)
from apps.nomenclature.models import BranchPosition


class BranchPositionShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    category = serializers.UUIDField(source="branch_category_id", read_only=True)

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "image",
            "price",
            "position_type",
            "category",
            "is_available",
            "description",
        )
        extra_kwargs = {
            "price": {"read_only": True}
        }

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            image = obj.position.mobile_image if request.user_agent.is_mobile else obj.position.web_image
            if image:
                return request.build_absolute_uri(image.url)


class RetrieveCartPositionModifiersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='position_modifier_group.name', required=False)
    position = BranchPositionShortSerializer(source="branch_position")
    modifier_group = serializers.UUIDField(source='position_modifier_group.uuid')

    class Meta:
        model = CartPositionModifier
        fields = (
            "name",
            "position",
            "modifier_group",
            "count",
        )


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
