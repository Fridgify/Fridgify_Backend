import json

from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from Fridgify_Backend.models import Users
from Fridgify_Backend.utils import db_utils
from Fridgify_Backend.utils.decorators import check_body

unique_keys = ("username", "password", "email", "name", "surname", "birth_date")


@api_view(["POST"])
@check_body(*unique_keys)
def register_view(request):
    body = json.loads(request.body.decode("utf-8"))
    try:
        obj, created = Users.objects.get_or_create(
            username=body["username"],
            password=body["password"],
            email=body["email"],
            name=body["name"],
            surname=body["surname"],
            birth_date=body["birth_date"],
        )
        if created:
            return Response(data="Created", status=201)
        else:
            duplicate_keys = db_utils.non_unique_keys(body, Users, *unique_keys)
            raise APIException(detail=f"{' and '.join(duplicate_keys)} already exist(s)", code=409)
    except IntegrityError:
        duplicate_keys = db_utils.non_unique_keys(body, Users, *unique_keys)
        raise APIException(detail=f"{' and '.join(duplicate_keys)} already exist(s)", code=409)
