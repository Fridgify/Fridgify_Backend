from django.http import JsonResponse, HttpResponse
from Fridgify_Backend.utils import token_handler
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
import collections


def get_fridges(request):
    if "Authorization" not in request.headers:
        return JsonResponse(status=403, data={"message": "Authorization missing"})
    request_token = request.headers["Authorization"]
    token = token_handler.get_data_for_token(request_token)

    if token is None:
        return JsonResponse(status=403, data={"message": "Authorization token is invalid"})

    if not token_handler.is_token_valid(token):
        return JsonResponse(status=401, data={"message": "Token expired. Request a new one",
                                              "tokenUrl": "auth/token/"})

    user_fridges = UserFridge.objects.filter(user_id=token.user_id)

    payload = []

    for user_fridge in user_fridges:
        fridge = Fridges.objects.get(fridge_id=user_fridge.fridge_id)
        payload.append({
            "id": fridge.fridge_id,
            "name": fridge.name,
            "description": fridge.description,
            "content": "tbd"
        })

    return JsonResponse(status=201, data={"fridges": payload})


def error_response(request):
    res = HttpResponse(status=405)
    res["Allow"] = "GET"
    return res


def entry_point(request):
    return HTTP_ENDPOINT_FUNCTION[request.method](request)


HTTP_ENDPOINT_FUNCTION = collections.defaultdict(lambda: error_response)
HTTP_ENDPOINT_FUNCTION["GET"] = get_fridges
