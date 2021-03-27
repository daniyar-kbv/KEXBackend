from rest_framework.exceptions import APIException


class InvalidOTP(APIException):
    status_code = 400
    default_detail = "Неверный OTP-код"
