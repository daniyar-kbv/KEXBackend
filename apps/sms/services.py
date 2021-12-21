import os
from datetime import timedelta
from typing import Tuple, Union, Optional

from django.db import transaction
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber
from constance import config

from .exceptions import InvalidOTP
from .models import OTP, SMSMessage, SMSTemplate
from .tasks import send_sms_task


def send_sms(
    recipient: Union[str, PhoneNumber],
    message: str = "",
    template_name: Union[str, Tuple[str, str]] = None,
    kwargs: dict = None,
    delta: Optional[timedelta] = None,
):
    if kwargs is None:
        kwargs = {}

    if not message:
        if not template_name:
            raise ValueError("Either content or template_name needs to be provided")

        message = SMSTemplate.objects.get(name=template_name).content

    message = message.format(**kwargs)

    if not isinstance(recipient, list):
        recipient = [recipient]

    if delta:
        eta = timezone.now() + delta
    else:
        eta = None

    with transaction.atomic():
        sms = SMSMessage(recipients=', '.join(recipient), content=message)
        sms.save()
        if config.SEND_OTP:
            transaction.on_commit(
                lambda: send_sms_task.apply_async(
                    eta=eta, args=[recipient, message, sms.uuid]
                )
            )


def send_otp(mobile_phone: PhoneNumber, template_name: str = "OTP"):
    otp = OTP.generate(mobile_phone)
    send_sms(
        recipient=mobile_phone.as_e164, template_name=template_name, kwargs={"otp": otp},
    )


def verify_otp(code: str, mobile_phone: PhoneNumber, save=False):
    otp = OTP.objects.active().filter(mobile_phone=mobile_phone).last()

    if str(mobile_phone) in config.config.SMS_FREE_PHONES:
        return True

    if config.USE_DEFAULT_OTP and code == "1111":
        return True
    elif not otp or otp.code != code:
        raise InvalidOTP

    if save:
        otp.verified = True
        otp.save(update_fields=["verified"])

    return True
