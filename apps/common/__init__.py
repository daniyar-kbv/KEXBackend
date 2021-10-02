from django.db import models

default_app_config = 'apps.common.apps.CommonConfig'


class ImageTypes(models.TextChoices):
    IMAGE_FOR_CHECK = ("image_for_check", "Для Бренда: чек")
    IMAGE_SQUARE = ("image_square", "Для Бренда: квадрат")
    IMAGE_SHORT = ("image_short", "Для Бренда: короткая")
    IMAGE_TALL = ("image_tall", "Для Бренда: высокая")
    IMAGE_LONG = ("image_long", "Для Бренда: длинная")
    IMAGE_FOR_PROMOTION = ("image_for_promotion", "Для Акции")
    IMAGE_FOR_POSITION = ("image_for_position", "Для Позиции")


class PlatformTypes(models.TextChoices):
    WEB = ('WEB', "Веб")
    MOBILE = ('MOBILE', "Моб. приложение")
