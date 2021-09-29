from typing import TYPE_CHECKING

from rest_framework import serializers

from apps.partners import DeliveryTypes
from apps.orders.models import (
    Cart, CartPosition, CartPositionModifier
)

from ..exceptions import InvalidBranchError, BranchNotActiveError


if TYPE_CHECKING:
    from apps.partners.models import Branch


class UpdateCartPositionModifiersSerializer(serializers.ModelSerializer):
    position = serializers.UUIDField(source='branch_position')
    modifier_group = serializers.UUIDField(source='position_modifier_group')

    class Meta:
        model = CartPositionModifier
        fields = (
            "modifier_group",
            "position",
            "count",
        )


class UpdateCartPositionSerializer(serializers.ModelSerializer):
    position = serializers.UUIDField(required=True, write_only=True)
    modifiers = UpdateCartPositionModifiersSerializer(
        many=True, required=False
    )

    class Meta:
        model = CartPosition
        fields = (
            "position",
            "count",
            "comment",
            "modifiers",
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

    def validate(self, attrs):
        self.validate_branch(self.context.get("branch"))
        return super().validate(attrs)

    def update(self, instance, validated_data):
        print('UpdateCartSerializer (validated_data):', validated_data)
        instance.positions.exclude(branch_position__position__position_type__in=[
            DeliveryTypes.NIGHT_DELIVERY, DeliveryTypes.DAY_DELIVERY]
        ).delete()

        for position in validated_data.pop('positions', []):
            cart_position = instance.positions.create(
                branch_position_id=position['position'],
                comment=position.get('comment'),
                count=position.get('count', 1),
            )
            for modifier in position.pop('modifiers', []):
                cart_position.modifiers.create(
                    position_modifier_group_id=modifier['position_modifier_group'],
                    branch_position_id=modifier['branch_position'],
                    count=modifier.get('count')
                )

        return instance
