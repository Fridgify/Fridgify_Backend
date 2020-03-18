import json

from django.db import IntegrityError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import exceptions
from Fridgify_Backend.models import UserFridge, Fridges
from Fridgify_Backend.utils.api_utils import serialize_object
from Fridgify_Backend.utils.decorators import check_body


@api_view(["POST"])
@check_body(*("name", "description"))
@permission_classes([IsAuthenticated])
@authentication_classes([APIAuthentication])
def create_fridge_view(request):
    body = json.loads(request.body)
    try:
        if UserFridge.objects.filter(user=request.user, fridge__name=body["name"]).exists():
            raise exceptions.ConflictException(detail="Fridge name already exists for user")
        fridge = Fridges.objects.create(name=body["name"], description=body["description"])
        UserFridge.objects.create(user=request.user, fridge=fridge)
        return Response(data=serialize_object(fridge, True), status=201)
    except IntegrityError:
        raise APIException(detail="Something went wrong", code=500)
