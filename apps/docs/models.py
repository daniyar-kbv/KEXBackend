from django.db import models

from apps.common.models import AbstractNameModel, AbstractTemplateModel
from apps.translations.models import MultiLanguageTextEditor
from .services import slugify


class TemplateModel(AbstractNameModel, AbstractTemplateModel):
    priority = models.IntegerField("Позиция в очереди", default=0)
    slug = models.SlugField("Читабельная ссылка", unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.ru)

        super(TemplateModel, self).save(*args, **kwargs)


class Document(TemplateModel):
    for_web = models.BooleanField("Статья для сайта", default=False)
