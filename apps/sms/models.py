from uuid import uuid4

import pyotp
from phonenumbers import PhoneNumber
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _  # noqa

from apps.common.models import TimestampModel

from .import SMSType
from .manager import OTPQueryset


class SMSMessage(TimestampModel):
    uuid = models.UUIDField(_("Идентификатор"), default=uuid4, unique=True, editable=False)
    recipients = models.CharField(_("Получатели"), max_length=255, editable=False)
    content = models.TextField(_("Содержимое"), editable=False)
    error_code = models.IntegerField(_("Код ошибки"), null=True, editable=False)
    error_description = models.CharField(
        _("Описание ошибки"), max_length=255, null=True, editable=False
    )

    class Meta:
        verbose_name = _("SMS сообщение")
        verbose_name_plural = _("SMS сообщения")


class SMSTemplate(models.Model):
    name = models.CharField(
        _("Наименование"), max_length=32, choices=SMSType.choices, unique=True
    )
    content = models.TextField(_("Содержимое"))

    class Meta:
        verbose_name = _("Шаблон СМС")
        verbose_name_plural = _("Шаблоны СМС")


class OTP(TimestampModel):
    code = models.CharField(_("OTP"), max_length=12, db_index=True, editable=False)
    verified = models.BooleanField(_("Подтверждён"), default=False, editable=False)
    mobile_phone = PhoneNumberField(_("Мобильный телефон"), editable=False)

    objects = OTPQueryset.as_manager()

    class Meta:
        verbose_name = _("Одноразовый пароль")
        verbose_name_plural = _("Одноразовые пароли")
        unique_together = ("code", "mobile_phone")

    @classmethod
    def generate(cls, mobile_phone: PhoneNumber):
        with transaction.atomic():
            instance = cls.objects.create()

            hotp = pyotp.HOTP(settings.HOTP_KEY, digits=settings.OTP_LENGTH)
            code = hotp.at(instance.pk)

            instance.code = code
            instance.mobile_phone = mobile_phone
            instance.save()
        return code
