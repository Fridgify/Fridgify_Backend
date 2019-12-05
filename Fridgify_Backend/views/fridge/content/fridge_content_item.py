from django.http import HttpResponse
from django.http import JsonResponse

from Fridgify_Backend.utils import fridge_content_handler
from Fridgify_Backend.utils import token_handler


# GET, DELETE, POST
def add_item_to_fridge(request, fridge_id, item_id):
    return JsonResponse({"message": "Add item"})


def get_item_in_fridge(request, fridge_id, item_id):
    return JsonResponse({"message": "Get item"})


def remove_content_in_fridge(request, fridge_id, item_id):
    if "Authorization" in request.headers:
        user_id = get_user(request)
        if user_id is None:
            return HttpResponse(status=403, content="Token not valid")
        content = fridge_content_handler.remove_item(fridge_id, item_id)
        if content == -1:
            return HttpResponse(status=500, content="Error removing item")
        elif content == 0:
            return HttpResponse(status=404, content="Nothing found")
        return HttpResponse(status=200, content="Successfully removed")
    return HttpResponse(status=401, content="User not authorized")


HTTP_ENDPOINT_FUNCTION = {
    "GET": get_item_in_fridge,
    "POST": add_item_to_fridge,
    "DELETE": remove_content_in_fridge
}


def entry_point(request, fridge_id, item_id):
    response = HTTP_ENDPOINT_FUNCTION[request.method](request, fridge_id, item_id)
    return response


def check_req_add(req_body):
    if all(x in req_body for x in ["name", "description", "buy_date", "expiration_date", "amount", "unit", "store"]):
        return True
    return False


def get_user(request):
    api_token = request.headers["Authorization"]
    return token_handler.token_info(api_token, "Fridgify-API")