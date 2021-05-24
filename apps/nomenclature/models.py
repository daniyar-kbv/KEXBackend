from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import AbstractNameModel
from apps.partners.models import OrganizationRelationMixin


class Category(OrganizationRelationMixin, AbstractNameModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории позиции")

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self._meta.get_field('name').related_name = "category_names"


class Position(OrganizationRelationMixin, AbstractNameModel):
    class Meta:
        verbose_name = _("Позиция(Блюдо)")
        verbose_name_plural = _("Позиции(Блюда)")

    def __init__(self, *args, **kwargs):
        super(Position, self).__init__(*args, **kwargs)
        self._meta.get_field('name').related_name = "position_names"

    description = models.TextField(_("Описание"))
    price = models.DecimalField(
        _("Цена"),
        decimal_places=2,
        max_digits=12
    )
    category = models.ForeignKey(
        "nomenclature.Category",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="positions",
        verbose_name=_("Категория"),
    )
    is_additional = models.BooleanField(
        _("Дополнительная позиция"),
        default=False,
    )

    def __str__(self):
        return self.name


class Combo(OrganizationRelationMixin, AbstractNameModel):
    class Meta:
        verbose_name = _("Комбо")
        verbose_name_plural = _("Комбо")

    def __init__(self, *args, **kwargs):
        super(Combo, self).__init__(*args, **kwargs)
        self._meta.get_field('name').related_name = "combo_names"

    price = models.DecimalField(
        _("Цена"),
        decimal_places=2,
        max_digits=12
    )
    positions = models.ManyToManyField("nomenclature.Position",)
