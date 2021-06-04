from django.contrib import admin

from .models import Category, LocalCategory, BranchCategory


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0


class LocalCategoryInline(admin.StackedInline):
    model = LocalCategory
    extra = 0
    readonly_fields = (
        "name",
        "category",
    )
#
#
# class PositionInfoByBranchInline(admin.StackedInline):
#     model = PositionInfoByBranch
#     extra = 0
#
#
# class PositionForm(AbstractNameModelForm):
#     class Meta(AbstractNameModelForm.Meta):
#         model = Position
#
#
# @admin.register(Position)
# class PositionAdmin(admin.ModelAdmin):
#     model = Position
#     list_filter = (
#         "local_brand",
#         "category",
#     )
#     inlines = [PositionInfoByBranchInline]
#     form = PositionForm
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
