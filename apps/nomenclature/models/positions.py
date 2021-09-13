from decimal import Decimal
from typing import TYPE_CHECKING, List

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.nomenclature.managers import BranchPositionManager
from apps.common.models import (
    AbstractDescriptionModel,
    AbstractNameModel,
    UUIDModel,
)

if TYPE_CHECKING:
    from apps.partners.models import Branch
    from apps.nomenclature.models import (
        ModifierGroup,
        PositionModifierGroup,
        PositionModifier,
    )


class PositionTypes(models.TextChoices):
    MAIN = "MAIN", "Основное блюдо"
    MODIFIER = "MODIFIER", "Модификатор"
    ADDITIONAL = "ADDITIONAL", "Дополнительное блюдо"
    DAY_DELIVERY = "DAY_DELIVERY", "Дневная доставка"
    NIGHT_DELIVERY = "NIGHT_DELIVERY", "Ночная доставка"


class Position(AbstractNameModel, AbstractDescriptionModel):
    class Meta:
        verbose_name = _("Позиция(Блюдо)")
        verbose_name_plural = _("Позиции(Блюда)")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        related_name="positions",
    )
    priority = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "nomenclature.Category",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="positions"
    )
    image = models.ImageField(
        null=True, blank=True
    )
    position_type = models.CharField(
        max_length=256,
        choices=PositionTypes.choices,
        default=PositionTypes.MAIN,
        db_index=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )
    is_active = models.BooleanField(
        _("Активен в системе mti"),
        default=True,
    )


class BranchPosition(UUIDModel):
    class Meta:
        unique_together = ("position", "branch")
        ordering = ('position__priority',)

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
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
    is_active = models.BooleanField(
        _("Активен в системе mti"),
        default=True,
    )
    is_available = models.BooleanField(
        _("Не доступен в системе IIKO"),
        default=True,
        help_text=_("Если отключен, то продукт отобразится как не доступный в приложении")
    )

    objects = BranchPositionManager()

    @property
    def name(self):
        return self.position.name

    @property
    def description(self):
        return self.position.description

    @property
    def image(self):
        return self.position.image

    @property
    def position_type(self):
        return self.position.position_type

    @property
    def outer_id(self):
        return self.position.outer_id

    @classmethod
    def register_branch_position(cls, branch: 'Branch', position: Position, modifier_groups: List['ModifierGroup'] = None):
        from apps.nomenclature.models import ModifierGroup, PositionModifierGroup, PositionModifier

        branch_position, created = cls.objects.update_or_create(
            branch=branch,
            position=position,
        )
        for modifier_group in modifier_groups:
            position_modifier_group, _ = PositionModifierGroup.objects.update_or_create(
                branch_position=branch_position,
                modifier_group=ModifierGroup.objects.get(
                    outer_id=modifier_group["outer_id"]
                ),
                defaults={
                    "is_required": modifier_group["is_required"],
                    "min_amount": modifier_group["min_amount"],
                    "max_amount": modifier_group["max_amount"],
                }
            )

            for modifier in modifier_group["modifiers"] or list():
                PositionModifier.objects.update_or_create(
                    modifier=cls.objects.get(
                        position__outer_id=modifier["outer_id"],
                        branch=branch,
                    ),
                    position_modifier_group=position_modifier_group,
                )

        return branch_position
