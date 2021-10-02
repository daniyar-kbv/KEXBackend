from django.contrib.contenttypes.admin import GenericStackedInline
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

from apps.common.admin import ReadChangeOnlyTabularInline, AbstractNameModelForm
from apps.nomenclature.admin import (
    CategoryInline,
    PositionInline, BranchPositionInline,
)

from .models import (
    Brand, BrandImage, LocalBrand, Branch, BranchDeliveryTime, LocalBrandPaymentType
)
from apps.common.models import ImageModel


class LocalBrandPaymentTypeInline(admin.TabularInline):
    model = LocalBrandPaymentType
    extra = 0
    classes = ('collapse',)
    fields = ('name', 'is_current')
    readonly_fields = 'name',


class BrandImageInline(admin.StackedInline):
    model = BrandImage
    extra = 0
    classes = ("collapse",)


class ImageModelInline(GenericStackedInline):
    model = ImageModel
    extra = 0


class BranchDeliveryTimeInline(admin.TabularInline):
    model = BranchDeliveryTime
    extra = 0
    classes = ('collapse',)


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
    )
    readonly_fields = (
        "get_local_brand_link",
    )


class LocalBrandInline(LocalBrandInlineBase):
    fields = (
        "get_local_brand_link",
        "city",
        "is_active",
    )
    readonly_fields = (
        "city",
        "get_local_brand_link",
    )


class BrandForm(AbstractNameModelForm):
    class Meta:
        model = Brand
        exclude = ('name', )


class BranchForm(AbstractNameModelForm):
    class Meta:
        model = Branch
        exclude = ('name', )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [BrandImageInline, LocalBrandInline, ImageModelInline]
    list_editable = ["priority"]
    list_display = ['name', "id", "priority"]
    ordering = ['priority']
    form = BrandForm


@admin.register(LocalBrand)
class LocalBrandAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
        PositionInline,
        BranchInline,
        LocalBrandPaymentTypeInline,
    ]
    list_filter = ('city',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_filter = ('local_brand',)
    inlines = [BranchPositionInline, BranchDeliveryTimeInline]
    form = BranchForm
