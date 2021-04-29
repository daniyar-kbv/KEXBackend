from rest_framework.exceptions import APIException

from config.constants import INVALID_OTP


class InvalidOTP(APIException):
    status_code = 400
    default_detail = "Неверный OTP-код"
    default_code = INVALID_OTP
