from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.translations.models import MultiLanguageChar, MultiLanguageText, MultiLanguageTextEditor, MultiLanguageFile
from .managers import MainManager


class MainModel(models.Model):
    objects = MainManager()

    class Meta:
        abstract = True


class AbstractNameModel(MainModel):
    name = models.ForeignKey(
        MultiLanguageChar,
        verbose_name=_("Название"),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.name is not None:
            return self.name.ru

        return "Не задано"


class AbstractTitleModel(MainModel):
    title = models.ForeignKey(
        MultiLanguageChar,
        verbose_name=_("Заголовок"),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.title is not None:
            return self.title.ru

        return "Не задано"


class AbstractDescriptionModel(MainModel):
    description = models.ForeignKey(
        MultiLanguageText,
        verbose_name=_("Описание"),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.description is not None:
            return self.description.ru

        return "Не задано"


class AbstractTemplateModel(MainModel):
    template = models.ForeignKey(
        MultiLanguageTextEditor,
        verbose_name="HTML шаблон",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.template is not None:
            return f"Шаблон #{self.id}"

        return "Не задано"


class AbstractImageModel(MainModel):
    image = models.ForeignKey(
        MultiLanguageFile,
        verbose_name="Картинка",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.image is not None:
            return f"Картинка #{self.id}"

        return "Не задано"


class CharIDModel(MainModel):
    id = models.CharField(
        _("Уникальный код"),
        max_length=16,
        primary_key=True
    )

    class Meta:
        abstract = True


class UUIDModel(MainModel):
    uuid = models.UUIDField("Идентификатор", default=uuid4, unique=True, editable=False)

    class Meta:
        abstract = True


class TimestampModel(MainModel):
    created_at = models.DateTimeField(
        _("Время создания"), auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        _("Время последнего изменения"), auto_now=True, db_index=True
    )

    class Meta:
        abstract = True

    @property
    def created_at_pretty(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")  # noqa

    @property
    def updated_at_pretty(self):
        return self.updated_at.strftime("%d/%m/%Y %H:%M:%S")  # noqa


class ServiceHistoryModel(MainModel):
    history = GenericRelation('pipeline.ServiceHistory')

    class Meta:
        abstract = True


class MultipleModelFK(MainModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
