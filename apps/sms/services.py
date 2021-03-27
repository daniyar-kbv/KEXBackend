import os
from datetime import timedelta
from typing import List, Tuple, Union, Optional

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber, to_python as phone_to_python
from django.template import Template, Context

from .models import SMSType
from .exceptions import InvalidOTP
from .models import OTP, SMSMessage, SMSTemplate
from .tasks import send_sms_task


def get_message_from_template(template_name, kwargs: dict = None):
    content_template = SMSTemplate.objects.get(name=template_name).content
    template = Template(content_template)
    context = Context(kwargs)
    return template.render(context)


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

        message = get_message_from_template(template_name, kwargs)

    if isinstance(recipient, str):
        # Parse mobile_phone for validate number
        recipient = phone_to_python(recipient)

    if delta:
        eta = timezone.now() + delta
    else:
        eta = None

    with transaction.atomic():
        sms = SMSMessage(recipients=recipient.as_e164, content=message)
        sms.save()
        transaction.on_commit(
            lambda: send_sms_task.apply_async(
                eta=eta, args=[recipient.as_e164, message, sms.uuid]
            )
        )


def send_otp(mobile_phone: PhoneNumber, template_name: str = "OTP"):
    otp = OTP.generate(mobile_phone)
    send_sms(
        recipient=mobile_phone, template_name=template_name, kwargs={"otp": otp},
    )


def verify_otp(code: str, mobile_phone: PhoneNumber, save=False):
    otp = OTP.objects.active().filter(mobile_phone=mobile_phone).last()

    default_otp = os.getenv("DEFAULT_OTP")

    if settings.DEBUG and default_otp is not None and default_otp == code:
        return True
    elif not otp or otp.code != code:
        raise InvalidOTP

    if save:
        otp.verified = True
        otp.save(update_fields=["verified"])

    return True
