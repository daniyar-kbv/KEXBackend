from rest_framework.exceptions import APIException

from config.constants.error_codes import FIREBASE_TOKEN_DOESNT_EXIST


class FirebaseTokenDoesntExist(APIException):
    status_code = 400
    default_code = FIREBASE_TOKEN_DOESNT_EXIST