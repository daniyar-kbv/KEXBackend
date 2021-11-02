from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model

from apps.common.models import TimestampModel, UUIDModel, ServiceHistoryModel

from . import CurrencyTypes, PaymentTypes, PaymentStatusTypes
from .managers import PaymentsManager, DebitCardsManager

User = get_user_model()


class DebitCard(UUIDModel, TimestampModel):
    class Meta:
        ordering = ("-updated_at",)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="debit_cards",
    )
    card_holder_name = models.CharField(
        max_length=256,
        null=True,
    )
    card_account_id = models.CharField(
        max_length=1024,
        null=True,
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

    objects = DebitCardsManager()

    def delete(self, using=None, keep_parents=False):
        self.card_token = None
        self.save(update_fields=["card_token"])


class Payment(TimestampModel, ServiceHistoryModel, UUIDModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payments"
    )
    debit_card = models.ForeignKey(
        DebitCard,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        to_field="uuid",
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
        default=PaymentTypes.DEBIT_CARD,
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
    cryptogram = models.CharField(max_length=4096, null=True)

    keep_card = models.BooleanField(
        default=False
    )
    card_holder_name = models.CharField(
        max_length=256,
        null=True,
        blank = True
    )

    pa_req = models.CharField(max_length=1024, null=True)
    pa_res = models.CharField(max_length=1024, null=True)
    acs_url = models.URLField(max_length=512, null=True)

    objects = PaymentsManager()

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    @property
    def is_completed(self):
        return self.status == PaymentStatusTypes.COMPLETED

    @atomic
    def change_status(self, status: str, status_reason: str = None):
        if self.status == status:
            return

        self.status = status

        if self.status == PaymentStatusTypes.COMPLETED:
            self.order.mark_as_paid()  # noqa

        self.status_reason = status_reason
        self.save(update_fields=["status", "status_reason"])
        self.status_transitions.create(status=status, status_reason=status_reason)  # noqa


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
