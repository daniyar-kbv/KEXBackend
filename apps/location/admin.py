from django.contrib import admin

from .models import Country, City

from apps.partners.admin import LocalBrandPriorityInline
from apps.common.admin import AbstractNameModelForm


class CountryForm(AbstractNameModelForm):
    class Meta:
        model = Country
        exclude = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    form = CountryForm


class CityForm(AbstractNameModelForm):
    class Meta:
        model = City
        exclude = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    model = City
    inlines = LocalBrandPriorityInline,
    form = CityForm
