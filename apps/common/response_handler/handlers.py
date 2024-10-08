from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional

from constance import config
from django.conf import settings
from rest_framework.exceptions import ErrorDetail

from config.constants import error_codes

from .dataclasses import CustomError


class AbstractHandler(ABC):
    _default_error_code: str = None
    use_default_code: bool = False

    def __init__(
            self,
            raw_data: Dict,
            language: str = None,
            device_uuid: str = None,
    ) -> None:
        self.raw_data = raw_data
        self.language = language or settings.DEFAULT_LANGUAGE
        self.device_uuid = device_uuid

    def get_error_detail(self) -> Tuple[str, str]:
        _error_code, _error_message = self._default_error_code, ""

        if isinstance(self.raw_data.get("detail"), ErrorDetail) and not self.use_default_code:
            _error_code = self.raw_data.get("detail").code

        _config_error_code = f"{_error_code}_{self.language}"

        if hasattr(config, _config_error_code):
            _error_message = getattr(config, _config_error_code)

        return _error_code, _error_message

    @abstractmethod
    def format_logic(self) -> Tuple[
        Optional[Dict], Optional[Dict]
    ]:
        """
        Response format logic
        """

    def format(self):
        return self.format_logic()


class HandlerCode200(AbstractHandler):
    def format_logic(self):
        return self.raw_data, None


class HandlerCode400(AbstractHandler):
    _default_error_code = error_codes.INVALID_INPUT_DATA

    def format_logic(self):
        return None, CustomError(*self.get_error_detail()).__dict__


class HandlerCode401(AbstractHandler):
    _default_error_code = error_codes.NOT_AUTHENTICATED

    def format_logic(self):
        if self.device_uuid:
            from apps.notifications.tasks import unregister_token_from_firebase
            from apps.notifications.models import FirebaseToken

            fbtoken: FirebaseToken = FirebaseToken.objects.filter(
                token=self.device_uuid,
            ).first()
            if fbtoken:
                fbtoken.delete()
                unregister_token_from_firebase.delay(self.device_uuid)

        return None, CustomError(*self.get_error_detail()).__dict__


class HandlerCode404(AbstractHandler):
    _default_error_code = error_codes.NOT_FOUND

    def format_logic(self):
        return None, CustomError(*self.get_error_detail()).__dict__


class HandlerCode429(AbstractHandler):
    _default_error_code = error_codes.TOO_MANY_REQUESTS
    use_default_code = True

    def format_logic(self):
        return None, CustomError(*self.get_error_detail()).__dict__
