from typing import List

from config import celery_app

from . import PushTypes
from .models import Notification
from .services import send_multicast_push, subscribe
from .firebase import (
    push_broadcast,
)


@celery_app.task(name='notifications.subscribe_to_topic')
def register_token_in_firebase(topic: str, registration_tokens: List[str]) -> None:
    print(f'REGISTER_TOKEN_IN_FIREBASE. tokens: {registration_tokens}')
    subscribe(topic, registration_tokens)


@celery_app.task
def push_broadcast_later(notify_data):
    push = Notification.objects.filter(title__text_ru=notify_data['ru']['title'], date=notify_data['date'])

    if push:
        del notify_data['date']
        push_broadcast(notify_data)
        print(f"Sending push: {notify_data['ru']['title']} finished")
    else:
        print(f"There is no such push: {notify_data['ru']['title']}")


@celery_app.task(name='notifications.rate_order_notifier')
def rate_order_notifier(order_pk: int):
    send_multicast_push(order_pk, PushTypes.ORDER_RATE)


@celery_app.task(name='notifications.status_update_notifier')
def status_update_notifier(order_pk: int):
    send_multicast_push(order_pk, PushTypes.ORDER_STATUS_UPDATE)

