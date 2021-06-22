from django.db import models

from . import PromotionTypes
from apps.translations.models import MultiLanguageFile, MultiLanguageTextEditor
from apps.docs.models import Document, TemplateModel


class Promotion(TemplateModel):
    image = models.ForeignKey(MultiLanguageFile, verbose_name="Картинка", on_delete=models.CASCADE)
    type = models.CharField("Тип Акции", max_length=20, choices=PromotionTypes.choices)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['priority']

