from django.contrib import admin

from .models import Country, City

from apps.partners.admin import LocalBrandPriorityInline
from apps.common.admin import AbstractNameModelForm


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ...


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    model = City
    inlines = LocalBrandPriorityInline,
    form = AbstractNameModelForm
