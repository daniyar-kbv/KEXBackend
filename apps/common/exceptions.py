from rest_framework.exceptions import APIException

from config.constants import error_codes


class IOSNotAvailableError(APIException):
    status_code = 400
    default_code = error_codes.IOS_NOT_AVAILABLE


class AndroidNotAvailableError(APIException):
    status_code = 400
    default_code = error_codes.ANDROID_NOT_AVAILABLE
