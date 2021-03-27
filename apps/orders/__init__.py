from django.db.models import TextChoices

default_app_config = 'apps.orders.apps.OrdersConfig'


class OrderStatuses(TextChoices):
    NEW = "NEW", "",
    COOKING = "COOKING", ""
    IN_DELIVERY = "IN_DELIVERY"
    ISSUED = "ISSUED", "",
    FAILURE = "FAILURE", ""
