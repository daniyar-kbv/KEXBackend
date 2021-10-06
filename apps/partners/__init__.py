from django.db import models

default_app_config = 'apps.partners.apps.PartnersConfig'


class DeliveryTypes(models.TextChoices):
    DAY_DELIVERY = 'DAY_DELIVERY', 'Дневная доставка'
    NIGHT_DELIVERY = 'NIGHT_DELIVERY', 'Ночная доставка'
