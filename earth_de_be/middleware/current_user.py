from threading import local

_user = local()
_request_path = local()


class CurrentUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        _request_path.value = request.path
        return self.get_response(request)

    def process_request(self, request):
        _user.value = request.user


def get_current_user():
    try:
        return _user.value if _user.value.id is not None else None
    except:
        return None


def get_request_path():
    try:
        return _request_path.value
    except:
        return None
