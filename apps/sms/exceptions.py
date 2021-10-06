from rest_framework.exceptions import APIException

from config.constants.error_codes import INVALID_OTP, OTP_RESEND_TIME_LIMIT


class InvalidOTP(APIException):
    status_code = 400
    default_detail = "Неверный OTP-код"
    default_code = INVALID_OTP


class OTPResendTimeLimit(APIException):
    status_code = 400
    default_detail = "Еще не прошел лимит времени для повторной отправки кода"
    default_code = OTP_RESEND_TIME_LIMIT
