from rest_framework.exceptions import APIException

from config.constants.error_codes import EMPTY_CART, ORDER_ALREADY_EXISTS


class EmptyCartError(APIException):
    status_code = 400
    default_code = EMPTY_CART


class OrderAlreadyExistError(APIException):
    status_code = 400
    default_code = ORDER_ALREADY_EXISTS
