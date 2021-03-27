from django.db.models import TextChoices

default_app_config = 'apps.sms.apps.SmsConfig'


class SMSType(TextChoices):
    OTP = "OTP", "Отправка одноразового пароля"
