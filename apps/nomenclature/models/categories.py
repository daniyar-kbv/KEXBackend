from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, UUIDModel


class Category(AbstractNameModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    brand = models.ForeignKey(  # noqa
        "partners.Brand",
        verbose_name=_("Бренд"),
        on_delete=models.PROTECT,
        null=True,
        related_name="categories",
    )
    is_active = models.BooleanField(
        default=False
    )


class LocalCategory(AbstractNameModel):
    class Meta:
        verbose_name = _("Локальная категория")
        verbose_name_plural = _("Локальные категории")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
        related_name="local_categories",
        verbose_name=_("Локальный бренд"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Категория")
    )
    is_active = models.BooleanField(
        default=True,
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
    local_category = models.ForeignKey(
        LocalCategory,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Локальная категория"),
    )
    is_active = models.BooleanField(
        default=True
    )
