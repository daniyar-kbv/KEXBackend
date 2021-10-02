from rest_framework.exceptions import APIException

from config.constants import error_codes


class CouponNotActive(APIException):
    status_code = 400
    default_code = error_codes.COUPON_NOT_ACTIVE
