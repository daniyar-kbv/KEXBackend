from django.db import models

from apps.common.models import AbstractNameModel
from apps.translations.models import MultiLanguageTextEditor
from .services import slugify


class TemplateModel(AbstractNameModel):
    template = models.ForeignKey(MultiLanguageTextEditor, verbose_name="HTML шаблон", on_delete=models.CASCADE)
    priority = models.IntegerField("Позиция в очереди", default=0)
    slug = models.SlugField("Читабельная ссылка", unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.ru)

        super(TemplateModel, self).save(*args, **kwargs)


class Document(TemplateModel):
    ...
