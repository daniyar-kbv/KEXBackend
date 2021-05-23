from django.contrib import admin

from .models import Category, Position, PositionInfoByOrganization


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0


class PositionInfoByOrganizationInline(admin.StackedInline):
    model = PositionInfoByOrganization
    extra = 0


class PositionAdmin(admin.ModelAdmin):
    model = Position
    inlines = [PositionInfoByOrganizationInline]
    list_filter = [
        "iiko_brand",
        "category",
    ]


admin.site.register(Category)
admin.site.register(Position, PositionAdmin)
