from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from apps.translations.models import MultiLanguageChar


class AbstractNameModel(models.Model):
    name = models.ForeignKey(
        MultiLanguageChar,
        verbose_name=_("Название"),
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name.ru


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


# class MultiLanguageText(models.Model):
#     text_ru = models.CharField("Текст (рус)", max_length=100, null=True)
#     text_kk = models.CharField("Текст (каз)", max_length=100, blank=True, null=True)
#     text_en = models.CharField("Текст (англ)", max_length=100, blank=True, null=True)
#
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     class Meta:
#         abstract = True
#
#     @property
#     def text(self):
#         return self.text_ru
#
#     def __str__(self):
#         return self.text_ru


# class TestCountry(AbstractNameModel):
#     extra = models.ForeignKey(MultiLanguageChar, on_delete=models.CASCADE, null=True, related_name='extras')
#     description = models.ForeignKey(MultiLanguageText, on_delete=models.CASCADE, null=True)


# class MultiLanguageGenericRelation(GenericRelation):
#     @property
#     def ru(self):
#         ctype = ContentType.objects.get_for_model(self.__class__)
#         try:
#             mltext = MultiLanguageText.objects.get(content_type__pk=ctype.id, object_id=self.id)
#         except:
#             return None
#         return mltext.text_ru
#
#     @ru.setter
#     def ru(self, value):
#         ctype = ContentType.objects.get_for_model(self.__class__)
#         try:
#             mltext = MultiLanguageText.objects.get(content_type__pk=ctype.id, object_id=self.id)
#             mltext.text_ru = value
#         except:
#             return None
#
#
# class NameField(MultiLanguageText):
#     class Meta:
#         verbose_name = _("Название")
#         verbose_name_plural = _("Названия")
#
#     def __init__(self, *args, **kwargs):
#         super(NameField, self).__init__(*args, **kwargs)
#         self._meta.get_field('text_ru').verbose_name = "Название (рус)"
#         self._meta.get_field('text_kk').verbose_name = "Название (каз)"
#         self._meta.get_field('text_en').verbose_name = "Название (англ)"
#
#
# class DescriptionField(MultiLanguageText):
#     class Meta:
#         verbose_name = _("Описание")
#         verbose_name_plural = _("Описания")
#
#     def __init__(self, *args, **kwargs):
#         super(DescriptionField, self).__init__(*args, **kwargs)
#         self._meta.get_field('text_ru').verbose_name = "Описание (рус)"
#         self._meta.get_field('text_kk').verbose_name = "Описание (каз)"
#         self._meta.get_field('text_en').verbose_name = "Описание (англ)"
#
#
# class TestModel(models.Model):
#     name = MultiLanguageGenericRelation(NameField, limit_choices_to=1)
#     description = MultiLanguageGenericRelation(DescriptionField, limit_choices_to=1)
#     text_area = models.TextField(null=True, blank=True)
#     text_input = models.CharField(max_length=10, null=True, blank=True)
#     number = models.IntegerField(null=True, blank=True)
