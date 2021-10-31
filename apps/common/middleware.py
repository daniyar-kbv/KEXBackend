from constance import config
from django.http import JsonResponse

from config.constants import user_agents_mobile

from .exceptions import IOSNotAvailableError, AndroidNotAvailableError


class UserAgent(object):
    user_agent_string: str = None
    is_mobile: bool = None
    is_pc: bool = None
    error_code: str = None
    error_message: str = ""

    def __init__(self, uastring):
        self.user_agent_string = uastring
        self.is_pc = False
        self.is_mobile = False

        if uastring == 'IOS' and not config.IOS_ON:
            self.error_code = IOSNotAvailableError.default_code
            if hasattr(config, f"{self.error_code}_ru"):
                self.error_message = getattr(config, f"{self.error_code}_ru")

        if uastring == 'Android' and not config.ANDROID_ON:
            self.error_code = AndroidNotAvailableError.default_code
            if hasattr(config, f"{self.error_code}_ru"):
                self.error_message = getattr(config, f"{self.error_code}_ru")

        if uastring:
            for uword in user_agents_mobile:
                if uword in uastring:
                    self.is_mobile = True
                    break

        if not self.is_mobile:
            self.is_pc = True


class UserAgentMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_request(request)

    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')
        user_agent_instance = UserAgent(user_agent)
        setattr(request, 'user_agent', user_agent_instance)

        if user_agent_instance.error_code:
            return JsonResponse({"data": None, "error": {
                "code": user_agent_instance.error_code,
                "message": user_agent_instance.error_message,
            }})

        response = self.get_response(request)
        return response
