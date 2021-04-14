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

    f"{NOT_AUTHENTICATED}_{Languages.RUSSIAN}": ("Необходимо заново зайти в аккаунт", ""),
    f"{NOT_AUTHENTICATED}_{Languages.KAZAKH}": ("Kaitadan kir, brat", ""),
    f"{NOT_AUTHENTICATED}_{Languages.ENGLISH}": ("need to sign in again", ""),

    f"{INVALID_INPUT_DATA}_{Languages.RUSSIAN}": ("Не валидные данные", ""),
    f"{INVALID_INPUT_DATA}_{Languages.KAZAKH}": ("duris emes toltirdin, bratiwka", ""),
    f"{INVALID_INPUT_DATA}_{Languages.ENGLISH}": ("invalid input data", ""),

    f"{INVALID_OTP}_{Languages.RUSSIAN}": ("Не правильный otp", ""),
    f"{INVALID_OTP}_{Languages.KAZAKH}": ("kate otp"),
    f"{INVALID_OTP}_{Languages.ENGLISH}": ("invalid otp"),
}
