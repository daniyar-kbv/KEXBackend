from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.orders.models import Order
from apps.pipeline.cloudpayments.services import make_payment, make_card_payment

from . import PaymentTypes, PaymentStatusTypes
from .models import Payment, DebitCard
from .exceptions import OrderAlreadyPaidError, ChangeForNotSetError


class DebitCardsSerializer(serializers.ModelSerializer):
    is_current = serializers.BooleanField(read_only=True, required=False)

    class Meta:
        model = DebitCard
        fields = (
            "uuid",
            "is_current",
            "card_holder_name",
            "card_masked_number",
            "card_expiration_date",
            "card_type",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "card_holder_name": {"read_only": True},
            "card_masked_number": {"read_only": True},
            "card_expiration_date": {"read_only": True},
            "card_type": {"read_only": True},
        }


class CreateWidgetPaymentSerializer(serializers.ModelSerializer):
    lead = serializers.UUIDField(source="order", required=True, write_only=True)

    class Meta:
        model = Payment
        fields = ('lead', 'uuid')
        extra_kwargs = {'uuid': {'read_only': True}}

    def validate_lead(self, value):
        return get_object_or_404(Order, lead_id=value)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["order"].payments.completed().exists():
            raise OrderAlreadyPaidError()

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        validated_data['ip_address'] = request.META['REMOTE_ADDR']
        validated_data['price'] = validated_data['order'].cart.total_price
        validated_data['payment_type'] = PaymentTypes.WEB_WIDGET

        return super().create(validated_data)


class CreatePaymentMixin(serializers.ModelSerializer):
    lead = serializers.UUIDField(source="order", required=True, write_only=True)

    class Meta:
        model = Payment
        fields = "lead",

    def validate_lead(self, value):
        return get_object_or_404(Order, lead_id=value)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["order"].payments.completed().exists():
            raise OrderAlreadyPaidError()

        return attrs

    def make_payment(self, payment_pk):
        ...

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        validated_data["ip_address"] = request.META["REMOTE_ADDR"]
        if validated_data.get("payment_type") == PaymentTypes.CASH and validated_data.get('change_for'):
            validated_data["price"] = validated_data.pop("change_for")
        else:
            validated_data["price"] = validated_data["order"].cart.total_price

        payment = super().create(validated_data)

        if not payment.payment_type == PaymentTypes.CASH:
            self.make_payment(payment.pk)
        else:
            payment.change_status(PaymentStatusTypes.COMPLETED)

        payment.refresh_from_db()

        return payment


class CreatePaymentSerializer(CreatePaymentMixin):
    keep_card = serializers.BooleanField(default=False, write_only=True)
    card_holder_name = serializers.CharField(required=False, write_only=True, allow_blank=True)
    change_for = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)

    def make_payment(self, payment_pk):
        make_payment(payment_pk)

    class Meta:
        model = Payment
        fields = (
            "uuid",
            "lead",
            "pa_req",
            "acs_url",
            "outer_id",
            "keep_card",
            "change_for",
            "payment_type",
            "card_holder_name",
            "cryptogram",
            "status",
            "status_reason",
        )
        extra_kwargs = {
            "card_holder_name": {"required": False},
            "cryptogram": {"write_only": True},
            "payment_type": {"write_only": True},
            "status_reason": {"read_only": True},
            "outer_id": {"read_only": True},
            "status": {"read_only": True},
            "uuid": {"read_only": True},
            "pa_req": {"read_only": True, "required": False},
            "acs_url": {"read_only": True, "required": False},
        }

    def validate(self, attrs):
        if attrs["order"].payments.completed().exists():
            raise OrderAlreadyPaidError()

        return super().validate(attrs)


class CreateCardPaymentSerializer(CreatePaymentMixin):
    def make_payment(self, payment_pk):
        make_card_payment(payment_pk)

    class Meta:
        model = Payment
        fields = (
            "uuid",
            "lead",
            "outer_id",
            "debit_card",
            "status",
            "status_reason",
            "pa_req",
            "acs_url",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "status": {"read_only": True},
            "outer_id": {"read_only": True},
            "status_reason": {"read_only": True},
            "pa_req": {"read_only": True, "required": False},
            "acs_url": {"read_only": True, "required": False},
        }


class Confirm3DSPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "uuid",
            "acs_url",
            "pa_req",
            "pa_res",
            "outer_id",
            "status",
            "status_reason",
        )
        extra_kwargs = {
            "status": {"read_only": True},
            "uuid": {"read_only": True},
            "acs_url": {"read_only": True},
            "pa_req": {"read_only": True},
            "outer_id": {"read_only": True},
            "status_reason": {"read_only": True},
        }

    def update(self, instance, validated_data):
        from apps.pipeline.cloudpayments.services import confirm_payment_3ds

        payment = super().update(instance, validated_data)
        confirm_payment_3ds(payment.pk)
        payment.refresh_from_db()

        return payment
