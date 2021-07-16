from rest_framework import serializers

from apps.payments import PaymentStatusTypes
from apps.payments.models import Payment

from .declined_codes import REASON_CODES


class CloudPaymentsPaymentSerializer(serializers.ModelSerializer):
    card_masked_number = serializers.CharField(required=False, allow_null=True, write_only=True)
    card_expiration_date = serializers.CharField(required=False, allow_null=True, write_only=True)
    card_token = serializers.CharField(required=False, allow_null=True, write_only=True)
    card_type = serializers.CharField(required=False, allow_null=True, write_only=True)
    reason_code = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Payment
        fields = (
            "rrn",
            "status",
            "pa_req",
            "pa_res",
            "acs_url",
            "outer_id",
            "card_type",
            "card_token",
            "reason_code",
            "card_masked_number",
            "card_expiration_date",
        )

    def update(self, instance, validated_data):
        print("validated_data", validated_data)
        status = validated_data.pop("status")
        status_reason = REASON_CODES.get(validated_data.get("reason_code"))

        instance.debit_card.is_active = status == PaymentStatusTypes.COMPLETED
        instance.debit_card.card_type = validated_data.pop("card_type", None)
        instance.debit_card.card_token = validated_data.pop("card_token", None)
        instance.debit_card.card_masked_number = validated_data.pop("card_masked_number", None)
        instance.debit_card.card_expiration_date = validated_data.pop("card_expiration_date", None)
        instance.debit_card.save(update_fields=[
            'is_active',
            'card_type',
            'card_token',
            'card_masked_number',
            'card_expiration_date',
        ])

        payment = super().update(instance, validated_data)
        payment.change_status(status, status_reason)

        return payment
