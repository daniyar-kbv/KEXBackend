from rest_framework.exceptions import APIException

from config.constants.error_codes import OBJECT_NOT_FOUND, TERMINAL_NOT_FOUND


class BrandNotFound(APIException):
    status_code = 400
    default_code = OBJECT_NOT_FOUND


class TerminalNotFound(APIException):
    status_code = 400
    default_code = TERMINAL_NOT_FOUND
