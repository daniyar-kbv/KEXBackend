# from django.contrib import admin
#
# from apps.common.admin import AbstractNameModelForm
#
# from .models import Category, Position, PositionInfoByBranch
#
#
# class CategoryInline(admin.StackedInline):
#     model = Category
#     extra = 0
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
#         "iiko_brand",
#         "category",
#     )
#     inlines = [PositionInfoByBranchInline]
#     form = PositionForm
#
#     fields = (
#         "name_kk",
#         "name_ru",
#         "name_en",
#         "iiko_brand",
#         "iiko_name",
#         "iiko_description",
#         "category",
#         "outer_id",
#     )
#
# admin.site.register(Category)
