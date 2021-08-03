from datetime import time

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, ServiceHistoryModel, MainModel

from . import BrandImageTypes
from .managers import LocalBrandManager, BranchesQuerySet


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
        unique_together = ("brand", "image_type")

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
    image = models.ImageField(_("Image"), null=True)


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
        _("Активна"), default=False
    )

    objects = LocalBrandManager()

    def deactivate_branches(self):  # noqa
        for branch in self.branches.all():  # noqa
            branch.is_active = False
            branch.save(update_fields=["is_active"])

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
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )
    is_active = models.BooleanField(
        _("Активна"), default=False
    )

    start_time = models.TimeField(_("Время работы с"), default=time(10, 0))
    end_time = models.TimeField(_("Время работы до"), default=time(22, 0))

    objects = BranchesQuerySet.as_manager()

    def __str__(self):
        return self.iiko_name
