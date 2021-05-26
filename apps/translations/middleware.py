class LanguageHeaderMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_request(request)

    def process_request(self, request):
        # print('inside my custom middleware')
        langs = {'ru': 'ru', 'kk': 'kk', 'en': 'en'}
        language = request.META.get('HTTP_LANGUAGE')
        if not language or not langs.get(language):
            request.META.update({'HTTP_LANGUAGE': 'ru'})
        response = self.get_response(request)
        return response
