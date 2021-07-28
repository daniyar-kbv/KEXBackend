from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import (
    TimestampModel,
    UUIDModel,
    ServiceHistoryModel,
    MainModel,
    AbstractNameModel,
    AbstractDescriptionModel,
    AbstractTitleModel,
)

from apps.orders import OrderStatuses
from apps.orders.managers import OrdersManager
from apps.payments import PaymentStatusTypes
from apps.translations.models import MultiLanguageChar, MultiLanguageText

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
    cart = models.OneToOneField(
        "orders.Cart",
        on_delete=models.PROTECT,
        related_name="order",
        null=True, blank=True,
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
        self.status = status
        self.status_reason = status_reason
        self.save(update_fields=["status", "status_reason"])
        self.status_transitions.create(status=status, status_reason=status_reason)  # noqa

    def mark_as_paid(self):
        self.change_status(status=OrderStatuses.PAID)

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


class RateSample(AbstractNameModel):
    class Meta:
        verbose_name = "Шаблон оценки"
        verbose_name_plural = "Шаблоны оценки"


class RateStar(
    AbstractTitleModel,
    AbstractDescriptionModel
):
    value = models.PositiveSmallIntegerField(_("Значение"), default=1)
    rate_samples = models.ManyToManyField(RateSample, verbose_name="Шаблоны оценки", blank=True)

    def __str__(self):
        return f"{self.value} звезд(ы)"

    class Meta:
        verbose_name = "Звезда оценки"
        verbose_name_plural = "Звезды оценки"
        ordering = ['value']


class RatedOrder(MainModel):
    star = models.ForeignKey(RateStar, on_delete=models.CASCADE, verbose_name="Звезда")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="rates")
    comment = models.TextField("Комментарий", null=True, blank=True)
    rate_samples = models.ManyToManyField(RateSample, verbose_name="Шаблоны оценки", blank=True)

    def __str__(self):
        return f"Заказ#{self.order.id} - {self.star} звезд(ы)"

    class Meta:
        verbose_name = "Оценка заказа"
        verbose_name_plural = "Оценки заказов"


class CouponGroup(MainModel):
    name = models.CharField("Название серии", max_length=255)

    class Meta:
        verbose_name = "Серия купона"
        verbose_name_plural = "Серии Купонов"

    def __str__(self):
        return self.name


class Coupon(AbstractDescriptionModel):
    group = models.ForeignKey(CouponGroup, verbose_name="Серия", on_delete=models.PROTECT)
    promocode = models.CharField(max_length=255, verbose_name="Код")
    start_date = models.DateField("Период действи с ", default=timezone.now)
    end_date = models.DateField("Период действи по ", default=timezone.now)

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"

    def __str__(self):
        return f"{self.promocode}[{self.group}]"

    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date
