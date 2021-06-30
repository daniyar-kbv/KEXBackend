from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import PromotionTypes
from apps.translations.models import MultiLanguageFile
from apps.docs.models import TemplateModel

User = get_user_model()


class Promotion(TemplateModel):
    image = models.ForeignKey(MultiLanguageFile, verbose_name="Картинка", on_delete=models.CASCADE)
    promo_type = models.CharField("Тип Акции", max_length=20, choices=PromotionTypes.choices)
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
