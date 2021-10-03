from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.orders.models import Lead, Order
from apps.location.serializers import AddressSerializer
from apps.partners.serializers import SquareImageBrandSerializer
from apps.nomenclature.models import (
    BranchPosition,
    PositionModifierGroup,
    PositionModifier,
)

from .retrieve_cart_serializers import RetrieveCartSerializer

from ..exceptions import EmptyCartError


class ModifierSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="modifier.uuid")
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = PositionModifier
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
        request = self.context.get("request")
        if request:
            image = obj.modifier.position.mobile_image if request.user_agent.is_mobile else obj.modifier.position.web_image
            if image:
                return request.build_absolute_uri(image.url)


class ModifierGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    modifiers = ModifierSerializer(many=True, required=False)

    class Meta:
        model = PositionModifierGroup
        fields = (
            "uuid",
            "name",
            "modifiers",
            "min_amount",
            "max_amount",
            "is_required",
        )

    def get_name(self, obj):
        if not obj.modifier_group.name:
            return

        return obj.modifier_group.name.text(lang=self.context["language"])


class BranchPositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    branch_category = serializers.UUIDField(source='category_id')
    modifier_groups = ModifierGroupSerializer(source="position_modifier_groups", many=True, required=False)

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
        request = self.context.get("request")
        if request:
            image = obj.position.mobile_image if request.user_agent.is_mobile else obj.position.web_image
            if image:
                return request.build_absolute_uri(image.url)


class OrdersListSerializer(serializers.ModelSerializer):
    cart = RetrieveCartSerializer()
    address = AddressSerializer(source="lead.address")
    brand = SquareImageBrandSerializer(source="lead.local_brand.brand")
    price = serializers.CharField(source="completed_payment.price", required=False)
    created_at = serializers.DateTimeField(source="completed_payment.created_at", required=False)
    payment_type = serializers.CharField(source="completed_payment.payment_type", required=False)
    check_url = serializers.SerializerMethodField()

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
            "check_url",
        )

    def get_check_url(self, obj):
        return self.context['request'].build_absolute_uri(f"{obj.lead_id}/check/")


class CreateOrderSerializer(serializers.ModelSerializer):
    lead = serializers.UUIDField(required=True)

    class Meta:
        model = Order
        fields = "lead",

    def validate_lead(self, value):
        return get_object_or_404(Lead, uuid=value)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs["lead"].cart is None or not attrs["lead"].cart.positions.exists():
            raise EmptyCartError

        return attrs

    def create(self, validated_data):
        lead = validated_data['lead']
        if not lead.user:
            lead.user = self.context["request"].user
            lead.save(update_fields=['user'])

        return Order.objects.get_or_create_from_lead(lead)
