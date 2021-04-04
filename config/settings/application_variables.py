import os

from django.db.models import TextChoices

from .error_codes import *


class Languages(TextChoices):
    KAZAKH = "kk", "Казахский"
    RUSSIAN = "ru", "Русский"
    ENGLISH = "en", "Английский"


DEFAULT_LANGUAGE = Languages.RUSSIAN

CONSTANCE_CONFIG = {
    f"{NO_ACTIVE_ACCOUNT}_{Languages.RUSSIAN}": ("Вы ввели неверные данные для входа в систему", ""),
    f"{NO_ACTIVE_ACCOUNT}_{Languages.KAZAKH}": ("kiretin dannilar duris emes, brat", ""),
    f"{NO_ACTIVE_ACCOUNT}_{Languages.ENGLISH}": ("invalid auth credentials to sign in", ""),

    f"{ACCESS_EXPIRED}_{Languages.RUSSIAN}": ("Необходимо заново зайти в аккаунт", ""),
    f"{ACCESS_EXPIRED}_{Languages.KAZAKH}": ("Kaitadan kir, brat", ""),
    f"{ACCESS_EXPIRED}_{Languages.ENGLISH}": ("need to sign in again", ""),
}
