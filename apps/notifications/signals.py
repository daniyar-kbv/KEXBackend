from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

from apps.orders.models.orders import Lead

from .firebase import subscribe_to_language_topic
from .models import Notification, FirebaseToken
from .services import form_notify_data
from .tasks import push_broadcast_later


@receiver(post_save, sender=Notification)
def save_notification_signal(sender, instance, **kwargs):
    print("notification post_save signal started")
    print("signal of instance: ", instance)
    notify_data = form_notify_data(instance)

    print(notify_data)

    if instance.date <= timezone.now():
        push_broadcast_later(notify_data)
    else:
        sec_delta = int(instance.date.timestamp() - timezone.now().timestamp())
        print("This is seconds delta: ", sec_delta)
        push_broadcast_later.apply_async((notify_data,), countdown=sec_delta)
    print("notification post_save signal ended")


@receiver(post_save, sender=FirebaseToken)
def save_fbtoken_signal(sender, instance, **kwargs):
    if instance.user:
        language = instance.user.language
    else:
        language = settings.DEFAULT_LANGUAGE

    subscribe_to_language_topic(language, [instance.token])
