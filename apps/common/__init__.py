from django.db import models

default_app_config = 'apps.common.apps.CommonConfig'


class ImageTypes(models.TextChoices):
    IMAGE_FOR_CHECK = ("IMAGE_FOR_CHECK", "Для Бренда: чек")
    IMAGE_SQUARE = ("IMAGE_SQUARE", "Для Бренда: квадрат")
    IMAGE_SHORT = ("IMAGE_SHORT", "Для Бренда: короткая")
    IMAGE_TALL = ("IMAGE_TALL", "Для Бренда: высокая")
    IMAGE_LONG = ("IMAGE_LONG", "Для Бренда: длинная")
    IMAGE_FOR_PROMOTION = ("IMAGE_FOR_PROMOTION", "Для Акции")
    IMAGE_FOR_POSITION = ("IMAGE_FOR_POSITION", "Для Позиции")


class PlatformTypes(models.TextChoices):
    WEB = ('WEB', "Веб")
    MOBILE = ('MOBILE', "Моб. приложение")
