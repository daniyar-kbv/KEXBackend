from requests import get
from requests.models import PreparedRequest
from requests.exceptions import ConnectionError, HTTPError, Timeout
from constance import config

from config import celery_app

from .models import OTP


@celery_app.task(
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=2,
    retry_kwargs={"max_retries": 5},
    ignore_result=True,
)
def send_sms_task(recipient: str, message: str):
    req = PreparedRequest()
    url = 'https://api.mobizon.kz/service/message/sendsmsmessage'
    params = {
        'output': "json",
        'recipient': recipient,
        'text': message,
        'apiKey': config.MOBIZON_API_KEY
    }

    req.prepare_url(url, params)
    print(req.url)
    res = get(req.url)

    return f"sms result {recipient}. {res.json()}"


@celery_app.task(ignore_result=True)
def delete_expired_otps():
    return OTP.objects.expired().delete()

"""
from apps.sms.tasks import send_sms_task
send_sms_task.delay(recipient='+77087552390', message='12121121212')
"""
