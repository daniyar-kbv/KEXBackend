from django.db import models
from django.utils import timezone

from apps.common.models import (
    MainModel,
    AbstractDescriptionModel,
)


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
