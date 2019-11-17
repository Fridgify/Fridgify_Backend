from django.http import HttpResponse
from django.http import JsonResponse
import jwt

import Fridgify_Backend.utils.token_handler as token_handler


def entry_point(request):
    if request.method == "GET":
        token = get_token(request)
        if token is None:
            return HttpResponse(content="Not Authorized", status=401)
        else:
            return JsonResponse(data={"token": token, "validation_time": 3600}, status=200, )
    else:
        return error_response()


def get_token(request):
    if "Authorization" in request.headers:
        login_token_enc = request.headers["Authorization"]
        try:
            login_token_dec = jwt.decode(login_token_enc, verify=False)
        except jwt.DecodeError:
            return None
        e_token = token_handler.existing_tokens(login_token_dec["user"], "Fridgify")
        if e_token == login_token_enc:
            token = token_handler.generate_token(login_token_dec["user"], "Fridgify-API")
            return token
    return None


def error_response():
    res = HttpResponse(status=405)
    res["Allow"] = "GET"
    return res
