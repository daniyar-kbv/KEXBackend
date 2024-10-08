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

    f"{NOT_FOUND}_{Languages.RUSSIAN}": ("NOT_FOUND_RU", ""),
    f"{NOT_FOUND}_{Languages.KAZAKH}": ("NOT_FOUND_KK", ""),
    f"{NOT_FOUND}_{Languages.ENGLISH}": ("NOT_FOUND_EN", ""),

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

    f"{CHANGE_FOR_NOT_SET}_{Languages.RUSSIAN}": ("CHANGE_FOR_NOT_SET_RU", ""),
    f"{CHANGE_FOR_NOT_SET}_{Languages.KAZAKH}": ("CHANGE_FOR_NOT_SET_KK", ""),
    f"{CHANGE_FOR_NOT_SET}_{Languages.ENGLISH}": ("CHANGE_FOR_NOT_SET_EN", ""),

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

    f"{DELIVERY_NOT_AVAILABLE}_{Languages.RUSSIAN}": ("DELIVERY_IS_NOT_AVAILABLE_RU", ""),
    f"{DELIVERY_NOT_AVAILABLE}_{Languages.KAZAKH}": ("DELIVERY_IS_NOT_AVAILABLE_KK", ""),
    f"{DELIVERY_NOT_AVAILABLE}_{Languages.ENGLISH}": ("DELIVERY_IS_NOT_AVAILABLE_EN", ""),

    f"{BRANCH_IS_CLOSED}_{Languages.RUSSIAN}": ("BRANCH_IS_CLOSED_RU", ""),
    f"{BRANCH_IS_CLOSED}_{Languages.KAZAKH}": ("BRANCH_IS_CLOSED_KK", ""),
    f"{BRANCH_IS_CLOSED}_{Languages.ENGLISH}": ("BRANCH_IS_CLOSED_EN", ""),

    f"{FIREBASE_TOKEN_DOESNT_EXIST}_{Languages.RUSSIAN}": ("FIREBASE_TOKEN_DOESNT_EXIST_RU", ""),
    f"{FIREBASE_TOKEN_DOESNT_EXIST}_{Languages.KAZAKH}": ("FIREBASE_TOKEN_DOESNT_EXIST_KK", ""),
    f"{FIREBASE_TOKEN_DOESNT_EXIST}_{Languages.ENGLISH}": ("FIREBASE_TOKEN_DOESNT_EXIST_EN", ""),

    f"{TOO_MANY_REQUESTS}_{Languages.RUSSIAN}": ("TOO_MANY_REQUESTS_RU", ""),
    f"{TOO_MANY_REQUESTS}_{Languages.KAZAKH}": ("TOO_MANY_REQUESTS_KK", ""),
    f"{TOO_MANY_REQUESTS}_{Languages.ENGLISH}": ("TOO_MANY_REQUESTS_EN", ""),

    f"{CART_POSITION_IS_OUT_OF_STOCK}_{Languages.RUSSIAN}": ("CART_POSITION_IS_OUT_OF_STOCK_RU", ""),
    f"{CART_POSITION_IS_OUT_OF_STOCK}_{Languages.KAZAKH}": ("CART_POSITION_IS_OUT_OF_STOCK_KK", ""),
    f"{CART_POSITION_IS_OUT_OF_STOCK}_{Languages.ENGLISH}": ("CART_POSITION_IS_OUT_OF_STOCK_EN", ""),

    f"{IOS_NOT_AVAILABLE}_{Languages.RUSSIAN}": ("IOS_NOT_AVAILABLE_RU", ""),
    f"{IOS_NOT_AVAILABLE}_{Languages.KAZAKH}": ("IOS_NOT_AVAILABLE_KK", ""),
    f"{IOS_NOT_AVAILABLE}_{Languages.ENGLISH}": ("IOS_NOT_AVAILABLE_EN", ""),

    f"{ANDROID_NOT_AVAILABLE}_{Languages.RUSSIAN}": ("IOS_NOT_AVAILABLE_RU", ""),
    f"{ANDROID_NOT_AVAILABLE}_{Languages.KAZAKH}": ("IOS_NOT_AVAILABLE_KK", ""),
    f"{ANDROID_NOT_AVAILABLE}_{Languages.ENGLISH}": ("IOS_NOT_AVAILABLE_EN", ""),

    f"{DELIVERY_IS_CHANGED}_{Languages.RUSSIAN}": ("DELIVERY_IS_CHANGED_RU", ""),
    f"{DELIVERY_IS_CHANGED}_{Languages.KAZAKH}": ("DELIVERY_IS_CHANGED_KK", ""),
    f"{DELIVERY_IS_CHANGED}_{Languages.ENGLISH}": ("DELIVERY_IS_CHANGED_EN", ""),

    f"{MIN_PRICE_ERROR}_{Languages.RUSSIAN}": ("MIN_PRICE_ERROR_RU", ""),
    f"{MIN_PRICE_ERROR}_{Languages.KAZAKH}": ("MIN_PRICE_ERROR_KK", ""),
    f"{MIN_PRICE_ERROR}_{Languages.ENGLISH}": ("MIN_PRICE_ERROR_EN", ""),
}
