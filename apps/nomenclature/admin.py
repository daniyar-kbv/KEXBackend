from django.contrib import admin

from apps.common.admin import ReadChangeOnlyTabularInline, ReadChangeOnlyStackedInline, AbstractNameModelForm, \
    AbstractDescriptionModelForm

from .models import (
    Category, BranchCategory,
    LocalPosition, BranchPosition,
)


class CategoryInline(ReadChangeOnlyTabularInline):
    model = Category
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


class LocalPositionInline(ReadChangeOnlyStackedInline):
    model = LocalPosition
    extra = 0
    classes = ("collapse",)
    fields = (
        "id",
        "name",
        "description",
        "image",
        "get_iiko_name",
        "local_category",
    )
    readonly_fields = (
        "id",
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
        "description",
        "iiko_name",
        "branch_category",
    )
    readonly_fields = (
        "name",
        "description",
        "iiko_name",
        "branch_category",
    )


class LocalPositionForm(AbstractNameModelForm, AbstractDescriptionModelForm):
    class Meta:
        model = LocalPosition
        exclude = ('name', 'description')


@admin.register(LocalPosition)
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
