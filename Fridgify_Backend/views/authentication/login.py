from django.http import JsonResponse
from django.http import HttpResponse
import secrets
import collections
import json

import Fridgify_Backend.utils.login_handler as login_handler
import Fridgify_Backend.utils.token_handler as token_handler


def login(request):
    if "Authorization" in request.headers:
        token = token_handler.check_token(request.headers["Authorization"], "Fridgify")
        if token is None:
            return HttpResponse(status=401, content="Invalid Token")
        else:
            return JsonResponse(status=200, data={"token": token})

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


HTTP_ENDPOINT_FUNCTION = collections.defaultdict(lambda: error_response)
HTTP_ENDPOINT_FUNCTION["POST"] = login


def entry_point(request):
    return HTTP_ENDPOINT_FUNCTION[request.method](request)
