from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

from apps.common.admin import ReadOnlyMixin
from apps.nomenclature.admin import CategoryInline, LocalCategoryInline

from .models import Brand, LocalBrand, Branch


class BranchInline(admin.TabularInline):
    model = Branch
    extra = 0
    classes = ("collapse",)
    fields = (
        "get_branch_link",
        "is_active",
    )
    readonly_fields = (
        "get_branch_link",
        "is_active",
    )

    def get_branch_link(self, obj):
        link = reverse("admin:partners_branch_change", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">{}</a>', link, obj.iiko_name)

    get_branch_link.short_description = "Ветка (филиал)"


class LocalBrandInline(admin.TabularInline):
    model = LocalBrand
    extra = 0
    classes = ("collapse",)
    fields = (
        "get_local_brand_link",
        "city",
        "priority",
        "is_active",
    )
    readonly_fields = (
        "city",
        "get_local_brand_link",
    )

    def get_local_brand_link(self, obj):
        link = reverse("admin:partners_localbrand_change", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">{}</a>', link, obj.full_name)

    get_local_brand_link.short_description = "Локальный бренд"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, LocalBrandInline]


@admin.register(LocalBrand)
class LocalBrandAdmin(admin.ModelAdmin):
    inlines = [LocalCategoryInline, BranchInline]
    list_filter = ('city',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_filter = ('local_brand',)
