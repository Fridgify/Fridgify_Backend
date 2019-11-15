from django.http import JsonResponse

# GET POST


def add_store(request):
    return JsonResponse({"message": "Add store"})


def get_store(request):
    return JsonResponse({"message": "Get store"})


HTTP_ENDPOINT_FUNCTION = {
    "GET": get_store,
    "POST": add_store
}


def entry_point(request):
    response = HTTP_ENDPOINT_FUNCTION[request](request)
    return response
