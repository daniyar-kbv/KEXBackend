from typing import TYPE_CHECKING

from rest_framework import serializers

from apps.orders.models import (
    Cart,
    CartPosition,
    CartPositionModifier,
    CartPositionModifierGroup,
)

from ..exceptions import InvalidBranchError, BranchNotActiveError, TerminalNotActiveError

if TYPE_CHECKING:
    from apps.partners.models import Branch


class UpdateCartPositionModifierSerializer(serializers.ModelSerializer):
    position = serializers.UUIDField(required=True, write_only=True)
    count = serializers.IntegerField(required=False)

    class Meta:
        model = CartPositionModifier
        fields = (
            "position",
            "count",
        )


class UpdateCartPositionModifierGroupSerializer(serializers.ModelSerializer):
    modifier_group = serializers.UUIDField(required=True, write_only=True)
    modifiers = UpdateCartPositionModifierSerializer(many=True, required=False)

    class Meta:
        model = CartPositionModifierGroup
        fields = (
            "modifier_group",
            "modifiers",
        )


class UpdateCartPositionSerializer(serializers.ModelSerializer):
    position = serializers.UUIDField(required=True, write_only=True)
    modifier_groups = UpdateCartPositionModifierGroupSerializer(many=True, required=False)

    class Meta:
        model = CartPosition
        fields = (
            "position",
            "count",
            "position",
            "comment",
            "modifier_groups",
        )


class UpdateCartSerializer(serializers.ModelSerializer):
    positions = UpdateCartPositionSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = (
            "positions",
        )

    def validate_branch(self, branch: 'Branch'):
        if branch is None:
            raise InvalidBranchError

        if not branch.is_active:
            raise BranchNotActiveError

        if not branch.is_alive:
            raise TerminalNotActiveError

    def validate(self, attrs):
        self.validate_branch(self.context.get("branch"))
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.positions.all().delete()

        for position in validated_data.pop("positions", list()):
            cart_position = instance.positions.create(
                branch_position_id=position["position"],
                comment=position.get("comment"),
                count=position.get("count"),
            )
            for modifier_group in position.pop("modifier_groups", list()):
                cart_position_modifier_group = cart_position.modifier_groups.create(
                    modifier_group_id=modifier_group["modifier_group"],
                )
                for modifier in modifier_group.get("modifiers", list()):
                    cart_position_modifier_group.modifiers.update_or_create(
                        branch_position_id=modifier["position"],
                        count=modifier.get("count")
                    )

        return instance
