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


class Country(AbstractNameModel):
    ...


class City(AbstractNameModel):
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.SET_NULL,
        null=True,
        related_name="cities",
        verbose_name=_("Страна")
    )

    @property
    def country_name(self):
        if self.country is None:
            return self.country.name

    def __str__(self):
        return f"{self.name}({self.country_name})"
