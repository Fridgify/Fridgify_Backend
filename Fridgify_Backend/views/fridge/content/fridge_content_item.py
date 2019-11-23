from django.http import JsonResponse

from Fridgify_Backend.utils import test_utils


# GET, DELETE, POST
def add_item_to_fridge(request):
    return JsonResponse({"message": "Add item"})


def get_item_in_fridge(request):
    return JsonResponse({"message": "Get item"})


def delete_item_in_fridge(request):
    return JsonResponse({"message": "Delete item"})


HTTP_ENDPOINT_FUNCTION = {
    "GET": get_item_in_fridge,
    "POST": add_item_to_fridge,
    "DELETE": delete_item_in_fridge
}


def entry_point(request):
    response = HTTP_ENDPOINT_FUNCTION[request](request)
    return response
