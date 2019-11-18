from django.http import JsonResponse
from django.http import HttpResponse
import secrets
import json

import Fridgify_Backend.utils.login_handler as login_handler
import Fridgify_Backend.utils.token_handler as token_handler


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


def error_response(request):
    res = HttpResponse(status=405)
    res["Allow"] = "POST"
    return res


HTTP_ENDPOINT_FUNCTION = {
    "POST": login,
    "GET": error_response,
    "DELETE": error_response,
    "PUT": error_response
}


def entry_point(request):
    return HTTP_ENDPOINT_FUNCTION[request.method](request)