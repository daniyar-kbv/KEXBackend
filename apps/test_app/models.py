from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User

from . import OrderStatuses


class CharIDModel(models.Model):
    id = models.CharField("Уникальный код", max_length=16, primary_key=True)

    class Meta:
        abstract = True


class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        "Время создания", auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        "Время последнего изменения", auto_now=True, db_index=True
    )

    class Meta:
        abstract = True

    @property
    def created_at_pretty(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")  # noqa

    @property
    def updated_at_pretty(self):
        return self.updated_at.strftime("%d/%m/%Y %H:%M:%S")  # noqa


class Address(models.Model):
    country = models.CharField(_("Страна"), max_length=255, null=True, blank=True)
    region = models.CharField(_("Регион"), max_length=255, null=True, blank=True)
    city = models.CharField(_("Город"), max_length=255, null=True, blank=True)
    district = models.CharField(_("Район"), max_length=255, null=True, blank=True)
    street = models.CharField(_("Улица"), max_length=255, null=True, blank=True)
    building = models.CharField(_("Дом / здание"), max_length=100, null=True, blank=True)
    corpus = models.CharField(_("Корпус"), max_length=100, null=True, blank=True)
    flat = models.CharField(_("Квартира"), max_length=50, null=True, blank=True)
    postal_code = models.CharField(_("Почтовый индекс"), max_length=7, null=True, blank=True)


class Organization(models.Model):
    name = models.CharField(max_length=256)


class Merchant(models.Model):
    name = models.CharField(max_length=256)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="merchants",
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Юр. адрес"),
    )


class MerchantMixin(models.Model):
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        abstract = True


class Category(MerchantMixin):
    name = models.CharField(max_length=256)


class Position(MerchantMixin):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="positions",
    )
    is_additional = models.BooleanField(default=False)


class Combo(MerchantMixin):
    name = models.CharField(max_length=256)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    positions = models.ManyToManyField(Position)


class Order(TimestampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    status = models.CharField(
        max_length=32,
        choices=OrderStatuses.choices,
        default=OrderStatuses.NEW,
    )
    status_reason = models.TextField()


class Cart(TimestampModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="cart"
    )


class OrderStatusTransition(TimestampModel):
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=OrderStatuses.choices,
        default=OrderStatuses.NEW
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_transitions",
        blank=True,
        null=True
    )
    status_reason = models.TextField()

    class Meta:
        ordering = ("created_at",)
