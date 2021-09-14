from django.contrib import admin

from apps.common.admin import ReadChangeOnlyTabularInline, ReadChangeOnlyStackedInline, AbstractNameModelForm, \
    AbstractDescriptionModelForm

from .models import (
    Category,
    Position, BranchPosition,
)


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
        "description",
        "image",
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
        "is_active",
        "is_exists",
        "is_available",
    )
    readonly_fields = (
        "name",
        "description",
        "price",
        "is_exists",
        "is_available",
    )


class LocalPositionForm(AbstractNameModelForm, AbstractDescriptionModelForm):
    class Meta:
        model = Position
        exclude = ('name', 'description')


@admin.register(Position)
class LocalPositionAdmin(admin.ModelAdmin):
    list_filter = "local_brand",
    readonly_fields = (
        # "name",
        # "description",
        "category",
        "local_brand",
        "outer_id",
    )
    form = LocalPositionForm
