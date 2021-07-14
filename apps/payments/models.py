from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model

from apps.common.models import TimestampModel, UUIDModel

from . import CurrencyTypes, PaymentTypes, PaymentStatusTypes
from .managers import PaymentsManager

User = get_user_model()


class DebitCard(UUIDModel, TimestampModel):
    class Meta:
        ordering = ("created_at",)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="debit_cards",
    )
    card_holder_name = models.CharField(
        max_length=256,
    )
    card_masked_number = models.CharField(
        max_length=256,
        null=True,
    )
    card_expiration_date = models.CharField(
        max_length=256,
        null=True,
    )
    card_token = models.CharField(
        max_length=256,
        null=True,
    )
    card_type = models.CharField(
        max_length=256,
        null=True,
    )
    is_active = models.BooleanField(
        default=False,
    )


class Payment(TimestampModel):
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payments"
    )
    debit_card = models.ForeignKey(
        DebitCard,
        on_delete=models.PROTECT,
        null=True,
        related_name="payments",
    )
    status = models.CharField(
        max_length=256,
        choices=PaymentStatusTypes.choices,
        default=PaymentStatusTypes.NEW,
    )
    status_reason = models.TextField(null=True)
    payment_type = models.CharField(
        max_length=256,
        choices=PaymentTypes.choices,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    ip_address = models.CharField(
        max_length=256,
    )
    currency = models.CharField(
        max_length=256,
        choices=CurrencyTypes.choices,
        default=CurrencyTypes.KZT,
    )
    rrn = models.CharField(
        max_length=256,
        null=True
    )
    outer_id = models.CharField(
        max_length=512,
    )
    cryptogram = models.CharField(max_length=1024)

    objects = PaymentsManager()

    @property
    def is_completed(self):
        return self.status == PaymentStatusTypes.COMPLETED

    @atomic
    def change_status(self, status: str, status_reason: str = None):
        self.status = status
        self.status_reason = status_reason
        self.save(update_fields=["status", "status_reason"])
        self.status_transitions.create(status=status, status_reason=status_reason)  # noqa

    def mark_as_declined(self, status_reason: str):
        self.change_status(status=PaymentStatusTypes.DECLINED, status_reason=status_reason)

    def mark_as_completed(self):
        print("mark as completed is called")
        self.change_status(status=PaymentStatusTypes.COMPLETED)
        self.order.mark_as_paid()  # noqa

    def mark_as_cancelled(self):
        self.change_status(status=PaymentStatusTypes.CANCELLED)


class PaymentStatusTransition(TimestampModel):
    class Meta:
        ordering = ("created_at",)

    status = models.CharField(
        max_length=256,
        choices=PaymentStatusTypes.choices,
        default=PaymentStatusTypes.NEW,
    )
    order = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="status_transitions",

    )
    status_reason = models.TextField(null=True)
