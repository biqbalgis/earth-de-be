from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse

from ct_django.utils import Data_Logger, MIDDLEWARE_Utils


class MicorserviceSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # without_session_list = ['/api/v2/login/', '/api/v2/logout/', '/api/v2/register/']
        try:
            session_key = request.headers['x-session-key'] if 'x-session-key' in request.headers else None
            url = MIDDLEWARE_Utils.get_request_url(request)
            # host = url.split(':')
            # ip = host[0]
            # port = int(host[len(host) - 1])
            if session_key is not None and session_key != "":
                session = SessionStore(session_key=session_key)
                user_id = session.get('_auth_user_id')
                if user_id:
                    request.user = User.objects.filter(id=user_id).first()
                    request.session = session
            if not request.session.session_key:
                request.session.save()
            response = self.get_response(request)
            return response
        except Exception as e:
            Data_Logger.log_error_message(e)

        return JsonResponse({"status": "failed", 'message': "Your session has expired. Please log in again"})
