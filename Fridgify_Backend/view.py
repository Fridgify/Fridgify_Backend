from django.http import JsonResponse


def hello_world():
    return JsonResponse({"message": "Hello World"})
