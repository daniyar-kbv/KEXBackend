from django.contrib import admin

from apps.partners.models import IIKOBrand

from .models import Country, City


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


class CityAdmin(admin.ModelAdmin):
    model = City
    inlines = IIKOBrandInline,


admin.site.register(Country)
admin.site.register(City, CityAdmin)
