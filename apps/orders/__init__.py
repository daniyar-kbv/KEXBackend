from django.db.models import TextChoices

default_app_config = 'apps.orders.apps.OrdersConfig'


class OrderStatuses(TextChoices):
    NEW = "NEW", "Новый заказ"
    PAID = "PAID", "Оплачено"
    IN_PROGRESS = "IN_PROGRESS"
    COOKING = "COOKING", "Готовится"
    IN_DELIVERY = "IN_DELIVERY", "Доставляется"
    ISSUED = "ISSUED", "Доставлен"
    FAILURE = "FAILURE", "Ошибка"
