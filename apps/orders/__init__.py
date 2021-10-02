from django.db.models import TextChoices

default_app_config = 'apps.orders.apps.OrdersConfig'


class OrderStatuses(TextChoices):
    NEW = "NEW", "Новый заказ"
    PAID = "PAID", "Оплачено"
    APPLYING = "APPLYING", "Процесс просадки в IIKO"
    APPLY_ERROR = "APPLY_ERROR", "Ошибка при просадке в IIKO"
    APPLIED = "APPLIED", "Просажено в IIKO"
    UNCONFIRMED = 'UNCONFIRMED', 'Заказ подтверждается'
    READY_FOR_COOKING = 'READY_FOR_COOKING', 'Заказ готов к приготовлению'
    COOKING_STARTED = 'COOKING_STARTED', 'Заказ в процессе готовки'
    COOKING_COMPLETED = 'COOKING_COMPLETED', 'Заказ приготовлен'
    WAITING = 'WAITING', 'Ожидание доставки заказа'
    ON_WAY = 'ON_WAY', 'Заказ доставляется'
    DELIVERED = 'DELIVERED', 'Заказ доставлен'
    DONE = 'DONE', 'Заказ завершен'
    CANCELLED = 'CANCELLED', 'Заказ отменен'
