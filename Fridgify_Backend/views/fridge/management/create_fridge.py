import json

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import exceptions
from Fridgify_Backend.models import UserFridge, Fridges, FridgeSerializer
from Fridgify_Backend.utils.decorators import check_body


@swagger_auto_schema(
    method="post",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Create a new fridge",
    request_body=FridgeSerializer,
    responses={
        201: openapi.Response("Created fridge", FridgeSerializer),
        500: "Internal Server Error",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["POST"])
@check_body("name")
@permission_classes([IsAuthenticated])
@authentication_classes([APIAuthentication])
def create_fridge_view(request):
    body = json.loads(request.body)
    try:
        if UserFridge.objects.filter(user=request.user, fridge__name=body["name"]).exists():
            raise exceptions.ConflictException(detail="Fridge name already exists for user")
        if "description" in body:
            fridge = Fridges.objects.create(name=body["name"], description=body["description"])
        else:
            fridge = Fridges.objects.create(name=body["name"])
        UserFridge.objects.create(user=request.user, fridge=fridge)
        return Response(data=FridgeSerializer(fridge).data, status=201)
    except IntegrityError:
        raise APIException(detail="Something went wrong", code=500)
