from rest_framework.exceptions import APIException

from config.constants.error_codes import ORDER_ALREADY_PAID


class OrderAlreadyPaidError(APIException):
    status_code = 400
    default_code = ORDER_ALREADY_PAID
