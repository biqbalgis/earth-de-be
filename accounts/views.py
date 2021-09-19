import json

from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf

from accounts.local_settings import USER_INFO_FIELDS
from earth_de_be.utils import Data_Logger


def userLogin(username, password, request):
    isUserExist = authenticate(username=username, password=password)
    token = csrf.get_token(request)
    if isUserExist is not None:
        auth.login(request, isUserExist)
        if request.session.session_key == '':
            request.session = SessionStore()
        request.user = User.objects.filter(username=username).first()
        user_data = list(User.objects.filter(username=username).values(*USER_INFO_FIELDS))[0]
        user_data["token"] = token
        userData = {'status': "ok", 'token': token, 'user': user_data,
                    "session_key": request.session.session_key}
    else:
        Data_Logger.log_error_message("User not authenticated", message_type='error')
        userData = {'status': "failed", 'errors': "Invalid Credentials"}
    return userData


@csrf_exempt
def login_user(request):
    try:
        if request.method == 'POST':
            user = request.POST['username'].lower()
            password = request.POST['password']
            response = userLogin(user, password, request)
            if response['status'] == 'ok':
                return JsonResponse(response, status=200)
            else:
                return JsonResponse(response, status=200)
    except Exception as e:
        Data_Logger.log_error_message(e)
    return JsonResponse({"status": "failed", 'errors': "Login Failed"})


def logout_user(request):
    try:
        session_obj = Session.objects.filter(session_key=request.session.session_key).first()
        if session_obj is not None:
            session_obj.delete()
        logout(request)
        return JsonResponse({"status": "ok"})
    except Exception as e:
        Data_Logger.log_error_message(e)
        return JsonResponse({"status": "failed", "message": "User not found"})
