from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from Fridgify_Backend.utils import token_handler
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
from Fridgify_Backend.models.fridge_content import FridgeContent
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
        content = check_content(fridge)
        payload.append({
            "id": fridge.fridge_id,
            "name": fridge.name,
            "description": fridge.description,
            "content": content
        })

    return JsonResponse(status=200, data={"fridges": payload})


def check_content(fridge):
    fresh = 0
    due_soon = 0
    over_due = 0
    total = 0
    content = FridgeContent.objects.filter(fridge_id=fridge.fridge_id)

    for item in content:
        expiration_date = datetime(year=item.expiration_date.year, month=item.expiration_date.month, day=item.expiration_date.day)
        created_at = datetime(year=item.created_at.year, month=item.created_at.month, day=item.created_at.day)
        delta = expiration_date - datetime.today()
        if delta.days < 0:
            over_due += 1
            continue
        if 5 > delta.days >= 0:
            due_soon += 1
            continue
        if (created_at - datetime.today()).days < 5:
            fresh += 1
            continue
        total += 1

    return {
        "total": total + fresh + due_soon + over_due,
        "fresh": fresh,
        "dueSoon": due_soon,
        "overDue": over_due
    }


def error_response(request):
    res = HttpResponse(status=405)
    res["Allow"] = "GET"
    return res


def entry_point(request):
    return HTTP_ENDPOINT_FUNCTION[request.method](request)


HTTP_ENDPOINT_FUNCTION = collections.defaultdict(lambda: error_response)
HTTP_ENDPOINT_FUNCTION["GET"] = get_fridges
