from rest_framework import serializers
from apps.orders.models import (
    Cart,
    CartPosition,
    CartPositionModifier,
    CartPositionModifierGroup,
)
from apps.nomenclature.models import BranchPosition


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

    def update(self, instance, validated_data):
        for position in validated_data.pop("positions", list()):
            cart_position, created = instance.positions.update_or_create(
                branch_position_id=position["position"],
                defaults={
                    "comment": position["comment"],
                    "count": position["count"],
                }
            )
            print(cart_position, created)

            for modifier_group in position.pop("modifier_groups", list()):
                cart_position_modifier_group, created = cart_position.modifier_groups.update_or_create(
                    modifier_group_id=modifier_group["modifier_group"],
                )
                print(cart_position_modifier_group, created)

                for modifier in modifier_group.get("modifiers", list()):
                    ctp, created = cart_position_modifier_group.modifiers.update_or_create(
                        branch_position_id=modifier["position"],
                        defaults={
                            "count": modifier.get("count"),
                        }
                    )
                    print(ctp, created)

        return instance


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