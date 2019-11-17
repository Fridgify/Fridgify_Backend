from django.http import JsonResponse
from django.http import HttpResponse
import secrets

from Fridgify_Backend.utils.login_handler import *


def entry_point(request):
    if request.method == "POST":
        return login(request)
    else:
        return error_response()


def login(request):
    if "Authorization" in request.headers:
        print("Authorization header exists...")

    # Check Credentials
    cred_check = check_credentials(request)
    if cred_check == 1:
        return JsonResponse(status=200, data={"token": "Token A"})
    elif cred_check == 0:
        return HttpResponse(status=401, content="Wrong Credentials")
    else:
        return HttpResponse(status=400, content="Bad Request")


def error_response():
    res = HttpResponse(status=405)
    res["Allow"] = "POST"
    return res
