from django.db import models

default_app_config = 'apps.partners.apps.PartnersConfig'


class BrandImageTypes(models.TextChoices):
    IMAGE_FOR_CHECK = ("IMAGE_FOR_CHECK", "для чека")
    IMAGE_SQUARE = ("IMAGE_SQUARE", "квадрат")
    IMAGE_SHORT = ("IMAGE_SHORT", "короткая")
    IMAGE_TALL = ("IMAGE_TALL", "высокая")
    IMAGE_LONG = ("IMAGE_LONG", "длинная")


class DeliveryTypes(models.TextChoices):
    DAY_DELIVERY = 'DAY_DELIVERY', 'Дневная доставка'
    NIGHT_DELIVERY = 'NIGHT_DELIVERY', 'Ночная доставка'


class PlatformTypes(models.TextChoices):
    WEB = ('WEB', "Веб")
    MOBILE = ('MOBILE', "Моб. приложение")
