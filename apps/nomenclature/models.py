from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, UUIDModel


class Category(UUIDModel, AbstractNameModel):
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


class LocalCategory(UUIDModel, AbstractNameModel):
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
        related_name="categories",
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


class LocalPosition(UUIDModel, AbstractNameModel):
    class Meta:
        verbose_name = _("Позиция(Блюдо)")
        verbose_name_plural = _("Позиции(Блюда)")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        related_name="positions",
    )
    image = models.ImageField(
        null=True, blank=True
    )
    price = models.DecimalField(
        _("Цена"),
        max_digits=12,
        decimal_places=2,
        default=Decimal(0),
    )
    iiko_name = models.CharField(
        _("Название в системе IIKO"),
        max_length=256, null=True, blank=True,
    )
    iiko_description = models.TextField(
        _("Описание в системе IIKO"), null=True, blank=True,
    )
    local_category = models.ForeignKey(
        LocalCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="local_positions"
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


class BranchPosition(UUIDModel):
    class Meta:
        unique_together = ("local_position", "branch")

    local_position = models.ForeignKey(
        "nomenclature.LocalPosition",
        on_delete=models.CASCADE,
        related_name="positions_by_org",
    )
    branch_category = models.ForeignKey(
        BranchCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="branch_positions",
    )
    branch = models.ForeignKey(
        "partners.Branch",
        on_delete=models.CASCADE,
        related_name="positions",
    )
    price = models.DecimalField(
        _("Цена"),
        decimal_places=2,
        max_digits=12
    )