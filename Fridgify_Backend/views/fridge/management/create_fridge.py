from django.http import JsonResponse
from django.http import HttpResponse
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.utils import token_handler
import json
import collections


def create_fridge(request):
    """ Create a new fridge for user

    :param request: request with a body containing a name and a description for the fridge
    :return: Response code with information about the request
    """
    if "Authorization" not in request.headers:
        return JsonResponse(status=403, data={"message": "Authorization missing"})
    request_token = request.headers["Authorization"]
    token = token_handler.get_data_for_token(request_token)

    if token is None:
        return JsonResponse(status=403, data={"message": "Authorization token is invalid"})

    if not token_handler.is_token_valid(token):
        return JsonResponse(status=401, data={"message": "Token expired. Request a new one",
                                              "tokenUrl": "auth/token/"})

    if not validate_body(request):
        return JsonResponse(status=400, data={"message": "Missing parameters. Required are name and description"})
    body = json.loads(request.body)

    fridge_name = body["name"]

    if check_for_duplicate_fridge(token.user_id, fridge_name):
        return JsonResponse(status=409, data={"message": "Fridge {} already exists for user".format(fridge_name)})

    fridge = Fridges()
    fridge.description = body["description"]
    fridge.name = fridge_name
    fridge.save()

    print("Created fridge with", fridge.name, fridge.description, fridge.fridge_id)

    user = Users.objects.get(user_id=token.user_id)

    user_fridge = UserFridge()
    user_fridge.fridge = fridge
    user_fridge.user = user
    user_fridge.save()

    print("Created UserFridge relation with", fridge.fridge_id, user.user_id)

    return JsonResponse(status=201, data={"message": "Created"})


def check_for_duplicate_fridge(user_id, fridge_name):
    """ Check if fridge exists for user

    :param user_id: The id of the user
    :param fridge_name: The name for the new fridge
    :return: exists - True | doesnt exist - False
    """
    print("Check for duplicate fridge")
    user_fridge_entries = UserFridge.objects.filter(user_id=user_id).all()
    for entry in user_fridge_entries:
        fridge_id = entry.fridge_id
        fridge = Fridges.objects.get(fridge_id=fridge_id)
        if fridge.name == fridge_name:
            return True
    return False


def validate_body(request):
    """ Check if request has a valid body

    :param request: The request send by the user
    :return: valid - True | invalid - False
    """
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
