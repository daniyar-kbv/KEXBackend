from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel, UUIDModel, ServiceHistoryModel

from . import OrderStatuses
from .managers import OrdersManager


class Cart(UUIDModel, TimestampModel):
    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")


class CartPosition(TimestampModel):
    class Meta:
        verbose_name = _("Товар корзины")
        verbose_name_plural = _("Товары корзины")

    cart = models.ForeignKey(
        "orders.Cart",
        on_delete=models.CASCADE,
        related_name="cart_positions",
    )
    organization_position = models.ForeignKey(
        "nomenclature.PositionInfoByOrganization",
        on_delete=models.CASCADE,
        related_name="carts",
        to_field="uuid",
    )
    count = models.PositiveSmallIntegerField(
        _("Количество"), default=1,
    )
    comment = models.TextField(
        _("Комментарий к заказу"),
        null=True, blank=True,
    )

    def increment_count(self):
        self.count += 1
        self.save(update_fields=["count"])

    def decrement_count(self):
        self.count -= 1
        if self.count < 0:
            self.count = 0

        self.save(update_fields=["count"])


class Lead(
    TimestampModel,
    ServiceHistoryModel,
    UUIDModel
):
    class Meta:
        verbose_name = _("Лид")
        verbose_name_plural = _("Лиды")

    organization = models.ForeignKey(
        "partners.Organization",
        verbose_name=_("Организация"),
        on_delete=models.PROTECT,
        null=True,
        related_name="leads",
    )
    iiko_brand = models.ForeignKey(
        "partners.IIKOBrand",
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

    cart = models.ForeignKey(
        "orders.Cart",
        on_delete=models.PROTECT,
        related_name="leads",
        null=True, blank=True,
    )


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
        null=True, blank=True,
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

    objects = OrdersManager()


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
