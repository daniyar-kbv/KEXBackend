from uuid import UUID
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.utils import create_multi_language_char
from apps.common.models import UUIDModel, AbstractNameModel
from apps.nomenclature.managers import PositionModifierGroupManager

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand


class ModifierGroup(UUIDModel, AbstractNameModel):
    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        related_name="modifier_groups",
        null=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )

    @classmethod
    def register_modifier_group(cls, local_brand: 'LocalBrand', outer_id: UUID, iiko_name: str):
        modifier_group, created = cls.objects.get_or_create(
            outer_id=outer_id,
            local_brand=local_brand,
        )

        if modifier_group.name is None:
            modifier_group.name = create_multi_language_char(iiko_name)

        modifier_group.save(update_fields=["name"])

        return modifier_group


class PositionModifierGroup(models.Model):
    modifier_group = models.ForeignKey(
        ModifierGroup,
        to_field="uuid",
        null=True,
        on_delete=models.CASCADE,
        related_name="position_modifier_groups",
    )
    branch_position = models.ForeignKey(
        "nomenclature.BranchPosition",
        on_delete=models.CASCADE,
        related_name="position_modifier_groups",
    )
    min_amount = models.PositiveSmallIntegerField(
        default=0
    )
    max_amount = models.PositiveSmallIntegerField(
        default=0
    )
    is_required = models.BooleanField(
        default=False,
    )

    objects = PositionModifierGroupManager()

    @property
    def name(self):
        return self.modifier_group.name


class PositionModifier(models.Model):
    class Meta:
        verbose_name = _("Modifier")
        verbose_name_plural = _("Modifiers")
        unique_together = ("modifier", "position_modifier_group")

    modifier = models.ForeignKey(
        "nomenclature.BranchPosition",
        on_delete=models.PROTECT,
        to_field="uuid", null=True,
    )
    position_modifier_group = models.ForeignKey(
        PositionModifierGroup,
        on_delete=models.SET_NULL,
        related_name="modifiers",
        null=True,
    )
