from apps.notifications.models import Notification
from config.settings import Languages


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
