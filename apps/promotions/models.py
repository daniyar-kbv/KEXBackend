from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import PromotionTypes
from apps.translations.models import MultiLanguageFile, MultiLanguageText
from apps.docs.models import TemplateModel
from apps.common.models import AbstractDescriptionModel
from ..partners.models import LocalBrand

User = get_user_model()


class Promotion(TemplateModel, AbstractDescriptionModel):
    image = models.ForeignKey(MultiLanguageFile, verbose_name="Картинка", on_delete=models.CASCADE)
    promo_type = models.CharField("Тип Акции", max_length=20, choices=PromotionTypes.choices)
    description = models.ForeignKey(
        MultiLanguageText, verbose_name=_("Текстовое описание (для сайта)"), on_delete=models.CASCADE, null=True
    )
    local_brand = models.ManyToManyField(LocalBrand, verbose_name=_("Локальный бренд"), blank=True)
    # contest_type = models.CharField("Тип Конкурса", max_length=20, choices=PromotionTypes.choices)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['priority']


class Participation(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="participations", on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, verbose_name="Акция", related_name="participations", on_delete=models.CASCADE)
    instagram_username = models.CharField(_("Инстаграм пользователя"), max_length=256, null=True, blank=True)
    # instagram сделан здесь а не в профиле для случая, если пользователь хочет в другом конкурсе поучаствовать с
    # другого инстаграм аккаунта
