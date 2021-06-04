from django.contrib import admin

from apps.nomenclature.admin import CategoryInline, LocalCategoryInline

from .models import Brand, LocalBrand, Branch


class BranchInline(admin.StackedInline):
    model = Branch
    extra = 0


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]


@admin.register(LocalBrand)
class LocalBrandAdmin(admin.ModelAdmin):
    inlines = [LocalCategoryInline, BranchInline]
    list_filter = ('city',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_filter = ('local_brand',)
