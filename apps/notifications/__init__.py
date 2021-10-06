from django.db.models import TextChoices

default_app_config = 'apps.notifications.apps.NotificationsConfig'


class PushTypes(TextChoices):
    INFO = ("INFO", "Информативный")
    ORDER_RATE = ("ORDER_RATE", "Оценка заказа")
    ORDER_STATUS_UPDATE = ("ORDER_STATUS_UPDATE", "Обновление статуса заказа")
    PROMOTION = ("PROMOTION", "Акция")
