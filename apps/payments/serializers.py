from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.orders.models import Order

from . import PaymentTypes
from .models import Payment, DebitCard
from .exceptions import OrderAlreadyPaidError

"""
dda3bfc9-a4ab-4861-a910-7cc39e2c9e88
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MzczODI4LCJqdGkiOiIyMTdkYTRiMWY2MzE0MGVkYTFjMGFmZWE3OGQ4MThjMSIsInVzZXJfaWQiOjF9.AKP_2KSCXml2DvczwbInw7YDOhf_codH3Z1ROJ1HDfU
"""

class CreatePaymentSerializer(serializers.ModelSerializer):
    lead = serializers.UUIDField(required=True, write_only=True)
    card_holder_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Payment
        fields = (
            "lead",
            "payment_type",
            "card_holder_name",
            "cryptogram",
            "order",
            "status",
            "status_reason",
        )
        extra_kwargs = {
            "order": {"read_only": True},
            "status": {"read_only": True},
            "status_reason": {"read_only": True},
            "cryptogram": {"write_only": True},
            "payment_type": {"write_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        order = get_object_or_404(Order, lead_id=attrs.pop("lead"))

        if order.payments.completed().exists():
            raise OrderAlreadyPaidError()

        attrs["order"] = order
        attrs["price"] = order.cart.price

        return attrs

    def check_payment_status(self):
        ...

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
