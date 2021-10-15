from typing import TYPE_CHECKING

from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _  # noqa

from apps.orders import OrderStatuses
from apps.partners import DeliveryTypes
from apps.payments import PaymentStatusTypes
from apps.orders.managers import OrdersManager
from apps.common.models import (
    TimestampModel,
    UUIDModel,
    ServiceHistoryModel,
)

if TYPE_CHECKING:
    from apps.partners.models import BranchDeliveryTime

User = get_user_model()


class Lead(
    TimestampModel,
    ServiceHistoryModel,
    UUIDModel
):
    class Meta:
        verbose_name = _("Лид")
        verbose_name_plural = _("Лиды")

    branch = models.ForeignKey(
        "partners.Branch",
        verbose_name=_("Организация"),
        on_delete=models.PROTECT,
        null=True,
        related_name="leads",
    )
    delivery_type = models.CharField(
        max_length=256,
        choices=DeliveryTypes.choices,
        null=True
    )
    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        verbose_name=_("Бренд"),
        on_delete=models.PROTECT,
        null=True,
        related_name="leads",
    )
    address = models.ForeignKey(
        "location.Address",
        verbose_name=_("Адресс"),
        on_delete=models.SET_NULL,
        null=True,
    )
    order_zone = models.CharField(
        _("Зона"),
        max_length=256,
        null=True,
    )
    estimated_duration = models.PositiveSmallIntegerField(
        _("Примерное время доставки"),
        null=True,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="leads",
        null=True, blank=True,
        verbose_name=_("Клиент"),
    )
    cart = models.OneToOneField(
        "orders.Cart",
        on_delete=models.PROTECT,
        related_name="lead",
        null=True, blank=True,
    )

    @atomic
    def drop_delivery(self):
        self.delivery_type = None
        self.cart.drop_delivery_position()
        self.save(update_fields=['delivery_type'])

    @atomic
    def update_delivery_params(self):
        actual_delivery: BranchDeliveryTime = self.branch.delivery_times.open().first()  # noqa

        if (actual_delivery and
            actual_delivery.delivery_type != self.delivery_type and
            actual_delivery.is_branch_position_exists
        ):
            self.cart.update_delivery_position(actual_delivery.branch_position)  # noqa
            self.delivery_type = actual_delivery.delivery_type
            self.save(update_fields=['delivery_type'])


class Order(
    TimestampModel,
    ServiceHistoryModel,
):
    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    lead = models.OneToOneField(
        "orders.Lead",
        to_field="uuid",
        related_name="order",
        verbose_name="Лид",
        null=True, blank=True,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("Клиент"),
    )
    branch = models.ForeignKey(
        "partners.Branch",
        verbose_name=_("Организация"),
        on_delete=models.PROTECT,
        null=True,
        related_name="orders",
    )
    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        verbose_name=_("Бренд"),
        on_delete=models.PROTECT,
        null=True,
        related_name="orders",
    )
    cart = models.OneToOneField(
        "orders.Cart",
        on_delete=models.PROTECT,
        related_name="order",
        null=True, blank=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )
    status = models.CharField(
        _("Статус"),
        max_length=32,
        choices=OrderStatuses.choices,
        default=OrderStatuses.NEW,
    )
    status_reason = models.TextField(
        _("Причина присвоения статуса"),
        null=True,
    )

    objects = OrdersManager()

    @atomic
    def change_status(self, status: str, status_reason: str = None):
        from apps.notifications.tasks import status_update_notifier

        if self.status == status:
            return

        self.status = status
        self.status_reason = status_reason
        self.save(update_fields=["status", "status_reason"])
        self.status_transitions.create(status=status, status_reason=status_reason)  # noqa

        if status in [
            OrderStatuses.COOKING_STARTED,
            OrderStatuses.COOKING_COMPLETED,
            OrderStatuses.WAITING,
            OrderStatuses.ON_WAY,
            OrderStatuses.DELIVERED,
        ]:
            status_update_notifier.delay(order_pk=self.pk)

    def mark_as_paid(self):
        from apps.pipeline.iiko.celery_tasks import order_apply_task

        order_apply_task.delay(order_pk=self.pk)
        self.change_status(status=OrderStatuses.PAID)

    def mark_as_apply_error(self):
        self.outer_id = None
        self.save(update_fields=['outer_id'])
        self.change_status(OrderStatuses.APPLY_ERROR, "Заказ не дошел до ресторона")

    @property
    def is_completed_payment_exists(self) -> bool:
        return self.payments.filter(status=PaymentStatusTypes.COMPLETED).exists()

    @property
    def completed_payment(self):
        if self.payments.filter(status=PaymentStatusTypes.COMPLETED).exists():
            return self.payments.get(status=PaymentStatusTypes.COMPLETED)


class OrderStatusTransition(TimestampModel):
    class Meta:
        verbose_name = _("Истории статусов заказа")
        verbose_name_plural = _("Истории статусов заказов")
        ordering = ("created_at",)

    status = models.CharField(
        _("Статус"),
        max_length=20,
        choices=OrderStatuses.choices,
        default=OrderStatuses.NEW
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="status_transitions",
        blank=True, null=True,
        verbose_name=_("Заказ"),
    )
    status_reason = models.TextField(_("Причина присвоения статуса"), null=True)
