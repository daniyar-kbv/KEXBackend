from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from apps.translations.models import MultiLanguageChar, MultiLanguageText
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
