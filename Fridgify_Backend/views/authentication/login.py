from django.http import JsonResponse
from django.http import HttpResponse
import secrets
import json

import Fridgify_Backend.utils.login_handler as login_handler
import Fridgify_Backend.utils.token_handler as token_handler


def entry_point(request):
    if request.method == "POST":
        return login(request)
    else:
        return error_response()


def login(request):
    if "Authorization" in request.headers:
        print("Authorization header exists...")

    # Check Credentials
    cred_check = login_handler.check_credentials(request)
    if cred_check == 1:
        token = token_handler.generate_token(json.load(request)["username"], "Fridgify")
        return JsonResponse(status=200, data={"token": token})
    elif cred_check == 0:
        return HttpResponse(status=401, content="Wrong Credentials")
    else:
        return HttpResponse(status=400, content="Bad Request")


def error_response():
    res = HttpResponse(status=405)
    res["Allow"] = "POST"
    return res
