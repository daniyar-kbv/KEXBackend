from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from apps.common.models import TimestampModel
from apps.partners.models import MerchantRelationMixin

from . import OrderStatuses


class Order(MerchantRelationMixin, TimestampModel):
    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("Клиент"),
    )
    status = models.CharField(
        _("Статус"),
        max_length=32,
        choices=OrderStatuses.choices,
        default=OrderStatuses.NEW,
    )
    status_reason = models.TextField(
        _("Причина присвоения статуса")
    )


class Cart(TimestampModel):
    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name=_("Заказ"),
    )


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
    status_reason = models.TextField(_("Причина присвоения статуса"))
