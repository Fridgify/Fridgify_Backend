import collections
from django.http import HttpResponse

from Fridgify_Backend.utils import register_handler


RESPONSE = {
    1: HttpResponse(status=201, content="Successfully created"),
    0: HttpResponse(status=400, content="Missing arguments"),
    -1: HttpResponse(status=500, content="Database Error. Contact your administrator"),
    -2: HttpResponse(status=409, content="Username already existing"),
    -3: HttpResponse(status=409, content="E-Mail already existing"),
}


def register(request):
    result = register_handler.register(request)
    return RESPONSE[result]


def error_response(request):
    res = HttpResponse(status=405)
    res["Allow"] = "POST"
    return res


HTTP_ENDPOINT_FUNCTION = collections.defaultdict(lambda: error_response)
HTTP_ENDPOINT_FUNCTION["POST"] = register


def entry_point(request):
    return HTTP_ENDPOINT_FUNCTION[request.method](request)
