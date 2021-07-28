from rest_framework import serializers

from apps.orders.models import Lead, Order
from apps.users.serializers import ShortAddressSerializer
from apps.partners.serializers import SquareImageBrandSerializer
from apps.nomenclature.models import (
    BranchPosition,
    ModifierGroup,
    BranchPositionModifier,
)

from .retrieve_cart_serializers import RetrieveCartSerializer

from ..exceptions import (
    EmptyCartError,
    OrderAlreadyExistError,
)


class ModifierSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="modifier.uuid")
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = BranchPositionModifier
        fields = (
            "uuid",
            "name",
            "image",
        )

    def get_name(self, obj):
        if not obj.modifier.name:
            return

        return obj.modifier.name.text(lang=self.context["language"])

    def get_image(self, obj):
        if not obj.modifier.local_position.image:
            return

        return self.context["request"].build_absolute_uri(
            obj.modifier.local_position.image.url
        )


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


class OrdersListSerializer(serializers.ModelSerializer):
    cart = RetrieveCartSerializer()
    address = ShortAddressSerializer(source="lead.address")
    brand = SquareImageBrandSerializer(source="lead.local_brand.brand")
    price = serializers.CharField(source="completed_payment.price", required=False)
    created_at = serializers.DateTimeField(source="completed_payment.created_at", required=False)
    payment_type = serializers.CharField(source="completed_payment.payment_type", required=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "brand",
            "address",
            "cart",
            "price",
            "created_at",
            "status",
            "payment_type",
            "status_reason",
            "lead_id",
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    lead = serializers.UUIDField(required=True)

    class Meta:
        model = Order
        fields = "lead",

    def validate(self, attrs):
        attrs = super().validate(attrs)
        lead = Lead.objects.get(uuid=attrs["lead"])

        if hasattr(lead, "order"):
            raise OrderAlreadyExistError
        if lead.cart is None or not lead.cart.positions.exists():
            raise EmptyCartError

        attrs["lead"] = lead
        return attrs

    def create(self, validated_data):
        return Order.objects.create_from_lead(
            self.context["request"].user,
            validated_data["lead"]
        )
