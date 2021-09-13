from uuid import UUID
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, UUIDModel
from apps.nomenclature.managers import CategoryManager

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand


class Category(UUIDModel, AbstractNameModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
        related_name="categories",
        verbose_name=_("Локальный бренд"),
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
