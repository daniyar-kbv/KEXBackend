import logging

from django.conf import settings

from . import PushTypes
from .models import Notification, NotificationTemplate
from config import celery_app
from .firebase import push_broadcast, send_to_token

logger = logging.getLogger('fcm')


@celery_app.task
def push_broadcast_later(notify_data):
    push = Notification.objects.filter(title__text_ru=notify_data['ru']['title'], date=notify_data['date'])
    print(f"Push exists or not: {push}")
    print("Push data: ")
    print(str(notify_data))
    if push:
        del notify_data['date']
        print('notify_data[date] deleted')
        print(notify_data)
        print(f"Sending push: {notify_data['ru']['title']} started")
        push_broadcast(notify_data)
        print(f"Sending push: {notify_data['ru']['title']} finished")
    else:
        print(f"There is no such push: {notify_data['ru']['title']}")


@celery_app.task
def automatic_push_to_user(fb_token, push_type):
    print("function automatic_push_to_user")
    print(fb_token)
    print(push_type)
    for n in NotificationTemplate.objects.all():
        print(n.push_type)
    print('changes applied')
    template = NotificationTemplate.objects.get(push_type=str(push_type))
    print("template: ", template)
    send_to_token(fb_token, template.title, template.description)


@celery_app.task
def push_order_rate_to_user(fb_token, order, lang=settings.DEFAULT_LANGUAGE):
    template = NotificationTemplate.objects.get(push_type=PushTypes.ORDER_RATE)
    extra = {
        'push_type': str(PushTypes.ORDER_RATE),
        'push_type_value': str(order.id)
    }
    send_to_token(fb_token, getattr(template.title, lang), getattr(template.description, lang), extra)


@celery_app.task
def push_order_status_update_to_user(fb_token, order, lang=settings.DEFAULT_LANGUAGE):
    template = NotificationTemplate.objects.get(push_type=PushTypes.ORDER_STATUS_UPDATE)
    title = getattr(template.title, lang).format(order.id)
    body = getattr(template.description, lang).format(order.status)
    extra = {
        'push_type': str(PushTypes.ORDER_STATUS_UPDATE),
        'push_type_value': str(order.id)
    }
    send_to_token(fb_token, title, body, extra)
