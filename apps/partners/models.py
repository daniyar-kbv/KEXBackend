from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel


class Organization(AbstractNameModel):
    class Meta:
        verbose_name = "Организация(бренд)"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class Merchant(AbstractNameModel):
    class Meta:
        verbose_name = "Мерчант (точка продажи)"
        verbose_name_plural = "Мерчанты"

    organization = models.ForeignKey(
        "partners.Organization",
        on_delete=models.PROTECT,
        related_name="merchants",
    )
    address = models.ForeignKey(
        "common.Address",
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name=_("Юр. адрес"),
    )


class MerchantRelationMixin(models.Model):
    merchant = models.ForeignKey(
        "partners.Merchant",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        abstract = True
