from typing import TYPE_CHECKING
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel
from apps.orders.managers import CartPositionQueryset
from apps.partners import DeliveryTypes

if TYPE_CHECKING:
    from apps.nomenclature.models import BranchPosition


class Cart(TimestampModel):
    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")

    def get_count_for_given_position(self, position_uuid: str) -> int:
        if self.positions.filter(branch_position_id=position_uuid).exists():
            return self.positions.get(branch_position_id=position_uuid).count

        return 0

    def drop_delivery_position(self):
        self.positions.filter(
            branch_position__position__position_type__in=[
                DeliveryTypes.DAY_DELIVERY,
                DeliveryTypes.NIGHT_DELIVERY
            ]
        ).delete()

    def update_delivery_position(self, delivery_position: 'BranchPosition'):
        print('CART (update_delivery_position) is called')
        self.drop_delivery_position()
        self.positions.create(branch_position=delivery_position)

    @property
    def positions_count(self) -> int:
        return self.positions.exclude_delivery().aggregate(Sum('count'))['count__sum'] or 0

    @property
    def delivery_price(self) -> Decimal:
        if self.positions.only_delivery().exists():
            return self.positions.only_delivery().first().price
        return Decimal('0.00')

    @property
    def positions_price(self) -> Decimal:
        if self.positions.exclude_delivery().exists():
            return sum(
                [position.price for position in self.positions.exclude_delivery()]
            )
        return Decimal('0.00')

    @property
    def total_price(self) -> Decimal:
        if self.positions.exists():
            return sum(
                [position.price for position in self.positions.all()]
            )
        return Decimal('0.00')

    @property
    def has_unavailable_positions(self):
        return self.positions\
            .filter(branch_position__is_available=False)\
            .exists()


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
        modifiers_price = sum([modifier.count * modifier.branch_position.price for modifier in self.modifiers.all()])
        return (self.branch_position.price * self.count) + modifiers_price


class CartPositionModifier(models.Model):
    cart_position = models.ForeignKey(
        CartPosition,
        on_delete=models.CASCADE,
        related_name="modifiers",
        null=True,
    )
    position_modifier_group = models.ForeignKey(
        "nomenclature.PositionModifierGroup",
        on_delete=models.CASCADE,
        to_field="uuid",
        null=True
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
