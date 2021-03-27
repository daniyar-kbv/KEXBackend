from django.conf import settings
from requests.exceptions import ConnectionError, HTTPError, Timeout

from .backend import sms_backend

from .models import OTP, SMSMessage
from django.conf import settings

# @celery_app.task(
#     autoretry_for=(ConnectionError, HTTPError, Timeout),
#     default_retry_delay=2,
#     retry_kwargs={"max_retries": 5},
#     ignore_result=True,
# )
def send_sms_task(recipient: str, message: str, message_id: str = None):
    auth = (settings.SMS_LOGIN, settings.SMS_PASSWORD)

    if getattr(settings, 'SMS_ENABLE', False):
        sms = sms_backend(*auth)
        data = sms.send_sms(
            sender=settings.SMS_SENDER,
            recipient=recipient,
            message=message
        )

        # if "error" in data:
        #     instance: SMSMessage = SMSMessage.objects.get(uuid=message_id)
        #     instance.error_description = data["error"]
        #     instance.error_code = data.get("error_code")
        #     instance.save(update_fields=["error_description", "error_code"])

        return data


# @celery_app.task(ignore_result=True)
def delete_expired_otps():
    return OTP.objects.expired().delete()
