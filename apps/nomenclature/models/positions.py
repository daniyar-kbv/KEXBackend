from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import (
    AbstractDescriptionModel,
    AbstractNameModel,
    UUIDModel,
)

# class Position(UUIDModel, AbstractNameModel):
#     """
#     reserved
#     """
#     ...


class LocalPosition(AbstractNameModel, AbstractDescriptionModel):
    class Meta:
        verbose_name = _("Позиция(Блюдо)")
        verbose_name_plural = _("Позиции(Блюда)")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        related_name="local_positions",
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
    local_category = models.ForeignKey(
        "nomenclature.LocalCategory",
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
    is_active = models.BooleanField(
        _("Временно отключен"),
        default=True,
        help_text=_("Если отключен, то продукт не отобразится в приложении")
    )
    is_available = models.BooleanField(
        _("В данный момент не доступен"),
        default=True,
        help_text=_("Если отключен, то продукт отобразится как не доступный в приложении")
    )


class BranchPosition(UUIDModel, AbstractNameModel, AbstractDescriptionModel):
    class Meta:
        unique_together = ("local_position", "branch")

    local_position = models.ForeignKey(
        "nomenclature.LocalPosition",
        on_delete=models.CASCADE,
        related_name="branch_positions",
    )
    iiko_name = models.CharField(
        _("Название в системе IIKO"),
        max_length=256, null=True, blank=True,
    )
    iiko_description = models.TextField(
        _("Описание в системе IIKO"), null=True, blank=True,
    )
    branch_category = models.ForeignKey(
        "nomenclature.BranchCategory",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        to_field="uuid",
        related_name="branch_positions",
    )
    branch = models.ForeignKey(
        "partners.Branch",
        on_delete=models.CASCADE,
        related_name="branch_positions",
    )
    price = models.DecimalField(
        _("Цена"),
        decimal_places=2,
        max_digits=12,
        default=Decimal(0),
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )
    is_available = models.BooleanField(
        _("В данный момент не доступен"),
        default=True,
        help_text=_("Если отключен, то продукт отобразится как не доступный в приложении")
    )


class BranchPositionModifier(models.Model):
    class Meta:
        verbose_name = _("Modifier")
        verbose_name_plural = _("Modifiers")
        unique_together = ("main_position", "modifier")

    main_position = models.ForeignKey(
        BranchPosition,
        on_delete=models.PROTECT,
        to_field="uuid", null=True,
        related_name="modifiers",
    )
    modifier = models.ForeignKey(
        BranchPosition,
        on_delete=models.PROTECT,
        to_field="uuid", null=True,
    )
    min_amount = models.PositiveSmallIntegerField(default=1)
    max_amount = models.PositiveSmallIntegerField(default=1)
    is_required = models.BooleanField(default=False)
