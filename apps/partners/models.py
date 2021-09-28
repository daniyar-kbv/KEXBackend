from datetime import time
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, ServiceHistoryModel, MainModel

from . import BrandImageTypes, DeliveryTypes, PlatformTypes
from .managers import LocalBrandManager, BranchesQuerySet, BranchDeliveryTimeQuerySet, BrandImageQuerySet


class Brand(AbstractNameModel):
    class Meta:
        verbose_name = _("Брэнд")
        verbose_name_plural = _("Брэнды")

    priority = models.PositiveSmallIntegerField(
        _("Приоритетность"),
        default=1,
    )


class BrandImage(MainModel):
    class Meta:
        verbose_name = _("Brand Image")
        verbose_name_plural = _("Brand Images")
        unique_together = ("brand", "image_type", "size")

    brand = models.ForeignKey(
        "partners.Brand",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Брэнд"),
    )
    image_type = models.CharField(
        _("Тип картинки"),
        max_length=12,
        choices=BrandImageTypes.choices,
        null=True
    )
    size = models.CharField(_("Размер"), choices=PlatformTypes.choices, default=PlatformTypes.MOBILE, max_length=10)
    image = models.ImageField(_("Image"), null=True)

    objects = BrandImageQuerySet.as_manager()


class LocalBrand(ServiceHistoryModel):
    class Meta:
        unique_together = "brand", "city"
        verbose_name = _("Локальный Брэнд")
        verbose_name_plural = _("Локальные Брэнды")

    brand = models.ForeignKey(
        "partners.Brand",
        on_delete=models.CASCADE,
        related_name="local_brands",
        verbose_name=_("Брэнд"),
    )
    full_name = models.CharField(
        _("Полное название"),
        max_length=256,
        null=True,
    )
    city = models.ForeignKey(
        "location.City",
        on_delete=models.CASCADE,
        related_name="api_logins",
        verbose_name=_("Город"),
    )
    api_login = models.CharField(
        _("API-логин"),
        unique=True,
        max_length=255,
    )
    is_active = models.BooleanField(
        _("Активна в системе mti"), default=False
    )

    objects = LocalBrandManager()

    def deactivate_branches(self):  # noqa
        for branch in self.branches.all():  # noqa
            branch.is_active = False
            branch.save(update_fields=["is_active"])

    @property
    def name(self):
        return self.brand.name

    @property
    def cache_mask(self):
        return f"{self.brand.name}_{self.api_login}".replace(" ", "_").upper()

    def __str__(self):
        return f"{self.brand}. {self.city}"


class Branch(AbstractNameModel):
    class Meta:
        verbose_name = _("Ветка (Филиал)")
        verbose_name_plural = _("Ветки (Филиалы)")

    local_brand = models.ForeignKey(  # noqa
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        related_name="branches",
        null=True,
    )
    iiko_name = models.CharField(
        max_length=512,
        null=True
    )
    address = models.ForeignKey(
        "location.Address",
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name=_("Юр. адрес"),
    )
    min_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("1000")
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )
    terminal_id = models.UUIDField(
        _("TerminalUUID в системе IIKO"), null=True,
    )
    is_active = models.BooleanField(
        _("Активна в системе mti"), default=False
    )
    is_alive = models.BooleanField(
        _("Доступен в системе IIKO"), default=False
    )

    objects = BranchesQuerySet.as_manager()

    def __str__(self):
        return self.iiko_name


class BranchDeliveryTime(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='delivery_times'
    )
    delivery_type = models.CharField(
        max_length=256,
        choices=DeliveryTypes.choices,
    )
    start_time = models.TimeField(_("Время работы с"), default=time(10, 0))
    end_time = models.TimeField(_("Время работы до"), default=time(22, 0))

    objects = BranchDeliveryTimeQuerySet.as_manager()

    @property
    def is_branch_position_exists(self):
        return self.branch.branch_positions\
            .filter(position__position_type=self.delivery_type)\
            .exists()

    @property
    def branch_position(self):
        return self.branch.branch_positions\
            .filter(position__position_type=self.delivery_type)\
            .first()
