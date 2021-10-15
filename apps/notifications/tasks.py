from typing import List

from django.conf import settings

from config.settings import Languages
from config import celery_app

from . import PushTypes
from .models import Notification, NotificationTemplate
from .firebase import (
    push_broadcast,
    push_multicast,
    subscribe_to_topic,
    unsubscribe_from_topic,
)


@celery_app.task(name='notifications.subscribe_to_topic')
def register_token_in_firebase(topic: str, registration_tokens: List[str]) -> None:
    print(f'REGISTER_TOKEN_IN_FIREBASE. tokens: {registration_tokens}')

    subscribe_to_topic(topic=topic, registration_tokens=registration_tokens)
    [unsubscribe_from_topic(lang, registration_tokens) for lang in Languages if lang != topic]


@celery_app.task
def push_broadcast_later(notify_data):
    push = Notification.objects.filter(title__text_ru=notify_data['ru']['title'], date=notify_data['date'])

    if push:
        del notify_data['date']
        push_broadcast(notify_data)
        print(f"Sending push: {notify_data['ru']['title']} finished")
    else:
        print(f"There is no such push: {notify_data['ru']['title']}")


@celery_app.task
def push_order_rate_to_user(fb_tokens, order, lang=settings.DEFAULT_LANGUAGE):
    template = NotificationTemplate.objects.get(push_type=PushTypes.ORDER_RATE)
    extra = {
        'push_type': str(PushTypes.ORDER_RATE),
        'push_type_value': str(order.id)
    }
    push_multicast(fb_tokens, getattr(template.title, lang), getattr(template.description, lang), extra)


@celery_app.task
def push_order_status_update_to_user(fb_tokens, order_id, order_status, lang=settings.DEFAULT_LANGUAGE):
    try:
        template = NotificationTemplate.objects.get(push_type=PushTypes.ORDER_STATUS_UPDATE)
        title = getattr(template.title, lang).format(order_id)
        body = getattr(template.description, lang).format(order_status)
        extra = {
            'push_type': str(PushTypes.ORDER_STATUS_UPDATE),
            'push_type_value': str(order_id)
        }
        push_multicast(fb_tokens, title, body, extra)
    except Exception as e:
        print("push_order_status_update_to_user task: ", str(e))
