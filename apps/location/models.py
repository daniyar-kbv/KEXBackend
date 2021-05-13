from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel


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

    longitude = models.DecimalField(_("Долгота"), max_digits=12, decimal_places=8, null=True)
    latitude = models.DecimalField(_("Широта"), max_digits=12, decimal_places=8, null=True)

    def __str__(self):
        if self.street:
            return f"{str(self.street)} {str(self.building or '')}"
        return f"Address #{self.id}"


class Country(AbstractNameModel):
    class Meta:
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")

    country_code = models.CharField(
        _("Код страны"),
        max_length=32,
        null=True, blank=True,
    )


class City(AbstractNameModel):
    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")
        unique_together = ("country", "name")

    country = models.ForeignKey(
        "location.Country",
        on_delete=models.SET_NULL,
        null=True,
        related_name="cities",
        verbose_name=_("Страна")
    )

    @property
    def country_name(self):
        if self.country is not None:
            return self.country.name

    def __str__(self):
        return f"{self.name}({self.country_name})"
