from django.db.models import TextChoices


class OrderStatuses(TextChoices):
    NEW = "NEW", "",
    COOKING = "COOKING", ""
    IN_DELIVERY = "IN_DELIVERY"
    ISSUED = "ISSUED", "",
    FAILURE = "FAILURE", ""
