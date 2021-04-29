from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app

from .models import OTP


@celery_app.task(
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=2,
    retry_kwargs={"max_retries": 5},
    ignore_result=True,
)
def send_sms_task(recipient: str, message: str, message_id: str = None):
    return f"successfully sent sms to {recipient} - message {message}"


@celery_app.task(ignore_result=True)
def delete_expired_otps():
    return OTP.objects.expired().delete()
