from rest_framework.exceptions import APIException

from config.constants.error_codes import INSTAGRAM_CODE_INVALID, INSTAGRAM_UNKNOWN_ERROR


class InstagramCodeInvalid(APIException):
    status_code = 400
    default_code = INSTAGRAM_CODE_INVALID


class InstagramUnknownError(APIException):
    status_code = 400
    default_code = INSTAGRAM_UNKNOWN_ERROR
