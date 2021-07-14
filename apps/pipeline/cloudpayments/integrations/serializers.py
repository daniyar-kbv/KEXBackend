from rest_framework import serializers

from apps.payments import PaymentStatusTypes
from apps.payments.models import Payment


class CloudPaymentsPaymentSerializer(serializers.ModelSerializer):
    success = serializers.BooleanField(required=True, write_only=True)
    card_masked_number = serializers.CharField(required=False, allow_null=True, write_only=True)
    card_expiration_date = serializers.CharField(required=False, allow_null=True, write_only=True)
    card_type = serializers.CharField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Payment
        fields = (
            "rrn",
            "status",
            "success",
            "outer_id",
            "card_type",
            "card_masked_number",
            "card_expiration_date",
        )

    def update(self, instance, validated_data):
        status = validated_data.pop("status")

        instance.debit_card.is_active = validated_data["success"]
        instance.debit_card.card_type = validated_data.pop("card_type", None)
        instance.debit_card.card_masked_number = validated_data.pop("card_masked_number", None)
        instance.debit_card.card_expiration_date = validated_data.pop("card_expiration_date", None)
        instance.debit_card.save(update_fields=[
            'is_active',
            'card_type',
            'card_masked_number',
            'card_expiration_date',
        ])

        payment = super().update(instance, validated_data)

        if status == PaymentStatusTypes.COMPLETED:
            payment.mark_as_completed()

        return payment
