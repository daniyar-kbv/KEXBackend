from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

from apps.common.admin import ReadOnlyMixin, ReadChangeOnlyTabularInline
from apps.nomenclature.admin import (
    CategoryInline, LocalCategoryInline, BranchCategoryInline,
    LocalPositionInline, BranchPositionInline,
)

from .models import Brand, LocalBrand, Branch


class BranchInline(ReadChangeOnlyTabularInline):
    model = Branch
    extra = 0
    classes = ("collapse",)
    fields = (
        "get_branch_link",
        "is_active",
    )
    readonly_fields = (
        "get_branch_link",
    )

    def get_branch_link(self, obj):
        link = reverse("admin:partners_branch_change", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">{}</a>', link, obj.iiko_name)

    get_branch_link.short_description = "Ветка (филиал)"


class LocalBrandInlineBase(ReadChangeOnlyTabularInline):
    classes = ("collapse",)
    model = LocalBrand
    extra = 0

    def get_local_brand_link(self, obj):
        link = reverse("admin:partners_localbrand_change", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">{}</a>', link, obj.full_name)

    get_local_brand_link.short_description = "Локальный бренд"


class LocalBrandPriorityInline(LocalBrandInlineBase):
    fields = (
        "get_local_brand_link",
        "priority",
    )
    readonly_fields = (
        "get_local_brand_link",
    )


class LocalBrandInline(LocalBrandInlineBase):
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


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, LocalBrandInline]
    list_select_related = (
        "categories",
        "local_brands"
    )


@admin.register(LocalBrand)
class LocalBrandAdmin(admin.ModelAdmin):
    inlines = [
        LocalCategoryInline,
        LocalPositionInline,
        BranchInline,
    ]
    list_select_related = (
        "local_categories",
        "local_positions",
        "branches",
    )
    list_filter = ('city',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_filter = ('local_brand',)
    list_select_related = (
        "branch_positions",
        "branch_categories",
    )
    inlines = [
        BranchCategoryInline,
        BranchPositionInline,
    ]
