import json
from django.http import JsonResponse
from django.http import HttpResponse

from Fridgify_Backend.utils import token_handler
from Fridgify_Backend.utils import fridge_content_handler


def add_content_to_fridge(request, fridge_id):
    if "Authorization" in request.headers:
        user_id = get_user(request)
        if user_id is None:
            return HttpResponse(status=403, content="Token not valid")
        try:
            req_body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400, content="Request body parsing went wrong")
        if not check_req_add(req_body):
            return HttpResponse(status=400, content="Missing request attributes")
        status = fridge_content_handler.fridge_add_item(fridge_id, user_id, req_body)
        if status == -1:
            return HttpResponse(status=500, content="Something went wrong adding the item. Probably already exists.")
        elif status == 0:
            return HttpResponse(status=401, content="User not authorized to use fridge")
    else:
        return HttpResponse(status=401, content="Not Authorized")
    return HttpResponse(status=201, content="Item was added")


def get_content_in_fridge(request, fridge_id):
    if "Authorization" in request.headers:
        user_id = get_user(request)
        if user_id is None:
            return HttpResponse(status=403, content="Token not valid")
        content = fridge_content_handler.fridge_get_item(fridge_id, user_id)
        if content == -1:
            return HttpResponse(status=500, content="Error retrieving fridge content.")
        elif content is None:
            return HttpResponse(status=404, content="Fridge not existing")
        elif content == 0:
            return HttpResponse(status=403, content="User not authorized for fridge")

        return JsonResponse(list(content), safe=False)
    return HttpResponse(status=401, content="User not authorized")


HTTP_ENDPOINT_FUNCTION = {
    "GET": get_content_in_fridge,
    "POST": add_content_to_fridge
}


def entry_point(request, fridge_id):
    response = HTTP_ENDPOINT_FUNCTION[request.method](request, fridge_id)
    return response


def check_req_add(req_body):
    if all(x in req_body for x in ["name", "description", "buy_date", "expiration_date", "amount", "unit", "store"]):
        return True
    return False


def get_user(request):
    api_token = request.headers["Authorization"]
    return token_handler.token_info(api_token, "Fridgify-API")