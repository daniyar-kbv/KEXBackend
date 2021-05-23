from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel
from apps.partners.models import OrganizationRelationMixin


class Category(AbstractNameModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории позиции")

    iiko_brand = models.ForeignKey(  # noqa
        "partners.IIKOBrand",
        verbose_name=_("Бренд"),
        on_delete=models.PROTECT,
        null=True,
    )


class Position(models.Model):
    class Meta:
        verbose_name = _("Позиция(Блюдо)")
        verbose_name_plural = _("Позиции(Блюда)")

    organizations = models.ManyToManyField(
        "partners.Organization",
        related_name="positions",
        null=True
    )
    iiko_name = models.CharField(
        _("Название в системе IIKO"),
        max_length=256, null=True, blank=True,
    )
    iiko_description = models.TextField(
        _("Описание в системе IIKO"), null=True, blank=True,
    )
    price = models.DecimalField(
        _("Цена"),
        decimal_places=2,
        max_digits=12
    )
    category = models.ForeignKey(
        "nomenclature.Category",
        on_delete=models.PROTECT,
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
