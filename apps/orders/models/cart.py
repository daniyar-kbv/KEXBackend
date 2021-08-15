from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel


class Cart(TimestampModel):
    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")

    @property
    def positions_count(self):
        return self.positions.count()

    @property
    def price(self) -> Decimal:
        if self.positions.exists():
            return sum(
                [position.price for position in self.positions.all()]
            )

        return Decimal('0.00')


class CartPosition(models.Model):
    class Meta:
        verbose_name = _("Товар корзины")
        verbose_name_plural = _("Товары корзины")

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="positions",
        null=True,
    )
    branch_position = models.ForeignKey(
        "nomenclature.BranchPosition",
        on_delete=models.CASCADE,
        related_name="positions",
        to_field="uuid",
        null=True,
    )
    count = models.PositiveSmallIntegerField(
        _("Количество"), default=1,
    )
    comment = models.TextField(
        _("Комментарий к заказу"),
        null=True, blank=True,
    )

    @property
    def price(self):
        return self.branch_position.price * self.count


class CartPositionModifierGroup(models.Model):
    cart_position = models.ForeignKey(
        CartPosition,
        on_delete=models.CASCADE,
        related_name="position_modifier_groups",
        null=True,
    )
    position_modifier_group = models.ForeignKey(
        "nomenclature.PositionModifierGroup",
        on_delete=models.CASCADE,
        to_field="uuid",
    )


class CartPositionModifier(models.Model):
    cart_position_modifier_group = models.ForeignKey(
        CartPositionModifierGroup,
        on_delete=models.CASCADE,
        related_name="modifiers",
        null=True,
    )
    branch_position = models.ForeignKey(
        "nomenclature.BranchPosition",
        on_delete=models.CASCADE,
        to_field="uuid",
        null=True,
    )
    count = models.PositiveSmallIntegerField(
        _("Количество"), default=1,
    )
