from django.contrib import admin

from apps.nomenclature.admin import CategoryInline

from .models import Brand, IIKOBrand, Organization


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        print(formfield)
        formfield.widget.can_delete_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield


@admin.register(IIKOBrand)
class IIKOBrandAdmin(admin.ModelAdmin):
    inlines = CategoryInline,
    list_filter = ('city',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ('iiko_brand',)
