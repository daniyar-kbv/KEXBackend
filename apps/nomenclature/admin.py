from django.contrib import admin

from .models import Category, Position, PositionInfoByOrganization


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0


class PositionInfoByOrganizationInline(admin.StackedInline):
    model = PositionInfoByOrganization
    extra = 0


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_filter = (
        "iiko_brand",
        "category",
    )
    inlines = [PositionInfoByOrganizationInline]


admin.site.register(Category)
