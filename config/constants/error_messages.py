from .error_codes import *
from config.settings import Languages


ERROR_MESSAGES = {
    f"{NO_ACTIVE_ACCOUNT}_{Languages.RUSSIAN}": ("NO_ACTIVE_ACCOUNT_RU", ""),
    f"{NO_ACTIVE_ACCOUNT}_{Languages.KAZAKH}": ("NO_ACTIVE_ACCOUNT_KK", ""),
    f"{NO_ACTIVE_ACCOUNT}_{Languages.ENGLISH}": ("NO_ACTIVE_ACCOUNT_EN", ""),

    f"{NOT_AUTHENTICATED}_{Languages.RUSSIAN}": ("NOT_AUTHENTICATED_RU", ""),
    f"{NOT_AUTHENTICATED}_{Languages.KAZAKH}": ("NOT_AUTHENTICATED_KK", ""),
    f"{NOT_AUTHENTICATED}_{Languages.ENGLISH}": ("NOT_AUTHENTICATED_EN", ""),

    f"{INVALID_INPUT_DATA}_{Languages.RUSSIAN}": ("INVALID_INPUT_DATA_RU", ""),
    f"{INVALID_INPUT_DATA}_{Languages.KAZAKH}": ("INVALID_INPUT_DATA_KK", ""),
    f"{INVALID_INPUT_DATA}_{Languages.ENGLISH}": ("INVALID_INPUT_DATA_EN", ""),

    f"{INVALID_OTP}_{Languages.RUSSIAN}": ("INVALID_OTP_RU", ""),
    f"{INVALID_OTP}_{Languages.KAZAKH}": ("INVALID_OTP_KK", ""),
    f"{INVALID_OTP}_{Languages.ENGLISH}": ("INVALID_OTP_EN", ""),

    f"{OBJECT_NOT_FOUND}_{Languages.RUSSIAN}": ("OBJECT_NOT_FOUND_RU", ""),
    f"{OBJECT_NOT_FOUND}_{Languages.KAZAKH}": ("OBJECT_NOT_FOUND_KK", ""),
    f"{OBJECT_NOT_FOUND}_{Languages.ENGLISH}": ("OBJECT_NOT_FOUND_EN", ""),

    f"{TERMINAL_NOT_FOUND}_{Languages.RUSSIAN}": ("TERMINAL_NOT_FOUND_RU", ""),
    f"{TERMINAL_NOT_FOUND}_{Languages.KAZAKH}": ("TERMINAL_NOT_FOUND_KK", ""),
    f"{TERMINAL_NOT_FOUND}_{Languages.ENGLISH}": ("TERMINAL_NOT_FOUND_EN", ""),

    f"{OTP_RESEND_TIME_LIMIT}_{Languages.RUSSIAN}": ("OTP_RESEND_TIME_LIMIT_RU", ""),
    f"{OTP_RESEND_TIME_LIMIT}_{Languages.KAZAKH}": ("OTP_RESEND_TIME_LIMIT_KK", ""),
    f"{OTP_RESEND_TIME_LIMIT}_{Languages.ENGLISH}": ("OTP_RESEND_TIME_LIMIT_EN", ""),

    f"{USER_NOT_FOUND}_{Languages.RUSSIAN}": ("USER_NOT_FOUND_RU", ""),
    f"{USER_NOT_FOUND}_{Languages.KAZAKH}": ("USER_NOT_FOUND_KK", ""),
    f"{USER_NOT_FOUND}_{Languages.ENGLISH}": ("USER_NOT_FOUND_EN", ""),

    f"{INSTAGRAM_CODE_INVALID}_{Languages.RUSSIAN}": ("INSTAGRAM_CODE_INVALID_RU", ""),
    f"{INSTAGRAM_CODE_INVALID}_{Languages.KAZAKH}": ("INSTAGRAM_CODE_INVALID_KK", ""),
    f"{INSTAGRAM_CODE_INVALID}_{Languages.ENGLISH}": ("INSTAGRAM_CODE_INVALID_EN", ""),

    f"{INSTAGRAM_UNKNOWN_ERROR}_{Languages.RUSSIAN}": ("INSTAGRAM_UNKNOWN_ERROR_RU", ""),
    f"{INSTAGRAM_UNKNOWN_ERROR}_{Languages.KAZAKH}": ("INSTAGRAM_UNKNOWN_ERROR_KK", ""),
    f"{INSTAGRAM_UNKNOWN_ERROR}_{Languages.ENGLISH}": ("INSTAGRAM_UNKNOWN_ERROR_EN", ""),

    f"{EMPTY_CART}_{Languages.RUSSIAN}": ("EMPTY_CART_RU", ""),
    f"{EMPTY_CART}_{Languages.KAZAKH}": ("EMPTY_CART_KK", ""),
    f"{EMPTY_CART}_{Languages.ENGLISH}": ("EMPTY_CART_EN", ""),

    f"{ORDER_ALREADY_PAID}_{Languages.RUSSIAN}": ("ORDER_ALREADY_PAID_RU", ""),
    f"{ORDER_ALREADY_PAID}_{Languages.KAZAKH}": ("ORDER_ALREADY_PAID_KK", ""),
    f"{ORDER_ALREADY_PAID}_{Languages.ENGLISH}": ("ORDER_ALREADY_PAID_EN", ""),

    f"{USER_HAS_NO_ADDRESS}_{Languages.RUSSIAN}": ("USER_HAS_NO_ADDRESS_RU", ""),
    f"{USER_HAS_NO_ADDRESS}_{Languages.KAZAKH}": ("USER_HAS_NO_ADDRESS_KK", ""),
    f"{USER_HAS_NO_ADDRESS}_{Languages.ENGLISH}": ("USER_HAS_NO_ADDRESS_EN", ""),

    f"{INVALID_BRANCH}_{Languages.RUSSIAN}": ("INVALID_BRANCH_RU", ""),
    f"{INVALID_BRANCH}_{Languages.KAZAKH}": ("INVALID_BRANCH_KK", ""),
    f"{INVALID_BRANCH}_{Languages.ENGLISH}": ("INVALID_BRANCH_EN", ""),

    f"{COUPON_NOT_ACTIVE}_{Languages.RUSSIAN}": ("COUPON_NOT_ACTIVE_RU", ""),
    f"{COUPON_NOT_ACTIVE}_{Languages.KAZAKH}": ("COUPON_NOT_ACTIVE_KK", ""),
    f"{COUPON_NOT_ACTIVE}_{Languages.ENGLISH}": ("COUPON_NOT_ACTIVE_EN", ""),

    f"{BRANCH_NOT_ACTIVE}_{Languages.RUSSIAN}": ("BRANCH_NOT_ACTIVE_RU", ""),
    f"{BRANCH_NOT_ACTIVE}_{Languages.KAZAKH}": ("BRANCH_NOT_ACTIVE_KK", ""),
    f"{BRANCH_NOT_ACTIVE}_{Languages.ENGLISH}": ("BRANCH_NOT_ACTIVE_EN", ""),

    f"{TERMINAL_NOT_ACTIVE}_{Languages.RUSSIAN}": ("TERMINAL_NOT_ACTIVE_RU", ""),
    f"{TERMINAL_NOT_ACTIVE}_{Languages.KAZAKH}": ("TERMINAL_NOT_ACTIVE_KK", ""),
    f"{TERMINAL_NOT_ACTIVE}_{Languages.ENGLISH}": ("TERMINAL_NOT_ACTIVE_EN", ""),

}
