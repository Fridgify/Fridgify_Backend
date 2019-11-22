import json
from django.http import JsonResponse


def add_content_to_fridge(request):
    return JsonResponse({"message": "Add content"})


def get_content_in_fridge(request):
    return JsonResponse({"message": "Get content"})


HTTP_ENDPOINT_FUNCTION = {
    "GET": get_content_in_fridge,
    "POST": add_content_to_fridge
}


def entry_point(request):
    response = HTTP_ENDPOINT_FUNCTION[request.method](request)
    return response


def check_req_add(req_body):
    if all(x in req_body for x in ["name", "description", "buy_date", "expiration_date", "amount", "unit", "store"]):
        return True
    return False
