from uuid import UUID
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.utils import create_multi_language_char
from apps.common.models import AbstractNameModel, UUIDModel

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand


class Category(UUIDModel, AbstractNameModel):
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
    priority = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
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

        # for branch in local_brand.branches.active():
        #     BranchCategory.register_branch_category(
        #         branch=branch,
        #         category=category,
        #     )

        return category
