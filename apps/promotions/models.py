from django.db import models

from . import PromotionTypes
from apps.translations.models import MultiLanguageFile, MultiLanguageTextEditor


class Promotion(models.Model):
    slug = models.SlugField("Читабельная ссылка", unique=True)
    image = models.ForeignKey(MultiLanguageFile, verbose_name="Картинка", on_delete=models.CASCADE)
    template = models.ForeignKey(MultiLanguageTextEditor, verbose_name="HTML шаблон", on_delete=models.CASCADE)
    type = models.CharField("Тип Акции", max_length=20, choices=PromotionTypes.choices)
    position = models.IntegerField("Позиция в очереди", default=0)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['position']

