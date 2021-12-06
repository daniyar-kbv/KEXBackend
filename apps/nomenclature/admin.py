from django.contrib import admin

from apps.common.admin import ReadChangeOnlyTabularInline, ReadChangeOnlyStackedInline

from .models import (
    Category,
    Position, BranchPosition,
)
from apps.common.admin import ImageModelInline


class CategoryInline(ReadChangeOnlyTabularInline):
    model = Category
    extra = 0
    classes = ("collapse",)
    fields = (
        "name",
        "priority",
        "is_active",
    )
    readonly_fields = (
        "name",
    )


class PositionInline(ReadChangeOnlyStackedInline):
    model = Position
    extra = 0
    classes = ("collapse",)
    fields = (
        "id",
        "name",
        "priority",
        "position_type",
        "description",
        "is_active",
        "category",
    )
    readonly_fields = (
        "id",
        "category",
    )


class BranchPositionInline(ReadChangeOnlyTabularInline):
    model = BranchPosition
    extra = 0
    classes = ("collapse",)
    fields = (
        "name",
        "description",
        "price",
        'position_type',
        "is_active",
        "is_exists",
        "is_available",
    )
    readonly_fields = (
        "name",
        "description",
        'position_type',
        "price",
        "is_exists",
        "is_available",
    )


@admin.register(Position)
class LocalPositionAdmin(admin.ModelAdmin):
    list_filter = "local_brand",
    list_display = (
        'name', 'local_brand', 'category', 'position_type',
        'is_web_image_exists', 'is_mobile_image_exists'
    )
    readonly_fields = (
        "category",
        "local_brand",
        "outer_id",
        'is_web_image_exists',
        'is_mobile_image_exists'
    )
    inlines = [
        ImageModelInline
    ]

    def is_web_image_exists(self, obj) -> bool:
        return obj.images.for_web().exists()

    is_web_image_exists.boolean = True

    def is_mobile_image_exists(self, obj) -> bool:
        return obj.images.for_mobile().exists()

    is_mobile_image_exists.boolean = True