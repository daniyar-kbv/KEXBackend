from django.db import models

from apps.common.models import AbstractNameModel, AbstractTitleModel, AbstractDescriptionModel, MainModel
from apps.orders.models import Order
from django.utils.translation import gettext_lazy as _


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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="rates")
    comment = models.TextField("Комментарий", null=True, blank=True)
    rate_samples = models.ManyToManyField(RateSample, verbose_name="Шаблоны оценки", blank=True)

    def __str__(self):
        return f"Заказ#{self.order.id} - {self.star} звезд(ы)"

    class Meta:
        verbose_name = "Оценка заказа"
        verbose_name_plural = "Оценки заказов"
