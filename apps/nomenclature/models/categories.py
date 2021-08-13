from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, UUIDModel


class Category(AbstractNameModel):
    class Meta:
        verbose_name = _("Локальная категория")
        verbose_name_plural = _("Локальные категории")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
        related_name="categories",
        verbose_name=_("Локальный бренд"),
    )
    is_active = models.BooleanField(
        default=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )


class BranchCategory(UUIDModel, AbstractNameModel):
    class Meta:
        verbose_name = _("Категория филиала")
        verbose_name_plural = _("Категории филиалов")

    branch = models.ForeignKey(
        "partners.Branch",
        on_delete=models.PROTECT,
        null=True,
        related_name="branch_categories",
        verbose_name=_("Филиал"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Локальная категория"),
        related_name="branch_categories",
    )
    is_active = models.BooleanField(
        default=True
    )
