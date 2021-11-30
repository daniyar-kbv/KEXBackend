from rest_framework.exceptions import APIException

from config.constants import error_codes


class EmptyCartError(APIException):
    status_code = 400
    default_code = error_codes.EMPTY_CART


class UserHasNoAddressError(APIException):
    status_code = 400
    default_code = error_codes.USER_HAS_NO_ADDRESS


class InvalidBranchError(APIException):
    status_code = 400
    default_code = error_codes.INVALID_BRANCH


class BranchNotActiveError(APIException):
    status_code = 400
    default_code = error_codes.BRANCH_NOT_ACTIVE


class TerminalNotActiveError(APIException):
    status_code = 400
    default_code = error_codes.TERMINAL_NOT_ACTIVE


class DeliveryNotAvailableError(APIException):
    status_code = 400
    default_code = error_codes.DELIVERY_NOT_AVAILABLE


class BranchIsClosedError(APIException):
    status_code = 400
    default_code = error_codes.BRANCH_IS_CLOSED


class DeliveryIsChangedError(APIException):
    status_code = 400
    default_code = error_codes.DELIVERY_IS_CHANGED


class OutOfStockError(APIException):
    status_code = 400
    default_code = error_codes.CART_POSITION_IS_OUT_OF_STOCK
