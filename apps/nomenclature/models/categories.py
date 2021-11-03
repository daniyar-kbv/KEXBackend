from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import UUIDModel
from apps.nomenclature.managers import CategoryManager


class Category(UUIDModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ('priority',)

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
        related_name="categories",
        verbose_name=_("Локальный бренд"),
    )
    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    priority = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )

    objects = CategoryManager()
