from django.contrib import admin

from apps.nomenclature.admin import CategoryInline

from .models import Brand, IIKOBrand, Organization


admin.site.register(Brand)


@admin.register(IIKOBrand)
class IIKOBrandAdmin(admin.ModelAdmin):
    inlines = CategoryInline,
    list_filter = ('city',)
    fields = (
        'brand',
        'city',
        'full_name',
        'api_login',
        'is_active',
        'priority',
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ('iiko_brand',)
    fields = (
        'name',
        'outer_id',
        'iiko_brand',
        'address',
        'is_active',
        'start_time',
        'end_time',
    )
