from rest_framework.exceptions import APIException

from config.constants import USER_NOT_FOUND


class UserNotFound(APIException):
    status_code = 400
    default_code = USER_NOT_FOUND
