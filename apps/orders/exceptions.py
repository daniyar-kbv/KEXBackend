from rest_framework.exceptions import APIException

from config.constants import error_codes


class EmptyCartError(APIException):
    status_code = 400
    default_code = error_codes.EMPTY_CART


class UserHasNoAddressError(APIException):
    status_code = 400
    default_code = error_codes.USER_HAS_NO_ADDRESS


class CouponNotActive(APIException):
    status_code = 400
    default_code = error_codes.COUPON_NOT_ACTIVE


class InvalidBranchError(APIException):
    status_code = 400
    default_code = error_codes.INVALID_BRANCH


class BranchNotActiveError(APIException):
    status_code = 400
    default_code = error_codes.BRANCH_NOT_ACTIVE


class TerminalNotActiveError(APIException):
    status_code = 400
    default_code = error_codes.TERMINAL_NOT_ACTIVE
