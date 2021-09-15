from rest_framework import serializers
from apps.orders.models import (
    Cart,
    CartPosition,
    CartPositionModifier,
    CartPositionModifierGroup,
)
from apps.nomenclature.models import BranchPosition


class BranchPositionShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
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

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context.get("language", "ru"))

    def get_image(self, obj):
        if not obj.position.image:
            return

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.position.image.url)

    def get_description(self, obj):
        if not obj.description:
            return

        return obj.description.text(lang=self.context.get("language", "ru"))


class RetrieveCartPositionModifierSerializer(serializers.ModelSerializer):
    position = BranchPositionShortSerializer(source="branch_position") #, read_only=True)

    class Meta:
        model = CartPositionModifier
        fields = (
            "position",
            "count",
        )


class RetrieveCartPositionModifierGroupSerializer(serializers.ModelSerializer):
    modifier_group = serializers.UUIDField(required=True, source="position_modifier_group_id")
    name = serializers.SerializerMethodField(required=False)
    modifiers = RetrieveCartPositionModifierSerializer(many=True, required=False)

    class Meta:
        model = CartPositionModifierGroup
        fields = (
            "name",
            "modifier_group",
            "modifiers",
        )

    def get_name(self, obj):
        if not obj.position_modifier_group or not obj.position_modifier_group.name:
            return

        return obj.position_modifier_group.name.text(lang=self.context.get("language", "ru"))


class RetrieveCartPositionSerializer(serializers.ModelSerializer):
    position = BranchPositionShortSerializer(source="branch_position")
    modifier_groups = RetrieveCartPositionModifierGroupSerializer(
        source='position_modifier_groups', many=True, required=False
    )

    class Meta:
        model = CartPosition
        fields = (
            "count",
            "position",
            "comment",
            "modifier_groups",
        )


class RetrieveCartSerializer(serializers.ModelSerializer):
    positions = RetrieveCartPositionSerializer(many=True, required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    positions_count = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = (
            'price',
            'positions_count',
            'positions',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['has_unavailable_positions'] = not all([position['position']['is_available'] for position in data['positions']])

        return data
