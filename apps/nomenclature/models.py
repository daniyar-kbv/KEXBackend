from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, UUIDModel


class Category(UUIDModel, AbstractNameModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории позиции")

    iiko_brand = models.ForeignKey(  # noqa
        "partners.IIKOBrand",
        verbose_name=_("Бренд"),
        on_delete=models.PROTECT,
        null=True,
        related_name="categories",
    )


class Position(models.Model):
    class Meta:
        verbose_name = _("Позиция(Блюдо)")
        verbose_name_plural = _("Позиции(Блюда)")

    iiko_brand = models.ForeignKey(
        "partners.IIKOBrand",
        on_delete=models.PROTECT,
        related_name="positions",
    )
    iiko_name = models.CharField(
        _("Название в системе IIKO"),
        max_length=256, null=True, blank=True,
    )
    iiko_description = models.TextField(
        _("Описание в системе IIKO"), null=True, blank=True,
    )
    category = models.ForeignKey(
        "nomenclature.Category",
        on_delete=models.PROTECT,
        to_field="uuid",
        null=True, blank=True,
        related_name="positions",
        verbose_name=_("Категория"),
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )
    is_additional = models.BooleanField(
        _("Дополнительная позиция"),
        default=False,
    )

    def __str__(self):
        return self.iiko_name


class PositionInfoByOrganization(UUIDModel):
    class Meta:
        unique_together = ("position", "organization")

    position = models.ForeignKey(
        "nomenclature.Position",
        on_delete=models.CASCADE,
        related_name="positions_by_org",
    )
    organization = models.ForeignKey(
        "partners.Organization",
        on_delete=models.CASCADE,
        related_name="positions",
    )
    price = models.DecimalField(
        _("Цена"),
        decimal_places=2,
        max_digits=12
    )
