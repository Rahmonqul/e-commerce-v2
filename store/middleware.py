from django.utils import translation
from django.conf import settings

class CustomLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.headers.get('Accept-Language', 'en')
        if language not in dict(settings.LANGUAGES):
            language = 'en'
        translation.activate(language)
        response = self.get_response(request)
        translation.deactivate()
        return response

import threading

_request_storage = threading.local()

def get_current_request():
    return getattr(_request_storage, 'request', None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_storage.request = request
        response = self.get_response(request)
        return response

