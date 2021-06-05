from django.contrib import admin

from apps.common.admin import ReadChangeOnlyTabularInline

from .models import (
    Category, LocalCategory, BranchCategory,
    LocalPosition, BranchPosition,
)


class CategoryInline(admin.TabularInline):
    model = Category
    classes = ("collapse",)
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


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


class LocalPositionInline(ReadChangeOnlyTabularInline):
    model = LocalPosition
    extra = 0
    classes = ("collapse",)
    fields = (
         "name",
         "image",
         "get_iiko_name",
         "local_category",
    )
    readonly_fields = (
        "get_iiko_name",
    )

    def get_iiko_name(self, obj):
        return obj.branch_positions.filter(
            iiko_name__isnull=False
        ).first().iiko_name
    get_iiko_name.short_description = "Название в системе IIKO"


class BranchPositionInline(ReadChangeOnlyTabularInline):
    model = BranchPosition
    extra = 0
    classes = ("collapse",)
    fields = (
        "name",
        "iiko_name",
        "branch_category",
    )
    readonly_fields = (
        "name",
        "iiko_name",
        "branch_category",
    )
