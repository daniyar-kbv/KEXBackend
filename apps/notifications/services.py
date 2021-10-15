from typing import List

from apps.orders.models import Order
from config.settings import Languages

from .models import Notification, NotificationTemplate
from .firebase import (
    push_multicast,
    subscribe_to_topic,
    unsubscribe_from_topic,
)


def form_notify_data(push: Notification):
    notify_data = {
        lang[0]: {
            'title': getattr(push.title, lang[0]),
            'body': getattr(push.description, lang[0]),
        } for lang in Languages.choices
    }

    notify_data['date'] = push.date
    notify_data['extra'] = {
        'push_type': str(push.push_type),
        'push_type_value': str(push.content_object.id) if push.content_object else ""
    }

    return notify_data


def send_multicast_push(
    order_pk: int, push_type: str,
):
    order = Order.objects.select_related('user').get(pk=order_pk)
    template = NotificationTemplate.objects.get(push_type=push_type)

    push_multicast(
        [order.user.fb_token],
        getattr(template.title, order.user.language),
        getattr(template.description, order.user.language),
        {'push_type': str(push_type),
         'push_type_value': str(order_pk)}
    )


def subscribe(
        topic: str, registration_tokens: List[str]
) -> None:
    if not isinstance(registration_tokens, list):
        registration_tokens = [registration_tokens]

    subscribe_to_topic(topic=topic, registration_tokens=registration_tokens)
    [unsubscribe_from_topic(lang, registration_tokens) for lang in Languages if lang != topic]
