from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _  # noqa


class AbstractNameModel(models.Model):
    name = models.CharField(
        _("Название"),
        max_length=256
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


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


class Address(models.Model):
    # todo моделька должна находится в другом app-e
    country = models.CharField(_("Страна"), max_length=255, null=True, blank=True)
    region = models.CharField(_("Регион"), max_length=255, null=True, blank=True)
    city = models.CharField(_("Город"), max_length=255, null=True, blank=True)
    district = models.CharField(_("Район"), max_length=255, null=True, blank=True)
    street = models.CharField(_("Улица"), max_length=255, null=True, blank=True)
    building = models.CharField(_("Дом / здание"), max_length=100, null=True, blank=True)
    corpus = models.CharField(_("Корпус"), max_length=100, null=True, blank=True)
    flat = models.CharField(_("Квартира"), max_length=50, null=True, blank=True)
    postal_code = models.CharField(_("Почтовый индекс"), max_length=7, null=True, blank=True)
