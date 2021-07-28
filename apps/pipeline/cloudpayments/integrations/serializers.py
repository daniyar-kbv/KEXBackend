from rest_framework import serializers

from apps.payments.models import Payment, DebitCard

from .declined_codes import REASON_CODES


class CloudPaymentsDebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = (
            "card_type",
            "card_token",
            "card_account_id",
            "card_holder_name",
            "card_masked_number",
            "card_expiration_date",
        )


class CloudPaymentsPaymentSerializer(serializers.ModelSerializer):
    reason_code = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    debit_card = CloudPaymentsDebitCardSerializer(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Payment
        fields = (
            "rrn",
            "status",
            "pa_req",
            "pa_res",
            "acs_url",
            "outer_id",
            "debit_card",
            "reason_code",
        )

    def register_debit_card(self, debit_card, payment):  # noqa
        if payment.debit_card is not None:
            return payment.debit_card

        if not payment.keep_card or debit_card is None or debit_card.get("card_token") is None:
            return

        debit_card_instance, created = DebitCard.objects.get_or_create(
            card_token=debit_card.pop("card_token"),
            user=payment.user,
            defaults=debit_card,
        )

        return debit_card_instance

    def update(self, instance, validated_data):
        status = validated_data.pop("status")
        status_reason = REASON_CODES.get(validated_data.get("reason_code"))
        validated_data["debit_card"] = self.register_debit_card(
            debit_card=validated_data.pop("debit_card"),
            payment=instance,
        )

        payment = super().update(instance, validated_data)
        payment.change_status(status, status_reason)

        return payment
