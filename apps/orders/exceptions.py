from rest_framework.exceptions import APIException

from config.constants.error_codes import (
    EMPTY_CART,
    USER_HAS_NO_ADDRESS,
    COUPON_NOT_ACTIVE)


class EmptyCartError(APIException):
    status_code = 400
    default_code = EMPTY_CART


class UserHasNoAddressError(APIException):
    status_code = 400
    default_code = USER_HAS_NO_ADDRESS


class CouponNotActive(APIException):
    status_code = 400
    default_code = COUPON_NOT_ACTIVE
