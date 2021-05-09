from .error_codes import *
from config.settings import Languages


ERROR_MESSAGES = {
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
    f"{INVALID_OTP}_{Languages.KAZAKH}": ("kate otp", ""),
    f"{INVALID_OTP}_{Languages.ENGLISH}": ("invalid otp", ""),

    f"{OBJECT_NOT_FOUND}_{Languages.RUSSIAN}": ("not found ru", ""),
    f"{OBJECT_NOT_FOUND}_{Languages.KAZAKH}": ("not found kz", ""),
    f"{OBJECT_NOT_FOUND}_{Languages.ENGLISH}": ("not found kz", ""),
}
