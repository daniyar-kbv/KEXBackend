from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.translations.models import MultiLanguageText
from apps.docs.models import TemplateModel
from apps.common.models import MultiLanguageImageModel

from . import PromotionTypes

from ..common import ImageTypes
from ..partners.models import LocalBrand

User = get_user_model()


class Promotion(TemplateModel):
    promo_type = models.CharField(
        "Тип Акции",
        max_length=20,
        choices=PromotionTypes.choices
    )
    description = models.ForeignKey(
        MultiLanguageText,
        verbose_name=_("Текстовое описание (для сайта)"),
        on_delete=models.CASCADE,
        null=True
    )
    local_brand = models.ManyToManyField(
        LocalBrand,
        verbose_name=_("Локальный бренд"),
        blank=True
    )
    web_url = models.URLField(
        "Ссылка на веб-сайт",
        null=True,
        blank=True
    )
    start_date = models.DateField(
        "Дата начала",
        null=True,
        default=timezone.now
    )
    end_date = models.DateField(
        "Дата завершения",
        null=True,
        default=timezone.now
    )

    images = GenericRelation(MultiLanguageImageModel)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['priority']

    @property
    def web_image(self):
        if self.images.for_web().filter(image_type=ImageTypes.IMAGE_FOR_PROMOTION).exists():
            return self.images.for_web().filter(image_type=ImageTypes.IMAGE_FOR_PROMOTION).first().image

    @property
    def mobile_image(self):
        if self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_FOR_PROMOTION).exists():
            return self.images.for_mobile().filter(image_type=ImageTypes.IMAGE_FOR_PROMOTION).first().image


class Participation(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="participations",
        on_delete=models.CASCADE
    )
    promotion = models.ForeignKey(
        Promotion,
        verbose_name="Акция",
        related_name="participations",
        on_delete=models.CASCADE
    )
    instagram_username = models.CharField(
        _("Инстаграм пользователя"),
        max_length=256,
        null=True,
        blank=True
    )
