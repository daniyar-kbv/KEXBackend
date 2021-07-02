from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel


class Cart(TimestampModel):
    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")


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


# class CartPositionModifierGroup(models.Model):
#     cart_position = models.ForeignKey(
#         CartPosition,
#         on_delete=models.CASCADE,
#         related_name="modifier_groups",
#         null=True,
#     )
#     modifier_group = models.ForeignKey(
#         "nomenclature.ModifierGroup",
#         ""
#     )


class CartPositionModifier(models.Model):
    cart_position = models.ForeignKey(
        CartPosition,
        on_delete=models.CASCADE,
        related_name="modifiers",
        null=True,
    )
    branch_position = models.ForeignKey(
        "nomenclature.BranchPosition",
        on_delete=models.CASCADE,
        related_name="carts",
        to_field="uuid",
        null=True,
    )
    count = models.PositiveSmallIntegerField(
        _("Количество"), default=1,
    )
