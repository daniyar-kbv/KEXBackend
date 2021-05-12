from django.contrib import admin

from .models import Brand, IIKOBrand, Organization


admin.site.register(Brand)
# admin.site.register(Organization)


@admin.register(IIKOBrand)
class IIKOBrandAdmin(admin.ModelAdmin):
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
class IIKOBrandAdmin(admin.ModelAdmin):

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
