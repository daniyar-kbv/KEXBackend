from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.orders.models import Order

from . import PaymentTypes
from .models import Payment, DebitCard
from .exceptions import OrderAlreadyPaidError


class DebitCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = (
            "uuid",
            "card_holder_name",
            "card_masked_number",
            "card_expiration_date",
            "card_type",
        )


class CreatePaymentSerializer(serializers.ModelSerializer):
    lead = serializers.UUIDField(required=True, write_only=True)
    card_holder_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Payment
        fields = (
            "lead",
            "pa_req",
            "acs_url",
            "outer_id",
            "payment_type",
            "card_holder_name",
            "cryptogram",
            "status",
            "status_reason",
        )
        extra_kwargs = {
            "status": {"read_only": True},
            "outer_id": {"read_only": True},
            "status_reason": {"read_only": True},
            "cryptogram": {"write_only": True},
            "payment_type": {"write_only": True},
            "pa_req": {"read_only": True, "required": False},
            "acs_url": {"read_only": True, "required": False},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        order = get_object_or_404(Order, lead_id=attrs.pop("lead"))

        if order.payments.completed().exists():
            raise OrderAlreadyPaidError()

        attrs["order"] = order
        attrs["price"] = order.cart.price

        return attrs

    def create(self, validated_data):
        from apps.pipeline.cloudpayments.services import make_payment

        request = self.context["request"]

        validated_data["ip_address"] = request.META["REMOTE_ADDR"]
        validated_data["debit_card"] = DebitCard.objects.create(
            card_holder_name=validated_data.pop("card_holder_name"),
            user=request.user,
        )

        payment = super().create(validated_data)
        make_payment(payment.pk)
        payment.refresh_from_db()

        return payment


class Confirm3DSPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "pa_res",
            "outer_id",
            "status",
            "status_reason",
        )
        extra_kwargs = {
            "status": {"read_only": True},
            "outer_id": {"read_only": True},
            "status_reason": {"read_only": True},
        }

    def update(self, instance, validated_data):
        from apps.pipeline.cloudpayments.services import confirm_payment_3ds

        payment = super().update(instance, validated_data)
        confirm_payment_3ds(payment.pk)
        payment.refresh_from_db()

        return payment
