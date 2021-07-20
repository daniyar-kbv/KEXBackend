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
    f"{OBJECT_NOT_FOUND}_{Languages.KAZAKH}": ("not found kk", ""),
    f"{OBJECT_NOT_FOUND}_{Languages.ENGLISH}": ("not found end", ""),

    f"{TERMINAL_NOT_FOUND}_{Languages.RUSSIAN}": ("terminal_not_found_ru", ""),
    f"{TERMINAL_NOT_FOUND}_{Languages.KAZAKH}": ("terminal_not_found_kk", ""),
    f"{TERMINAL_NOT_FOUND}_{Languages.ENGLISH}": ("terminal_not_found_eng", ""),

    f"{OTP_RESEND_TIME_LIMIT}_{Languages.RUSSIAN}": ("Лимит времени для повторной отправки кода", ""),
    f"{OTP_RESEND_TIME_LIMIT}_{Languages.KAZAKH}": ("uakyt ali otpedy goi, brat", ""),
    f"{OTP_RESEND_TIME_LIMIT}_{Languages.ENGLISH}": ("time limit for otp resending", ""),

    f"{USER_NOT_FOUND}_{Languages.RUSSIAN}": ("Пользователь не найден", ""),
    f"{USER_NOT_FOUND}_{Languages.KAZAKH}": ("ondai adam zhok", ""),
    f"{USER_NOT_FOUND}_{Languages.ENGLISH}": ("There is no such user", ""),

    f"{INSTAGRAM_CODE_INVALID}_{Languages.RUSSIAN}": ("Инстаграм код неправильный", ""),
    f"{INSTAGRAM_CODE_INVALID}_{Languages.KAZAKH}": ("Instagram code invalid deimyn sagan", ""),
    f"{INSTAGRAM_CODE_INVALID}_{Languages.ENGLISH}": ("Instagram code invalid", ""),

    f"{INSTAGRAM_UNKNOWN_ERROR}_{Languages.RUSSIAN}": ("Инстаграм неизвестная ошибка", ""),
    f"{INSTAGRAM_UNKNOWN_ERROR}_{Languages.KAZAKH}": ("Instagram unknown error deimyn sagan", ""),
    f"{INSTAGRAM_UNKNOWN_ERROR}_{Languages.ENGLISH}": ("Instagram unknown error", ""),

    f"{EMPTY_CART}_{Languages.RUSSIAN}": ("Корзина пустая", ""),
    f"{EMPTY_CART}_{Languages.KAZAKH}": ("Корзина пустая", ""),
    f"{EMPTY_CART}_{Languages.ENGLISH}": ("Корзина пустая", ""),

    f"{ORDER_ALREADY_PAID}_{Languages.RUSSIAN}": ("Заказ уже оплачен", ""),
    f"{ORDER_ALREADY_PAID}_{Languages.KAZAKH}": ("Заказ уже оплачен", ""),
    f"{ORDER_ALREADY_PAID}_{Languages.ENGLISH}": ("Заказ уже оплачен", ""),

    f"{ORDER_ALREADY_EXISTS}_{Languages.RUSSIAN}": ("Заказ уже создан", ""),
    f"{ORDER_ALREADY_EXISTS}_{Languages.KAZAKH}": ("Заказ уже создан", ""),
    f"{ORDER_ALREADY_EXISTS}_{Languages.ENGLISH}": ("Заказ уже создан", ""),

    f"{USER_HAS_NO_ADDRESS}_{Languages.RUSSIAN}": ("USER_HAS_NO_ADDRESS", ""),
    f"{USER_HAS_NO_ADDRESS}_{Languages.KAZAKH}": ("USER_HAS_NO_ADDRESS", ""),
    f"{USER_HAS_NO_ADDRESS}_{Languages.ENGLISH}": ("USER_HAS_NO_ADDRESS", ""),
}
