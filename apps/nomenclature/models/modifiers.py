from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import UUIDModel
from apps.nomenclature.managers import PositionModifierGroupManager


class ModifierGroup(UUIDModel):
    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        related_name="modifier_groups",
        null=True,
    )
    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )


class PositionModifierGroup(UUIDModel):
    modifier_group = models.ForeignKey(
        ModifierGroup,
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
