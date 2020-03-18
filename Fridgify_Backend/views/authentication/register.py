import json

import bcrypt
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from Fridgify_Backend.models import Users
from Fridgify_Backend.models import exceptions
from Fridgify_Backend.utils import api_utils
from Fridgify_Backend.utils.decorators import check_body

unique_keys = ("username", "password", "email", "name", "surname", "birth_date")


@api_view(["POST"])
@check_body(*unique_keys)
def register_view(request):
    body = json.loads(request.body.decode("utf-8"))
    try:
        password = bcrypt.hashpw(body["password"].encode("utf-8"), bcrypt.gensalt())
        obj, created = Users.objects.get_or_create(
            username=body["username"],
            password=password.decode("utf-8"),
            email=body["email"],
            name=body["name"],
            surname=body["surname"],
            birth_date=body["birth_date"],
        )
        if created:
            return Response(data="Created", status=201)
        else:
            duplicate_keys = api_utils.non_unique_keys(body, Users, *unique_keys)
            raise exceptions.ConflictException(detail=f"{' and '.join(duplicate_keys)} already exist(s)")
    except IntegrityError:
        duplicate_keys = api_utils.non_unique_keys(body, Users, *unique_keys)
        raise exceptions.ConflictException(detail=f"{' and '.join(duplicate_keys)} already exist(s)")
