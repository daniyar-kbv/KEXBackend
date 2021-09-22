from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel
from apps.orders.managers import CartPositionQueryset


class Cart(TimestampModel):
    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")

    def get_count_for_given_position(self, position_uuid: str) -> int:
        if self.positions.filter(branch_position_id=position_uuid).exists():
            return self.positions.get(branch_position_id=position_uuid).count

        return 0

    @property
    def positions_count(self) -> int:
        # return self.positions.exclude_delivery().count()
        return self.positions.exclude_delivery().aggregate(Sum('count'))['count__sum']

    @property
    def delivery_price(self) -> Decimal:
        if self.positions.only_delivery().exists():
            return self.positions.only_delivery().first().price

        return Decimal('0.00')

    @property
    def price(self) -> Decimal:
        if self.positions.exclude_delivery().exists():
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

    objects = CartPositionQueryset.as_manager()

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
