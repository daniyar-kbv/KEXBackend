from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from apps.translations.models import MultiLanguageChar


class AbstractNameModel(models.Model):
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


class CharIDModel(models.Model):
    id = models.CharField(
        _("Уникальный код"),
        max_length=16,
        primary_key=True
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uuid = models.UUIDField("Идентификатор", default=uuid4, unique=True, editable=False)

    class Meta:
        abstract = True


class TimestampModel(models.Model):
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


class ServiceHistoryModel(models.Model):
    history = GenericRelation('pipeline.ServiceHistory')

    class Meta:
        abstract = True
