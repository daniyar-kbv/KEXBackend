from uuid import UUID
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.nomenclature.managers import BranchCategoryManager
from apps.common.utils import create_multi_language_char
from apps.common.models import AbstractNameModel, UUIDModel

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand, Branch


class Category(AbstractNameModel):
    class Meta:
        verbose_name = _("Локальная категория")
        verbose_name_plural = _("Локальные категории")

    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
        related_name="categories",
        verbose_name=_("Локальный бренд"),
    )
    is_active = models.BooleanField(
        default=True,
    )
    outer_id = models.UUIDField(
        _("UUID в системе IIKO"), null=True,  # noqa
    )

    @classmethod
    def register_category(cls, local_brand: 'LocalBrand', outer_id: UUID, iiko_name: str):
        category, created = cls.objects.get_or_create(
            outer_id=outer_id,
            local_brand=local_brand,
        )

        if category.name is None:
            category.name = create_multi_language_char(iiko_name)
            category.save(update_fields=["name"])

        for branch in local_brand.branches.active():
            BranchCategory.register_branch_category(
                branch=branch,
                category=category,
            )

        return category


class BranchCategory(UUIDModel):
    class Meta:
        verbose_name = _("Категория филиала")
        verbose_name_plural = _("Категории филиалов")

    branch = models.ForeignKey(
        "partners.Branch",
        on_delete=models.PROTECT,
        null=True,
        related_name="branch_categories",
        verbose_name=_("Филиал"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Локальная категория"),
        related_name="branch_categories",
    )
    is_active = models.BooleanField(
        default=True
    )

    objects = BranchCategoryManager()

    @property
    def name(self):
        return self.category.name

    @classmethod
    def register_branch_category(cls, branch: 'Branch', category: Category):
        branch_category, created = cls.objects.get_or_create(
            category=category,
            branch=branch,
        )

        return branch_category