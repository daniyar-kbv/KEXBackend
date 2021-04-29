from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel, ServiceHistoryModel


class Brand(AbstractNameModel):
    class Meta:
        verbose_name = _("Брэнд")
        verbose_name_plural = _("Брэнды")


class IIKOBrand(ServiceHistoryModel):
    class Meta:
        unique_together = "brand", "city"
        verbose_name = _("IIKO Брэнд")
        verbose_name_plural = _("IIKO Брэнды")

    brand = models.ForeignKey(
        "partners.Brand",
        on_delete=models.CASCADE,
        related_name="api_logins",
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

    @property
    def cache_mask(self):
        return f"{self.brand.name}_{self.api_login}".replace(" ", "_").upper()

    def __str__(self):
        return f"{self.brand}. {self.city}"


class Organization(AbstractNameModel):
    class Meta:
        verbose_name = _("Организация")
        verbose_name_plural = _("Организации")

    iiko_brand = models.ForeignKey(  # noqa
        "partners.IIKOBrand",
        on_delete=models.PROTECT,
        related_name="merchants",
        null=True,
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


class OrganizationRelationMixin(models.Model):
    merchant = models.ForeignKey(
        "partners.Organization",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        abstract = True
