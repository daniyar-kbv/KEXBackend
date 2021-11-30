from uuid import uuid4
from datetime import time
from decimal import Decimal

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common import ImageTypes
from apps.common.models import (
    AbstractNameModel,
    ServiceHistoryModel,
    ImageModel
)

from . import DeliveryTypes, RequiredLocalBrandPaymentTypes
from .managers import (
    BranchDeliveryTimeQuerySet,
    LocalBrandManager,
    BranchManager,
)


class BrandImageMixin:
    @property
    def web_image_square(self):
        if self.images.for_web().filter(image_type=ImageTypes.IMAGE_SQUARE).exists():
            return self.images.for_web().filter(image_type=ImageTypes.IMAGE_SQUARE).first().image

    @property
    def web_image_short(self):
        if self.images.for_web().filter(image_type=ImageTypes.IMAGE_SHORT).exists():
            return self.images.for_web().filter(image_type=ImageTypes.IMAGE_SHORT).first().image

    @property
    def web_image_tall(self):
        if self.images.for_web().filter(image_type=ImageTypes.IMAGE_TALL).first():
            return self.images.for_web().filter(image_type=ImageTypes.IMAGE_TALL).first().image

    @property
    def web_image_long(self):
        if self.images.for_web().filter(image_type=ImageTypes.IMAGE_LONG).first():
            return self.images.for_web().filter(image_type=ImageTypes.IMAGE_LONG).first().image

    @property
    def mobile_image_square(self):
        if self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_SQUARE).exists():
            return self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_SQUARE).first().image

    @property
    def mobile_image_short(self):
        if self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_SHORT).exists():
            return self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_SHORT).first().image

    @property
    def mobile_image_tall(self):
        if self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_TALL).first():
            return self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_TALL).first().image

    @property
    def mobile_image_long(self):
        if self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_LONG).first():
            return self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_LONG).first().image


class Brand(BrandImageMixin, AbstractNameModel):
    class Meta:
        verbose_name = _("Брэнд")
        verbose_name_plural = _("Брэнды")

    priority = models.PositiveSmallIntegerField(
        _("Приоритетность"),
        default=1,
    )
    images = GenericRelation(ImageModel)
    kml_map = models.FileField(null=True, blank=True)


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

    @property
    def get_default_cancel_cause_uuid(self):
        if self.cancel_causes.filter(is_default=True).exists():
            return self.cancel_causes.filter(is_default=True).first().uuid

    @property
    def get_default_cancel_cause_name(self):
        if self.cancel_causes.filter(is_default=True).exists():
            return self.cancel_causes.filter(is_default=True).first().name

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

    objects = BranchManager()

    def __str__(self):
        return self.iiko_name


class LocalBrandPaymentType(models.Model):
    local_brand = models.ForeignKey(  # noqa
        "partners.LocalBrand",
        on_delete=models.CASCADE,
        related_name="payment_types",
    )
    uuid = models.UUIDField("Идентификатор", default=uuid4, editable=False)
    name = models.CharField(max_length=256, null=True)
    code = models.CharField(max_length=256, null=True)
    payment_type = models.CharField(
        max_length=26,
        choices=RequiredLocalBrandPaymentTypes.choices,
        null=True,
        blank=True,
    )


class LocalBrandCancelCause(models.Model):
    local_brand = models.ForeignKey(
        'partners.LocalBrand',
        on_delete=models.CASCADE,
        related_name='cancel_causes',
    )
    uuid = models.UUIDField('Идентификатор', null=True)
    name = models.CharField(max_length=1024, null=True)
    is_default = models.BooleanField(
        default=False,
    )


class BranchDeliveryTime(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='zones'
    )
    delivery_type = models.CharField(
        max_length=256,
        choices=DeliveryTypes.choices,
    )
    zone_name = models.CharField(
        max_length=256, editable=False
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
