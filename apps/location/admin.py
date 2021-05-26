from django.contrib import admin

from apps.partners.models import IIKOBrand

from .models import Country, City
from ..common.admin import AbstractNameModelForm


class IIKOBrandInline(admin.TabularInline):
    model = IIKOBrand
    readonly_fields = "brand_name",
    fields = (
        "brand_name",
        "priority",
    )

    def brand_name(self, obj):
        return obj.brand.name

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class CountryForm(AbstractNameModelForm):
    class Meta(AbstractNameModelForm.Meta):
        model = Country


class CityForm(AbstractNameModelForm):
    class Meta(AbstractNameModelForm.Meta):
        model = City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name',)
    search_fields = ('name__text_ru',)
    form = CountryForm
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'id',
                'name_ru',
                'name_kk',
                'name_en',
                'country_code',
            )
        }),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    model = City
    inlines = IIKOBrandInline,
    form = CityForm
    list_display = ('name',)
    search_fields = ('name__text_ru',)

