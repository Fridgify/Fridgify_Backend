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
