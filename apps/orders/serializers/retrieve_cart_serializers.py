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
    category = serializers.UUIDField(source="branch_category_id", read_only=True)

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "image",
            "price",
            "category",
        )
        extra_kwargs = {
            "price": {"read_only": True}
        }

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context.get("language", "ru"))

    def get_image(self, obj):
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


class RetrieveCartPositionModifierSerializer(serializers.ModelSerializer):
    position = BranchPositionShortSerializer(source="branch_position") #, read_only=True)

    class Meta:
        model = CartPositionModifier
        fields = (
            "position",
            "count",
        )


class RetrieveCartPositionModifierGroupSerializer(serializers.ModelSerializer):
    group_uuid = serializers.UUIDField(required=True, write_only=True)
    modifiers = RetrieveCartPositionModifierSerializer(many=True, required=False)

    class Meta:
        model = CartPositionModifierGroup
        fields = (
            "group_uuid",
            "modifiers",
        )


class RetrieveCartPositionSerializer(serializers.ModelSerializer):
    position = BranchPositionShortSerializer(source="branch_position")#, read_only=True)
    modifier_groups = RetrieveCartPositionModifierGroupSerializer(many=True, required=False)

    class Meta:
        model = CartPosition
        fields = (
            "position",
            "count",
            "position",
            "comment",
            "modifier_groups",
        )


class RetrieveCartSerializer(serializers.ModelSerializer):
    positions = RetrieveCartPositionSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = (
            "positions",
        )