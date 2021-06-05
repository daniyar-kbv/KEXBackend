from django.db import models

default_app_config = 'apps.partners.apps.PartnersConfig'


class BrandImageTypes(models.TextChoices):
    IMAGE_SQUARE = ("IMAGE_SQUARE", "квадрат")
    IMAGE_SHORT = ("IMAGE_SHORT", "короткая")
    IMAGE_TALL = ("IMAGE_TALL", "высокая")
    IMAGE_LONG = ("IMAGE_LONG", "длинная")
