from django.contrib import admin

from apps.common.admin import ReadChangeOnlyTabularInline

from .models import Category, LocalCategory, BranchCategory


class CategoryInline(admin.TabularInline):
    model = Category
    classes = ("collapse",)
    extra = 0


class LocalCategoryInline(ReadChangeOnlyTabularInline):
    model = LocalCategory
    extra = 0
    classes = ("collapse",)
    fields = (
        "name",
        "is_active",
    )
    readonly_fields = (
        "name",
    )


class BranchCategoryInline(ReadChangeOnlyTabularInline):
    model = BranchCategory
    extra = 0
    classes = ("collapse",)
    fields = (
        "name",
        "is_active",
    )
    readonly_fields = (
        "name",
    )

#
#
# class LocalPositionInfoByBranchInline(admin.StackedInline):
#     model = LocalPositionInfoByBranch
#     extra = 0
#
#
# class LocalPositionForm(AbstractNameModelForm):
#     class Meta(AbstractNameModelForm.Meta):
#         model = LocalPosition
#
#
# @admin.register(LocalPosition)
# class LocalPositionAdmin(admin.ModelAdmin):
#     model = LocalPosition
#     list_filter = (
#         "local_brand",
#         "category",
#     )
#     inlines = [LocalPositionInfoByBranchInline]
#     form = LocalPositionForm
#
#     fields = (
#         "name_kk",
#         "name_ru",
#         "name_en",
#         "local_brand",
#         "iiko_name",
#         "iiko_description",
#         "category",
#         "outer_id",
#     )
#
# admin.site.register(Category)
