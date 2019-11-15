from django.http import JsonResponse
from django.http import HttpResponse
import secrets


def entry_point(request):
    if request.method == "POST":
        login(request)
        return HttpResponse(status=200, content="Hello")
    else:
        return error_response()


def login(request):
    print(request)
    # Step 1. Authorization Header Check
    if "Authorization" in request.headers:
        # Step 1.A Check if Token is valid
        print("Authorization header exists...")
    else:
        # Step 1.B Check User Credentials
        print("Check credentials...")
    # Step 1. Create a Token


def error_response():
    res = HttpResponse(status=405, reason="Method not allowed.")
    res["Allow"] = "POST"
    return res
