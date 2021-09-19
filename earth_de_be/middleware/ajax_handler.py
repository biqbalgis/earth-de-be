import json

from django.http import JsonResponse

from earth_de_be.local_settings import FRONT_END_PORT
from earth_de_be.utils import Data_Logger, MIDDLEWARE_Utils


class AjaxMessaging:
    """
    Middlware for JSON responses. It adds to each JSON response array with
    messages from django.contrib.messages framework.
    It allows handle messages on a page with javascript
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        url = MIDDLEWARE_Utils.get_request_url(request)
        request_path = request.path
        is_failure = False
        if url.port in FRONT_END_PORT:
            msg = "Starting Request"
            Data_Logger.log_message(msg)
        response = self.get_response(request)
        if request.is_ajax():
            if response['Content-Type'] not in ["application/javascript", "application/json"]:
                if url.port in FRONT_END_PORT:
                    msg = "Failed to get response"
                    Data_Logger.log_message("Failed Request: Due to non json response", message_type="error")
                    is_failure = True
                    return JsonResponse({"status": "failed", "message": msg}, status=404)
            else:
                res = json.loads(response.content)
                if res['status'].lower() == "failed":
                    is_failure = True
                    Data_Logger.log_message("Failed Request", message_type="error")
        if url.port in FRONT_END_PORT:
            if is_failure == True:
                Data_Logger.log_message("Complete Request with Error")
            else:
                Data_Logger.log_message("Complete Request Successfully")
        return response
