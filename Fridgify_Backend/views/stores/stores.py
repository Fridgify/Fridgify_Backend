import json

from django.db import IntegrityError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils.api_utils import serialize_object
from Fridgify_Backend.utils.decorators import check_body
from Fridgify_Backend.models import Stores


@api_view(["GET", "POST"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def stores_view(request):
    if request.method == "GET":
        stores = Stores.objects.all()
        return Response(data=[serialize_object(store, True) for store in stores], status=200)
    else:
        return create_store(request)


@check_body("name")
def create_store(request):
    body = json.loads(request.body)
    try:
        store = Stores.objects.create(name=body["name"])
        return Response(data=serialize_object(store, True), status=201)
    except IntegrityError:
        raise APIException(detail="Store already exists", code=409)
