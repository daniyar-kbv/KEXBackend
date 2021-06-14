from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel, UUIDModel


class Cart(UUIDModel, TimestampModel):
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
        to_field="uuid",
        related_name="positions",
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

    def increment_count(self):
        self.count += 1
        self.save(update_fields=["count"])

    def decrement_count(self):
        self.count -= 1
        if self.count < 0:
            self.count = 0

        self.save(update_fields=["count"])


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
