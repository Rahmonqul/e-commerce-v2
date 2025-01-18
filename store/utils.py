import threading

_local = threading.local()

def get_request():
    return getattr(_local, 'request', None)

def set_request(request):
    _local.request = request