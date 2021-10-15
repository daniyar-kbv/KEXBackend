from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

from .tasks import register_token_in_firebase
from .models import Notification, FirebaseToken
from .services import form_notify_data
from .tasks import push_broadcast_later


@receiver(post_save, sender=Notification)
def save_notification_signal(sender, instance, **kwargs):
    print("SAVE_NOTIFICATION_SIGNAL (sender): %r" % instance)
    notify_data = form_notify_data(instance)
    print("SAVE_NOTIFICATION_SIGNAL (body): %r" % notify_data)

    if instance.date <= timezone.now():
        push_broadcast_later(notify_data)
    else:
        sec_delta = int(instance.date.timestamp() - timezone.now().timestamp())
        push_broadcast_later.apply_async((notify_data,), countdown=sec_delta)


@receiver(post_save, sender=FirebaseToken)
def save_fbtoken_signal(sender, instance, **kwargs):
    if instance.user:
        language = instance.user.language
    else:
        language = settings.DEFAULT_LANGUAGE

    register_token_in_firebase.delay(topic=language, registration_tokens=instance.token)
