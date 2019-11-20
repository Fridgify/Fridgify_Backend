from django.http import JsonResponse
from django.http import HttpResponse
from Fridgify_Backend.models.fridges import Fridges
import json
import collections


def create_fridge(request):
    if not validate_body(request):
        return JsonResponse(status=400, data={"message": "Missing parameters. Required are name and description"})
    body = json.loads(request.body)

    fridge = Fridges()
    fridge.description = body["name"]
    fridge.name = body["description"]
    fridge.save()

    print("Created fridge with", fridge.name, fridge.description, fridge.fridge_id)

    fridge_id = fridge["id"]

    # TODO: Add relation to user

    return JsonResponse(status=201, data={"message": "Created"})


def validate_body(request):
    if not hasattr(request, "body"):
        return False
    req_body = json.loads(request.body)
    print(req_body)
    if "name" not in req_body:
        return False
    if "description" not in req_body:
        return False
    return True


def error_response(request):
    res = HttpResponse(status=405)
    res["Allow"] = "POST"
    return res


def entry_point(request):
    return HTTP_ENDPOINT_FUNCTION[request.method](request)


HTTP_ENDPOINT_FUNCTION = collections.defaultdict(lambda: error_response)
HTTP_ENDPOINT_FUNCTION["POST"] = create_fridge
