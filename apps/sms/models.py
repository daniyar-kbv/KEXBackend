from uuid import uuid4

import pyotp
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import PhoneNumber

from django.conf import settings
from django.db import models, transaction

from apps.test_app.models import TimestampModel, CharIDModel
from .manager import OTPQueryset


class SMSMessage(TimestampModel):
    uuid = models.UUIDField("Идентификатор", default=uuid4, unique=True, editable=False)
    recipients = models.CharField("Получатели", max_length=255, editable=False)
    content = models.TextField("Содержимое", editable=False)
    error_code = models.IntegerField("Код ошибки", null=True, editable=False)
    error_description = models.CharField(
        "Описание ошибки", max_length=255, null=True, editable=False
    )

    class Meta:
        verbose_name = "SMS сообщение"
        verbose_name_plural = "SMS сообщения"


class SMSType(CharIDModel):
    name = models.CharField(
        "Наименование", max_length=255
    )

    class Meta:
        verbose_name = "Тип смс"
        verbose_name_plural = "Типы смс"

    def __str__(self):
        return f"{self.id}({self.name})"


class SMSTemplate(models.Model):
    name = models.ForeignKey(
        SMSType,
        on_delete=models.CASCADE,
    )
    content = models.TextField("Содержимое", help_text="""
    Используется django.template, {{otp}}
    """)

    class Meta:
        verbose_name = "Шаблон СМС"
        verbose_name_plural = "Шаблоны СМС"


class OTP(TimestampModel):
    code = models.CharField("OTP", max_length=12, db_index=True, editable=False)
    verified = models.BooleanField("Подтверждён", default=False, editable=False)
    mobile_phone = PhoneNumberField("Мобильный телефон", editable=False)

    objects = OTPQueryset.as_manager()

    class Meta:
        verbose_name = "Одноразовый пароль"
        verbose_name_plural = "Одноразовые пароли"
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
