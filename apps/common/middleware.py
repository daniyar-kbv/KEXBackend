from config.constants import user_agents_mobile


class UserAgent(object):
    user_agent_string = None
    is_mobile = None
    is_pc = None

    def __init__(self, uastring):
        print('uastring', uastring)
        self.user_agent_string = uastring
        self.is_pc = False
        self.is_mobile = False

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
        setattr(request, 'user_agent', UserAgent(user_agent))
        response = self.get_response(request)
        return response
