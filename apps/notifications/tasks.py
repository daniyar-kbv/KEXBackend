import logging

from .models import Notification
from config import celery_app
from .firebase import push_broadcast

logger = logging.getLogger('fcm')


@celery_app.task
def push_broadcast_later(notify_data):
    push = Notification.objects.filter(title__text_ru=notify_data['ru']['title'], date=notify_data['date'])
    print(f"Push exists or not: {push}")
    print("Push data: ")
    print(str(notify_data))
    if push:
        del notify_data['date']
        print(f"Sending push: {notify_data['ru']['title']} started")
        push_broadcast(notify_data)
        print(f"Sending push: {notify_data['ru']['title']} finished")
    else:
        print(f"There is no such push: {notify_data['ru']['title']}")
